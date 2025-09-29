# 同期システム設計

## 概要

NotionとObsidianの既存機能を最大限活用し、両プラットフォーム間の情報同期を実現する軽量な同期システムを設計します。データベースを設けず、既存のプラットフォームの機能を活用する設計です。

## アーキテクチャ

```
┌─────────────────────────────────────────────────────────────┐
│                    Sync Coordinator                         │
├─────────────────────────────────────────────────────────────┤
│  Change Detector │ Conflict Resolver │ Data Transformer     │
│  • 変更検出      │  • 競合解決      │  • データ変換        │
│  • イベント監視  │  • ユーザー判断  │  • フォーマット変換  │
│  • 差分計算      │  • 自動解決      │  • メタデータ処理    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                External Platform APIs                        │
├─────────────────────────────────────────────────────────────┤
│  Notion API │ Obsidian FS │ File Watcher │ Event Queue      │
│  • ページ操作  │  • ファイル監視  │  • 変更検出    │  • イベント管理  │
│  • データベース│  • メタデータ    │  • 通知送信    │  • 優先度管理  │
│  • ブロック    │  • リンク解析    │  • エラー処理  │  • リトライ    │
└─────────────────────────────────────────────────────────────┘
```

## 主要コンポーネント

### 1. 変更検出器

**役割**: NotionとObsidianの変更を検出
**機能**:
- ファイルシステム監視
- API ポーリング
- イベント駆動の変更検出
- 差分計算

**実装例**:
```python
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from notion_client import Client

class ChangeDetector:
    def __init__(self, notion_token, obsidian_path):
        self.notion_client = Client(auth=notion_token)
        self.obsidian_path = obsidian_path
        self.observer = Observer()
        self.last_sync_times = {}
    
    def start_monitoring(self):
        """監視の開始"""
        # Obsidianファイルの監視
        event_handler = ObsidianFileHandler(self.obsidian_path)
        self.observer.schedule(event_handler, self.obsidian_path, recursive=True)
        self.observer.start()
        
        # Notion API のポーリング
        self.start_notion_polling()
    
    def start_notion_polling(self):
        """Notion API のポーリング"""
        while True:
            try:
                self.check_notion_changes()
                time.sleep(30)  # 30秒間隔でポーリング
            except Exception as e:
                print(f"Notion polling error: {e}")
                time.sleep(60)  # エラー時は1分待機
    
    def check_notion_changes(self):
        """Notionの変更をチェック"""
        # 最近更新されたページを取得
        pages = self.notion_client.search(
            query="",
            filter={"property": "object", "value": "page"},
            sort={"direction": "descending", "timestamp": "last_edited_time"}
        )
        
        for page in pages:
            page_id = page['id']
            last_edited = page['last_edited_time']
            
            # 前回の同期時刻と比較
            if page_id not in self.last_sync_times or \
               last_edited > self.last_sync_times[page_id]:
                
                self.handle_notion_change(page)
                self.last_sync_times[page_id] = last_edited
    
    def handle_notion_change(self, page):
        """Notionの変更を処理"""
        change_event = {
            'type': 'notion_change',
            'page_id': page['id'],
            'title': page['properties']['title']['title'][0]['text']['content'],
            'last_edited': page['last_edited_time'],
            'action': 'update'
        }
        
        # イベントキューに追加
        self.add_to_event_queue(change_event)

class ObsidianFileHandler(FileSystemEventHandler):
    def __init__(self, obsidian_path):
        self.obsidian_path = obsidian_path
        self.change_detector = None
    
    def set_change_detector(self, change_detector):
        self.change_detector = change_detector
    
    def on_modified(self, event):
        if event.is_directory:
            return
        
        if event.src_path.endswith('.md'):
            self.handle_file_change(event.src_path)
    
    def on_created(self, event):
        if event.is_directory:
            return
        
        if event.src_path.endswith('.md'):
            self.handle_file_change(event.src_path, action='create')
    
    def on_deleted(self, event):
        if event.is_directory:
            return
        
        if event.src_path.endswith('.md'):
            self.handle_file_change(event.src_path, action='delete')
    
    def handle_file_change(self, file_path, action='update'):
        """ファイル変更を処理"""
        change_event = {
            'type': 'obsidian_change',
            'file_path': file_path,
            'action': action,
            'timestamp': time.time()
        }
        
        # イベントキューに追加
        if self.change_detector:
            self.change_detector.add_to_event_queue(change_event)
```

