"""
Obsidian ファイルモニター
Obsidianファイルシステムの監視を行う
"""
import logging
import os
import time
import asyncio
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path
from datetime import datetime

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    logging.warning("watchdog not available")

logger = logging.getLogger(__name__)

class ObsidianFileHandler(FileSystemEventHandler):
    """Obsidianファイル変更ハンドラー"""
    
    def __init__(self, vault_path: str, change_callback: Optional[Callable] = None):
        self.vault_path = vault_path
        self.change_callback = change_callback
        self.last_modified = {}
    
    def on_modified(self, event):
        """ファイル変更時の処理"""
        if event.is_directory:
            return
        
        if event.src_path.endswith('.md'):
            self._handle_file_change(event.src_path, 'modified')
    
    def on_created(self, event):
        """ファイル作成時の処理"""
        if event.is_directory:
            return
        
        if event.src_path.endswith('.md'):
            self._handle_file_change(event.src_path, 'created')
    
    def on_deleted(self, event):
        """ファイル削除時の処理"""
        if event.is_directory:
            return
        
        if event.src_path.endswith('.md'):
            self._handle_file_change(event.src_path, 'deleted')
    
    def on_moved(self, event):
        """ファイル移動時の処理"""
        if event.is_directory:
            return
        
        if event.src_path.endswith('.md'):
            self._handle_file_change(event.src_path, 'moved', event.dest_path)
    
    def _handle_file_change(self, file_path: str, action: str, dest_path: str = None):
        """ファイル変更の処理"""
        try:
            # 重複イベントを防ぐため、最後の変更時刻をチェック
            current_time = time.time()
            if file_path in self.last_modified:
                if current_time - self.last_modified[file_path] < 1.0:  # 1秒以内の重複を無視
                    return
            
            self.last_modified[file_path] = current_time
            
            # 変更イベントを作成
            change_event = {
                'type': 'obsidian_change',
                'file_path': file_path,
                'action': action,
                'dest_path': dest_path,
                'timestamp': datetime.now().isoformat()
            }
            
            # コールバック関数を呼び出し
            if self.change_callback:
                self.change_callback(change_event)
            
            logger.info(f"Obsidian file {action}: {file_path}")
            
        except Exception as e:
            logger.error(f"File change handling failed: {e}")

