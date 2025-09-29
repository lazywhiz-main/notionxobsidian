"""
同期コーディネーター
NotionとObsidian間の同期を管理する
"""
import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class SyncCoordinator:
    """同期コーディネータークラス"""
    
    def __init__(self, notion_client, obsidian_monitor, analysis_engine):
        self.notion_client = notion_client
        self.obsidian_monitor = obsidian_monitor
        self.analysis_engine = analysis_engine
        self.running = False
        self.sync_queue = asyncio.Queue()
        self.sync_status = {
            'success_count': 0,
            'pending_count': 0,
            'error_count': 0,
            'last_sync': None
        }
    
    async def initialize(self):
        """同期コーディネーターの初期化"""
        try:
            logger.info("Initializing sync coordinator...")
            
            # 変更コールバックの設定
            self.obsidian_monitor.set_change_callback(self._handle_obsidian_change)
            
            logger.info("Sync coordinator initialized successfully")
            
        except Exception as e:
            logger.error(f"Sync coordinator initialization failed: {e}")
            raise
    
    async def start(self):
        """同期コーディネーターの開始"""
        try:
            logger.info("Starting sync coordinator...")
            self.running = True
            
            # 同期処理のタスクを開始
            sync_task = asyncio.create_task(self._process_sync_queue())
            
            # タスクの実行
            await sync_task
            
        except Exception as e:
            logger.error(f"Sync coordinator start failed: {e}")
            raise
    
    async def stop(self):
        """同期コーディネーターの停止"""
        logger.info("Stopping sync coordinator...")
        self.running = False
    
    async def _process_sync_queue(self):
        """同期キューの処理"""
        while self.running:
            try:
                # キューから同期タスクを取得
                sync_item = await asyncio.wait_for(
                    self.sync_queue.get(), 
                    timeout=1.0
                )
                
                # 同期を実行
                await self._execute_sync(sync_item)
                
            except asyncio.TimeoutError:
                # タイムアウトは正常（キューが空）
                continue
            except Exception as e:
                logger.error(f"Sync queue processing failed: {e}")
                self.sync_status['error_count'] += 1
    
    async def _execute_sync(self, sync_item: Dict[str, Any]):
        """同期の実行"""
        try:
            sync_type = sync_item.get('type')
            
            if sync_type == 'notion_to_obsidian':
                await self._sync_notion_to_obsidian(sync_item)
            elif sync_type == 'obsidian_to_notion':
                await self._sync_obsidian_to_notion(sync_item)
            elif sync_type == 'bidirectional':
                await self._sync_bidirectional(sync_item)
            else:
                logger.warning(f"Unknown sync type: {sync_type}")
                return
            
            # 同期ステータスを更新
            self.sync_status['success_count'] += 1
            self.sync_status['last_sync'] = datetime.now().isoformat()
            
            logger.info(f"Sync completed successfully: {sync_type}")
            
        except Exception as e:
            logger.error(f"Sync execution failed: {e}")
            self.sync_status['error_count'] += 1
    
    async def _sync_notion_to_obsidian(self, sync_item: Dict[str, Any]):
        """NotionからObsidianへの同期"""
        try:
            page_id = sync_item.get('page_id')
            if not page_id:
                logger.error("Page ID not provided for Notion to Obsidian sync")
                return
            
            # Notionページの内容を取得
            notion_content = await self.notion_client.get_page_content(page_id)
            if not notion_content:
                logger.error(f"Failed to get Notion page content: {page_id}")
                return
            
            # Obsidianファイルに変換
            obsidian_content = self._convert_notion_to_obsidian(notion_content)
            
            # Obsidianファイルに保存
            file_path = self._generate_obsidian_file_path(obsidian_content)
            success = await self.obsidian_monitor.write_file_content(file_path, obsidian_content['content'])
            
            if success:
                logger.info(f"Notion page synced to Obsidian: {file_path}")
            else:
                logger.error(f"Failed to write Obsidian file: {file_path}")
                
        except Exception as e:
            logger.error(f"Notion to Obsidian sync failed: {e}")
            raise
    
    async def _sync_obsidian_to_notion(self, sync_item: Dict[str, Any]):
        """ObsidianからNotionへの同期"""
        try:
            file_path = sync_item.get('file_path')
            if not file_path:
                logger.error("File path not provided for Obsidian to Notion sync")
                return
            
            # Obsidianファイルの内容を取得
            obsidian_content = await self.obsidian_monitor.get_file_content(file_path)
            if not obsidian_content:
                logger.error(f"Failed to get Obsidian file content: {file_path}")
                return
            
            # Notionページに変換
            notion_content = self._convert_obsidian_to_notion(obsidian_content, file_path)
            
            # Notionページを作成/更新
            page_id = await self._create_or_update_notion_page(notion_content)
            
            if page_id:
                logger.info(f"Obsidian file synced to Notion: {page_id}")
            else:
                logger.error(f"Failed to create/update Notion page")
                
        except Exception as e:
            logger.error(f"Obsidian to Notion sync failed: {e}")
            raise
    
    async def _sync_bidirectional(self, sync_item: Dict[str, Any]):
        """双方向同期"""
        try:
            # 両方向の同期を実行
            await self._sync_notion_to_obsidian(sync_item)
            await self._sync_obsidian_to_notion(sync_item)
            
            logger.info("Bidirectional sync completed")
            
        except Exception as e:
            logger.error(f"Bidirectional sync failed: {e}")
            raise
    
    def _handle_obsidian_change(self, change_event: Dict[str, Any]):
        """Obsidianの変更を処理"""
        try:
            # 同期タスクをキューに追加
            sync_item = {
                'type': 'obsidian_to_notion',
                'file_path': change_event['file_path'],
                'action': change_event['action'],
                'timestamp': change_event['timestamp']
            }
            
            asyncio.create_task(self._add_to_sync_queue(sync_item))
            
        except Exception as e:
            logger.error(f"Obsidian change handling failed: {e}")
    
    async def _add_to_sync_queue(self, sync_item: Dict[str, Any]):
        """同期キューにアイテムを追加"""
        try:
            await self.sync_queue.put(sync_item)
            self.sync_status['pending_count'] += 1
            
        except Exception as e:
            logger.error(f"Failed to add to sync queue: {e}")
    
    def _convert_notion_to_obsidian(self, notion_content: Dict[str, Any]) -> Dict[str, Any]:
        """NotionからObsidianへの変換"""
        try:
            # 基本的な変換（実際の実装では、DataTransformerを使用）
            title = notion_content.get('title', 'Untitled')
            content = notion_content.get('content', '')
            
            # フロントマターの作成
            frontmatter = f"""---
notion_id: {notion_content.get('page', {}).get('id', '')}
created_time: {notion_content.get('page', {}).get('created_time', '')}
last_edited_time: {notion_content.get('page', {}).get('last_edited_time', '')}
source: notion
---

# {title}

{content}"""
            
            return {
                'title': title,
                'content': frontmatter,
                'frontmatter': {
                    'notion_id': notion_content.get('page', {}).get('id', ''),
                    'source': 'notion'
                }
            }
            
        except Exception as e:
            logger.error(f"Notion to Obsidian conversion failed: {e}")
            return {}
    
    def _convert_obsidian_to_notion(self, obsidian_content: str, file_path: str) -> Dict[str, Any]:
        """ObsidianからNotionへの変換"""
        try:
            # ファイル名からタイトルを抽出
            file_name = Path(file_path).stem
            
            # フロントマターを除去
            content_lines = obsidian_content.split('\n')
            if content_lines[0] == '---':
                # フロントマターをスキップ
                end_index = content_lines.index('---', 1)
                content = '\n'.join(content_lines[end_index + 1:])
            else:
                content = obsidian_content
            
            # 見出しを除去
            content_without_title = content
            if content.startswith('# '):
                content_without_title = content[2:].strip()
            
            return {
                'title': file_name,
                'content': content_without_title,
                'properties': {
                    'title': {'title': [{'text': {'content': file_name}}]},
                    'obsidian_id': file_path,
                    'source': 'obsidian'
                }
            }
            
        except Exception as e:
            logger.error(f"Obsidian to Notion conversion failed: {e}")
            return {}
    
    def _generate_obsidian_file_path(self, obsidian_content: Dict[str, Any]) -> str:
        """Obsidianファイルパスを生成"""
        try:
            title = obsidian_content.get('title', 'Untitled')
            
            # ファイル名に使用できない文字を置換
            safe_title = title.replace('/', '_').replace('\\', '_').replace(':', '_')
            
            # ファイルパスを生成
            file_path = f"{self.obsidian_monitor.vault_path}/{safe_title}.md"
            
            return file_path
            
        except Exception as e:
            logger.error(f"Obsidian file path generation failed: {e}")
            return f"{self.obsidian_monitor.vault_path}/Untitled.md"
    
    async def _create_or_update_notion_page(self, notion_content: Dict[str, Any]) -> Optional[str]:
        """Notionページを作成/更新"""
        try:
            # 既存のページを検索
            existing_page = await self._find_existing_notion_page(notion_content)
            
            if existing_page:
                # 既存ページを更新
                page_id = await self._update_notion_page(existing_page['id'], notion_content)
            else:
                # 新しいページを作成
                page_id = await self._create_notion_page(notion_content)
            
            return page_id
            
        except Exception as e:
            logger.error(f"Notion page creation/update failed: {e}")
            return None
    
    async def _find_existing_notion_page(self, notion_content: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """既存のNotionページを検索"""
        try:
            obsidian_id = notion_content.get('properties', {}).get('obsidian_id')
            if not obsidian_id:
                return None
            
            # Obsidian IDでページを検索
            pages = await self.notion_client.get_pages()
            for page in pages:
                properties = page.get('properties', {})
                page_obsidian_id = properties.get('Obsidian ID', {}).get('rich_text', [{}])[0].get('text', {}).get('content')
                
                if page_obsidian_id == obsidian_id:
                    return page
            
            return None
            
        except Exception as e:
            logger.error(f"Existing Notion page search failed: {e}")
            return None
    
    async def _create_notion_page(self, notion_content: Dict[str, Any]) -> Optional[str]:
        """新しいNotionページを作成"""
        try:
            # ページデータを準備
            page_data = {
                'parent': {'type': 'page_id', 'page_id': 'parent_page_id'},  # 実際の親ページIDに置き換え
                'properties': notion_content.get('properties', {}),
                'children': self._convert_content_to_blocks(notion_content.get('content', ''))
            }
            
            # ページを作成
            result = self.notion_client.client.pages.create(**page_data)
            return result['id']
            
        except Exception as e:
            logger.error(f"Notion page creation failed: {e}")
            return None
    
    async def _update_notion_page(self, page_id: str, notion_content: Dict[str, Any]) -> Optional[str]:
        """既存のNotionページを更新"""
        try:
            # ページのプロパティを更新
            page_data = {
                'properties': notion_content.get('properties', {})
            }
            
            self.notion_client.client.pages.update(page_id=page_id, **page_data)
            
            # ページの内容を更新
            blocks = self._convert_content_to_blocks(notion_content.get('content', ''))
            self.notion_client.client.blocks.children.append(
                block_id=page_id,
                children=blocks
            )
            
            return page_id
            
        except Exception as e:
            logger.error(f"Notion page update failed: {e}")
            return None
    
    def _convert_content_to_blocks(self, content: str) -> List[Dict[str, Any]]:
        """コンテンツをNotionブロックに変換"""
        try:
            blocks = []
            lines = content.split('\n')
            
            for line in lines:
                if not line.strip():
                    continue
                
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
                else:
                    blocks.append({
                        'type': 'paragraph',
                        'paragraph': {'rich_text': [{'text': {'content': line}}]}
                    })
            
            return blocks
            
        except Exception as e:
            logger.error(f"Content to blocks conversion failed: {e}")
            return []
    
    async def trigger_sync(self, sync_type: str, sync_data: Dict[str, Any]) -> bool:
        """手動同期の実行"""
        try:
            sync_item = {
                'type': sync_type,
                **sync_data
            }
            
            await self._add_to_sync_queue(sync_item)
            logger.info(f"Manual sync triggered: {sync_type}")
            return True
            
        except Exception as e:
            logger.error(f"Manual sync trigger failed: {e}")
            return False
    
    def get_sync_status(self) -> Dict[str, Any]:
        """同期ステータスを取得"""
        return self.sync_status.copy()
    
    async def get_sync_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """同期履歴を取得"""
        try:
            # 実際の実装では、データベースから履歴を取得
            return []
            
        except Exception as e:
            logger.error(f"Sync history retrieval failed: {e}")
            return []