### 2. 競合解決器

**役割**: 同期競合の検出と解決
**機能**:
- 競合検出
- ユーザー判断の支援
- 自動解決ルール
- 競合履歴の管理

**実装例**:
```python
class ConflictResolver:
    def __init__(self):
        self.conflict_rules = {
            'notion_priority': self.resolve_notion_priority,
            'obsidian_priority': self.resolve_obsidian_priority,
            'newer_wins': self.resolve_newer_wins,
            'user_choice': self.resolve_user_choice
        }
    
    def detect_conflict(self, notion_content, obsidian_content):
        """競合を検出"""
        conflicts = []
        
        # タイトルの競合
        if notion_content['title'] != obsidian_content['title']:
            conflicts.append({
                'type': 'title_conflict',
                'notion_value': notion_content['title'],
                'obsidian_value': obsidian_content['title'],
                'field': 'title'
            })
        
        # コンテンツの競合
        if notion_content['content'] != obsidian_content['content']:
            conflicts.append({
                'type': 'content_conflict',
                'notion_value': notion_content['content'],
                'obsidian_value': obsidian_content['content'],
                'field': 'content'
            })
        
        # メタデータの競合
        if notion_content['tags'] != obsidian_content['tags']:
            conflicts.append({
                'type': 'tags_conflict',
                'notion_value': notion_content['tags'],
                'obsidian_value': obsidian_content['tags'],
                'field': 'tags'
            })
        
        return conflicts
    
    def resolve_conflict(self, conflict, resolution_strategy='user_choice'):
        """競合を解決"""
        if resolution_strategy in self.conflict_rules:
            return self.conflict_rules[resolution_strategy](conflict)
        else:
            return self.resolve_user_choice(conflict)
    
    def resolve_notion_priority(self, conflict):
        """Notion優先で解決"""
        return {
            'resolved_value': conflict['notion_value'],
            'resolution_reason': 'Notion priority rule',
            'confidence': 0.8
        }
    
    def resolve_obsidian_priority(self, conflict):
        """Obsidian優先で解決"""
        return {
            'resolved_value': conflict['obsidian_value'],
            'resolution_reason': 'Obsidian priority rule',
            'confidence': 0.8
        }
    
    def resolve_newer_wins(self, conflict):
        """新しい方で解決"""
        notion_time = conflict.get('notion_timestamp', 0)
        obsidian_time = conflict.get('obsidian_timestamp', 0)
        
        if notion_time > obsidian_time:
            return {
                'resolved_value': conflict['notion_value'],
                'resolution_reason': 'Newer wins rule (Notion)',
                'confidence': 0.9
            }
        else:
            return {
                'resolved_value': conflict['obsidian_value'],
                'resolution_reason': 'Newer wins rule (Obsidian)',
                'confidence': 0.9
            }
    
    def resolve_user_choice(self, conflict):
        """ユーザー選択で解決"""
        return {
            'resolved_value': None,  # ユーザーの選択を待つ
            'resolution_reason': 'User choice required',
            'confidence': 1.0,
            'requires_user_input': True,
            'options': [
                {'value': conflict['notion_value'], 'label': 'Notion version'},
                {'value': conflict['obsidian_value'], 'label': 'Obsidian version'},
                {'value': 'merge', 'label': 'Merge both versions'}
            ]
        }
```

### 3. データ変換器

**役割**: プラットフォーム間のデータ変換
**機能**:
- Notion → Obsidian 変換
- Obsidian → Notion 変換
- メタデータの処理
- フォーマットの統一