class ObsidianFileMonitor:
    """Obsidianファイルモニタークラス"""
    
    def __init__(self, vault_path: str):
        self.vault_path = vault_path
        self.observer = None
        self.event_handler = None
        self.running = False
        self.change_callback = None
        self.file_cache = {}
    
    async def initialize(self):
        """ファイルモニターの初期化"""
        try:
            logger.info(f"Initializing Obsidian file monitor for: {self.vault_path}")
            
            # ボルトパスの存在確認
            if not os.path.exists(self.vault_path):
                raise ValueError(f"Obsidian vault path does not exist: {self.vault_path}")
            
            # ファイルキャッシュの初期化
            await self._initialize_file_cache()
            
            # イベントハンドラーの初期化
            self.event_handler = ObsidianFileHandler(
                self.vault_path,
                self._handle_file_change
            )
            
            # オブザーバーの初期化
            self.observer = Observer()
            self.observer.schedule(
                self.event_handler,
                self.vault_path,
                recursive=True
            )
            
            logger.info("Obsidian file monitor initialized successfully")
            
        except Exception as e:
            logger.error(f"File monitor initialization failed: {e}")
            raise
    
    async def start(self):
        """ファイルモニターの開始"""
        try:
            logger.info("Starting Obsidian file monitor...")
            self.running = True
            
            # オブザーバーの開始
            self.observer.start()
            
            # 監視タスクの開始
            monitor_task = asyncio.create_task(self._monitor_loop())
            
            # タスクの実行
            await monitor_task
            
        except Exception as e:
            logger.error(f"File monitor start failed: {e}")
            raise
    
    async def stop(self):
        """ファイルモニターの停止"""
        logger.info("Stopping Obsidian file monitor...")
        self.running = False
        
        if self.observer:
            self.observer.stop()
            self.observer.join()
    
    def set_change_callback(self, callback: Callable):
        """変更コールバックの設定"""
        self.change_callback = callback
    
    async def _initialize_file_cache(self):
        """ファイルキャッシュの初期化"""
        try:
            vault_path = Path(self.vault_path)
            
            for md_file in vault_path.rglob("*.md"):
                file_info = await self._get_file_info(md_file)
                if file_info:
                    self.file_cache[str(md_file)] = file_info
            
            logger.info(f"Initialized file cache with {len(self.file_cache)} files")
            
        except Exception as e:
            logger.error(f"File cache initialization failed: {e}")
    
    async def _get_file_info(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """ファイル情報の取得"""
        try:
            if not file_path.exists():
                return None
            
            stat = file_path.stat()
            
            return {
                'path': str(file_path),
                'name': file_path.name,
                'size': stat.st_size,
                'created_time': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified_time': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'relative_path': str(file_path.relative_to(Path(self.vault_path)))
            }
            
        except Exception as e:
            logger.error(f"File info retrieval failed: {e}")
            return None
    
    async def _monitor_loop(self):
        """監視ループ"""
        while self.running:
            try:
                # 定期的なファイルキャッシュの更新
                await self._update_file_cache()
                
                # 1分間隔でチェック
                await asyncio.sleep(60)
                
            except Exception as e:
                logger.error(f"Monitor loop failed: {e}")
                await asyncio.sleep(60)
    
    async def _update_file_cache(self):
        """ファイルキャッシュの更新"""
        try:
            vault_path = Path(self.vault_path)
            current_files = set()
            
            # 現在のファイルをスキャン
            for md_file in vault_path.rglob("*.md"):
                file_path = str(md_file)
                current_files.add(file_path)
                
                # 新しいファイルまたは変更されたファイルをチェック
                if file_path not in self.file_cache:
                    file_info = await self._get_file_info(md_file)
                    if file_info:
                        self.file_cache[file_path] = file_info
                        logger.info(f"New file detected: {file_path}")
                else:
                    # 既存ファイルの変更をチェック
                    current_info = await self._get_file_info(md_file)
                    cached_info = self.file_cache[file_path]
                    
                    if current_info and current_info['modified_time'] != cached_info['modified_time']:
                        self.file_cache[file_path] = current_info
                        logger.info(f"File modified: {file_path}")
            
            # 削除されたファイルをチェック
            deleted_files = set(self.file_cache.keys()) - current_files
            for deleted_file in deleted_files:
                del self.file_cache[deleted_file]
                logger.info(f"File deleted: {deleted_file}")
            
        except Exception as e:
            logger.error(f"File cache update failed: {e}")
    
    def _handle_file_change(self, change_event: Dict[str, Any]):
        """ファイル変更の処理"""
        try:
            # 変更コールバックを呼び出し
            if self.change_callback:
                self.change_callback(change_event)
            
            # ファイルキャッシュを更新
            file_path = change_event['file_path']
            action = change_event['action']
            
            if action == 'created' or action == 'modified':
                # ファイル情報を更新
                file_path_obj = Path(file_path)
                if file_path_obj.exists():
                    asyncio.create_task(self._update_file_info(file_path))
            elif action == 'deleted':
                # ファイルをキャッシュから削除
                if file_path in self.file_cache:
                    del self.file_cache[file_path]
            elif action == 'moved':
                # ファイルの移動を処理
                old_path = file_path
                new_path = change_event['dest_path']
                
                if old_path in self.file_cache:
                    file_info = self.file_cache[old_path]
                    file_info['path'] = new_path
                    self.file_cache[new_path] = file_info
                    del self.file_cache[old_path]
            
        except Exception as e:
            logger.error(f"File change handling failed: {e}")
    
    async def _update_file_info(self, file_path: str):
        """ファイル情報の更新"""
        try:
            file_path_obj = Path(file_path)
            file_info = await self._get_file_info(file_path_obj)
            if file_info:
                self.file_cache[file_path] = file_info
            
        except Exception as e:
            logger.error(f"File info update failed: {e}")
    
    async def get_file_content(self, file_path: str) -> Optional[str]:
        """ファイルの内容を取得"""
        try:
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                return None
            
            with open(file_path_obj, 'r', encoding='utf-8') as f:
                return f.read()
                
        except Exception as e:
            logger.error(f"File content retrieval failed: {e}")
            return None
    
    async def write_file_content(self, file_path: str, content: str) -> bool:
        """ファイルに内容を書き込み"""
        try:
            file_path_obj = Path(file_path)
            
            # ディレクトリが存在しない場合は作成
            file_path_obj.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path_obj, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # ファイルキャッシュを更新
            file_info = await self._get_file_info(file_path_obj)
            if file_info:
                self.file_cache[file_path] = file_info
            
            logger.info(f"File content written: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"File content writing failed: {e}")
            return False
    
    async def get_all_markdown_files(self) -> List[Dict[str, Any]]:
        """すべてのMarkdownファイルを取得"""
        try:
            files = []
            vault_path = Path(self.vault_path)
            
            for md_file in vault_path.rglob("*.md"):
                file_info = await self._get_file_info(md_file)
                if file_info:
                    files.append(file_info)
            
            return files
            
        except Exception as e:
            logger.error(f"Markdown files retrieval failed: {e}")
            return []
    
    async def search_files(self, query: str) -> List[Dict[str, Any]]:
        """ファイルの検索"""
        try:
            matching_files = []
            vault_path = Path(self.vault_path)
            
            for md_file in vault_path.rglob("*.md"):
                if query.lower() in md_file.name.lower():
                    file_info = await self._get_file_info(md_file)
                    if file_info:
                        matching_files.append(file_info)
            
            return matching_files
            
        except Exception as e:
            logger.error(f"File search failed: {e}")
            return []
    
    def get_file_cache(self) -> Dict[str, Any]:
        """ファイルキャッシュを取得"""
        return self.file_cache.copy()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """キャッシュ統計を取得"""
        try:
            total_files = len(self.file_cache)
            total_size = sum(file_info.get('size', 0) for file_info in self.file_cache.values())
            
            return {
                'total_files': total_files,
                'total_size': total_size,
                'average_size': total_size / total_files if total_files > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Cache stats calculation failed: {e}")
            return {'total_files': 0, 'total_size': 0, 'average_size': 0}