**実装例**:
```python
class DataTransformer:
    def __init__(self):
        self.conversion_rules = {
            'notion_to_obsidian': self.convert_notion_to_obsidian,
            'obsidian_to_notion': self.convert_obsidian_to_notion
        }
    
    def convert_notion_to_obsidian(self, notion_content):
        """NotionからObsidianへの変換"""
        obsidian_content = {
            'title': notion_content['title'],
            'content': self.convert_notion_blocks_to_markdown(notion_content['blocks']),
            'frontmatter': {
                'notion_id': notion_content['id'],
                'created_time': notion_content['created_time'],
                'last_edited_time': notion_content['last_edited_time'],
                'tags': notion_content.get('tags', []),
                'source': 'notion'
            },
            'metadata': notion_content.get('metadata', {})
        }
        
        return obsidian_content
    
    def convert_obsidian_to_notion(self, obsidian_content):
        """ObsidianからNotionへの変換"""
        notion_content = {
            'title': obsidian_content['title'],
            'blocks': self.convert_markdown_to_notion_blocks(obsidian_content['content']),
            'properties': {
                'title': {'title': [{'text': {'content': obsidian_content['title']}}]},
                'obsidian_id': obsidian_content.get('id'),
                'file_path': obsidian_content.get('file_path'),
                'tags': obsidian_content.get('frontmatter', {}).get('tags', [])
            },
            'metadata': obsidian_content.get('metadata', {})
        }
        
        return notion_content
    
    def convert_notion_blocks_to_markdown(self, blocks):
        """NotionブロックをMarkdownに変換"""
        markdown_content = []
        
        for block in blocks:
            if block['type'] == 'paragraph':
                text = self.extract_rich_text(block['paragraph']['rich_text'])
                markdown_content.append(text)
            elif block['type'] == 'heading_1':
                text = self.extract_rich_text(block['heading_1']['rich_text'])
                markdown_content.append(f"# {text}")
            elif block['type'] == 'heading_2':
                text = self.extract_rich_text(block['heading_2']['rich_text'])
                markdown_content.append(f"## {text}")
            elif block['type'] == 'heading_3':
                text = self.extract_rich_text(block['heading_3']['rich_text'])
                markdown_content.append(f"### {text}")
            elif block['type'] == 'bulleted_list_item':
                text = self.extract_rich_text(block['bulleted_list_item']['rich_text'])
                markdown_content.append(f"- {text}")
            elif block['type'] == 'numbered_list_item':
                text = self.extract_rich_text(block['numbered_list_item']['rich_text'])
                markdown_content.append(f"1. {text}")
            elif block['type'] == 'code':
                code = block['code']['rich_text'][0]['text']['content']
                language = block['code']['language']
                markdown_content.append(f"```{language}\n{code}\n```")
            elif block['type'] == 'quote':
                text = self.extract_rich_text(block['quote']['rich_text'])
                markdown_content.append(f"> {text}")
            # 他のブロックタイプも同様に変換
        
        return '\n'.join(markdown_content)
    
    def convert_markdown_to_notion_blocks(self, markdown_content):
        """MarkdownをNotionブロックに変換"""
        blocks = []
        lines = markdown_content.split('\n')
        
        for line in lines:
            if line.startswith('# '):
                blocks.append({
                    'type': 'heading_1',
                    'heading_1': {'rich_text': [{'text': {'content': line[2:]}}]}
                })
            elif line.startswith('## '):
                blocks.append({
                    'type': 'heading_2',
                    'heading_2': {'rich_text': [{'text': {'content': line[3:]}}]}
                })
            elif line.startswith('### '):
                blocks.append({
                    'type': 'heading_3',
                    'heading_3': {'rich_text': [{'text': {'content': line[4:]}}]}
                })
            elif line.startswith('- '):
                blocks.append({
                    'type': 'bulleted_list_item',
                    'bulleted_list_item': {'rich_text': [{'text': {'content': line[2:]}}]}
                })
            elif line.startswith('1. '):
                blocks.append({
                    'type': 'numbered_list_item',
                    'numbered_list_item': {'rich_text': [{'text': {'content': line[3:]}}]}
                })
            elif line.startswith('> '):
                blocks.append({
                    'type': 'quote',
                    'quote': {'rich_text': [{'text': {'content': line[2:]}}]}
                })
            elif line.startswith('```'):
                # コードブロックの処理
                language = line[3:] if len(line) > 3 else ''
                code_lines = []
                i = lines.index(line) + 1
                while i < len(lines) and not lines[i].startswith('```'):
                    code_lines.append(lines[i])
                    i += 1
                
                blocks.append({
                    'type': 'code',
                    'code': {
                        'rich_text': [{'text': {'content': '\n'.join(code_lines)}}],
                        'language': language
                    }
                })
            else:
                # 通常の段落
                blocks.append({
                    'type': 'paragraph',
                    'paragraph': {'rich_text': [{'text': {'content': line}}]}
                })
        
        return blocks
    
    def extract_rich_text(self, rich_text_array):
        """リッチテキスト配列からテキストを抽出"""
        text_parts = []
        for text_obj in rich_text_array:
            text_parts.append(text_obj['text']['content'])
        return ''.join(text_parts)
```

## 同期フロー

### 1. 双方向同期

**目的**: NotionとObsidian間の双方向同期
**フロー**:

```python
class SyncCoordinator:
    def __init__(self, notion_client, obsidian_path):
        self.notion_client = notion_client
        self.obsidian_path = obsidian_path
        self.change_detector = ChangeDetector(notion_client, obsidian_path)
        self.conflict_resolver = ConflictResolver()
        self.data_transformer = DataTransformer()
        self.event_queue = []
    
    def start_sync(self):
        """同期の開始"""
        self.change_detector.start_monitoring()
        
        while True:
            # イベントキューから変更を取得
            if self.event_queue:
                event = self.event_queue.pop(0)
                self.process_change_event(event)
            
            time.sleep(1)  # 1秒間隔でチェック
    
    def process_change_event(self, event):
        """変更イベントを処理"""
        if event['type'] == 'notion_change':
            self.handle_notion_change(event)
        elif event['type'] == 'obsidian_change':
            self.handle_obsidian_change(event)
    
    def handle_notion_change(self, event):
        """Notionの変更を処理"""
        try:
            # Notionページの詳細を取得
            page = self.notion_client.pages.retrieve(event['page_id'])
            notion_content = self.extract_notion_content(page)
            
            # 対応するObsidianファイルを検索
            obsidian_file = self.find_corresponding_obsidian_file(event['page_id'])
            
            if obsidian_file:
                # 既存ファイルの更新
                obsidian_content = self.read_obsidian_file(obsidian_file)
                
                # 競合をチェック
                conflicts = self.conflict_resolver.detect_conflict(
                    notion_content, obsidian_content
                )
                
                if conflicts:
                    # 競合を解決
                    resolved_content = self.resolve_conflicts(conflicts)
                    self.update_obsidian_file(obsidian_file, resolved_content)
                else:
                    # 競合なし、直接更新
                    obsidian_content = self.data_transformer.convert_notion_to_obsidian(notion_content)
                    self.update_obsidian_file(obsidian_file, obsidian_content)
            else:
                # 新しいファイルの作成
                obsidian_content = self.data_transformer.convert_notion_to_obsidian(notion_content)
                self.create_obsidian_file(obsidian_content)
                
        except Exception as e:
            print(f"Error handling Notion change: {e}")
    
    def handle_obsidian_change(self, event):
        """Obsidianの変更を処理"""
        try:
            # Obsidianファイルの内容を読み取り
            obsidian_content = self.read_obsidian_file(event['file_path'])
            
            # 対応するNotionページを検索
            notion_page_id = self.find_corresponding_notion_page(event['file_path'])
            
            if notion_page_id:
                # 既存ページの更新
                notion_content = self.extract_notion_content(
                    self.notion_client.pages.retrieve(notion_page_id)
                )
                
                # 競合をチェック
                conflicts = self.conflict_resolver.detect_conflict(
                    notion_content, obsidian_content
                )
                
                if conflicts:
                    # 競合を解決
                    resolved_content = self.resolve_conflicts(conflicts)
                    self.update_notion_page(notion_page_id, resolved_content)
                else:
                    # 競合なし、直接更新
                    notion_content = self.data_transformer.convert_obsidian_to_notion(obsidian_content)
                    self.update_notion_page(notion_page_id, notion_content)
            else:
                # 新しいページの作成
                notion_content = self.data_transformer.convert_obsidian_to_notion(obsidian_content)
                self.create_notion_page(notion_content)
                
        except Exception as e:
            print(f"Error handling Obsidian change: {e}")
    
    def resolve_conflicts(self, conflicts):
        """競合を解決"""
        resolved_content = {}
        
        for conflict in conflicts:
            resolution = self.conflict_resolver.resolve_conflict(conflict)
            
            if resolution['requires_user_input']:
                # ユーザーの選択を待つ
                user_choice = self.request_user_choice(conflict, resolution['options'])
                resolved_content[conflict['field']] = user_choice
            else:
                resolved_content[conflict['field']] = resolution['resolved_value']
        
        return resolved_content
    
    def request_user_choice(self, conflict, options):
        """ユーザーの選択を要求"""
        # 実際の実装では、UI でユーザーに選択を求める
        # ここでは簡略化して最初のオプションを選択
        return options[0]['value']
```

### 2. 競合解決フロー

**目的**: 同期競合の適切な解決
**フロー**:

```python
class ConflictResolutionFlow:
    def __init__(self):
        self.resolution_strategies = {
            'automatic': self.automatic_resolution,
            'user_choice': self.user_choice_resolution,
            'hybrid': self.hybrid_resolution
        }
    
    def automatic_resolution(self, conflict):
        """自動解決"""
        # ルールベースの自動解決
        if conflict['type'] == 'title_conflict':
            return self.resolve_title_conflict(conflict)
        elif conflict['type'] == 'content_conflict':
            return self.resolve_content_conflict(conflict)
        elif conflict['type'] == 'tags_conflict':
            return self.resolve_tags_conflict(conflict)
    
    def user_choice_resolution(self, conflict):
        """ユーザー選択による解決"""
        # ユーザーに選択肢を提示
        options = [
            {'value': conflict['notion_value'], 'label': 'Notion version'},
            {'value': conflict['obsidian_value'], 'label': 'Obsidian version'},
            {'value': 'merge', 'label': 'Merge both versions'}
        ]
        
        return self.present_user_choice(conflict, options)
    
    def hybrid_resolution(self, conflict):
        """ハイブリッド解決"""
        # 自動解決を試行
        automatic_result = self.automatic_resolution(conflict)
        
        # 信頼度が低い場合はユーザーに確認
        if automatic_result['confidence'] < 0.8:
            return self.user_choice_resolution(conflict)
        else:
            return automatic_result
    
    def resolve_title_conflict(self, conflict):
        """タイトル競合の解決"""
        # より長いタイトルを選択
        if len(conflict['notion_value']) > len(conflict['obsidian_value']):
            return {
                'resolved_value': conflict['notion_value'],
                'resolution_reason': 'Longer title',
                'confidence': 0.7
            }
        else:
            return {
                'resolved_value': conflict['obsidian_value'],
                'resolution_reason': 'Longer title',
                'confidence': 0.7
            }
    
    def resolve_content_conflict(self, conflict):
        """コンテンツ競合の解決"""
        # より長いコンテンツを選択
        if len(conflict['notion_value']) > len(conflict['obsidian_value']):
            return {
                'resolved_value': conflict['notion_value'],
                'resolution_reason': 'Longer content',
                'confidence': 0.6
            }
        else:
            return {
                'resolved_value': conflict['obsidian_value'],
                'resolution_reason': 'Longer content',
                'confidence': 0.6
            }
    
    def resolve_tags_conflict(self, conflict):
        """タグ競合の解決"""
        # タグをマージ
        notion_tags = set(conflict['notion_value'])
        obsidian_tags = set(conflict['obsidian_value'])
        merged_tags = list(notion_tags.union(obsidian_tags))
        
        return {
            'resolved_value': merged_tags,
            'resolution_reason': 'Merged tags',
            'confidence': 0.9
        }
```

## 技術スタック

### 1. ファイルシステム監視

**ライブラリ**:
- **watchdog**: ファイルシステム監視
- **inotify**: Linux のファイルシステム監視
- **fsevents**: macOS のファイルシステム監視

**実装例**:
```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class FileSystemMonitor:
    def __init__(self, path):
        self.path = path
        self.observer = Observer()
        self.event_handler = FileSystemEventHandler()
    
    def start_monitoring(self):
        """監視の開始"""
        self.observer.schedule(self.event_handler, self.path, recursive=True)
        self.observer.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        
        self.observer.join()
    
    def stop_monitoring(self):
        """監視の停止"""
        self.observer.stop()
        self.observer.join()
```

### 2. API 統合

**ライブラリ**:
- **notion-client**: Notion API
- **requests**: HTTP クライアント
- **aiohttp**: 非同期HTTP クライアント

**実装例**:
```python
from notion_client import Client
import aiohttp
import asyncio

class APIIntegration:
    def __init__(self, notion_token):
        self.notion_client = Client(auth=notion_token)
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def sync_notion_to_obsidian(self, page_id):
        """NotionからObsidianへの同期"""
        try:
            # Notionページの取得
            page = self.notion_client.pages.retrieve(page_id)
            
            # ブロックの取得
            blocks = self.notion_client.blocks.children.list(page_id)
            
            # Obsidianファイルへの変換
            obsidian_content = self.convert_to_obsidian(page, blocks)
            
            # ファイルの保存
            await self.save_obsidian_file(obsidian_content)
            
        except Exception as e:
            print(f"Sync error: {e}")
    
    async def sync_obsidian_to_notion(self, file_path):
        """ObsidianからNotionへの同期"""
        try:
            # Obsidianファイルの読み取り
            obsidian_content = await self.read_obsidian_file(file_path)
            
            # Notionページへの変換
            notion_content = self.convert_to_notion(obsidian_content)
            
            # Notionページの作成/更新
            await self.create_or_update_notion_page(notion_content)
            
        except Exception as e:
            print(f"Sync error: {e}")
```

### 3. イベント管理

**ライブラリ**:
- **asyncio**: 非同期処理
- **queue**: イベントキュー
- **threading**: マルチスレッド処理

**実装例**:
```python
import asyncio
import queue
import threading
from datetime import datetime

class EventManager:
    def __init__(self):
        self.event_queue = queue.Queue()
        self.event_handlers = {}
        self.running = False
    
    def register_handler(self, event_type, handler):
        """イベントハンドラーの登録"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    def emit_event(self, event_type, event_data):
        """イベントの発生"""
        event = {
            'type': event_type,
            'data': event_data,
            'timestamp': datetime.now(),
            'id': self.generate_event_id()
        }
        
        self.event_queue.put(event)
    
    def start_event_loop(self):
        """イベントループの開始"""
        self.running = True
        
        while self.running:
            try:
                event = self.event_queue.get(timeout=1)
                self.process_event(event)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Event processing error: {e}")
    
    def process_event(self, event):
        """イベントの処理"""
        event_type = event['type']
        
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                try:
                    handler(event)
                except Exception as e:
                    print(f"Handler error: {e}")
    
    def stop_event_loop(self):
        """イベントループの停止"""
        self.running = False
    
    def generate_event_id(self):
        """イベントIDの生成"""
        return f"event_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
```

## 運用考慮事項

### 1. パフォーマンス

**最適化項目**:
- 同期処理の並列化
- キャッシュの活用
- 差分同期の実装

**監視項目**:
- 同期処理時間
- メモリ使用量
- CPU使用率

### 2. 信頼性

**考慮事項**:
- 同期の失敗処理
- データの整合性
- エラーの復旧

**対策**:
- リトライ機構の実装
- ログの記録
- バックアップの作成

### 3. セキュリティ

**考慮事項**:
- API キーの管理
- データの暗号化
- アクセス制御

**対策**:
- 環境変数での設定管理
- 通信の暗号化
- 権限の適切な設定
