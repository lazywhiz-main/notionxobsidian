"""
SyncCoordinatorのテスト
"""
import unittest
import sys
import os
import asyncio
from unittest.mock import Mock, AsyncMock

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sync_system.sync_coordinator import SyncCoordinator

class TestSyncCoordinator(unittest.TestCase):
    """SyncCoordinatorのテストクラス"""
    
    def setUp(self):
        """テストの前処理"""
        # モックオブジェクトの作成
        self.mock_notion_client = Mock()
        self.mock_obsidian_monitor = Mock()
        self.mock_analysis_engine = Mock()
        
        # SyncCoordinatorのインスタンス作成
        self.coordinator = SyncCoordinator(
            self.mock_notion_client,
            self.mock_obsidian_monitor,
            self.mock_analysis_engine
        )
    
    def test_coordinator_initialization(self):
        """コーディネーターの初期化テスト"""
        self.assertIsNotNone(self.coordinator.notion_client)
        self.assertIsNotNone(self.coordinator.obsidian_monitor)
        self.assertIsNotNone(self.coordinator.analysis_engine)
        self.assertFalse(self.coordinator.running)
        self.assertIsNotNone(self.coordinator.sync_queue)
        self.assertIsNotNone(self.coordinator.sync_status)
    
    def test_sync_status_initialization(self):
        """同期ステータスの初期化テスト"""
        status = self.coordinator.sync_status
        
        self.assertEqual(status['success_count'], 0)
        self.assertEqual(status['pending_count'], 0)
        self.assertEqual(status['error_count'], 0)
        self.assertIsNone(status['last_sync'])
    
    def test_convert_notion_to_obsidian(self):
        """NotionからObsidianへの変換テスト"""
        notion_content = {
            'title': 'Test Page',
            'content': 'This is a test page content.',
            'page': {
                'id': 'test_page_id',
                'created_time': '2024-01-01T00:00:00Z',
                'last_edited_time': '2024-01-01T00:00:00Z'
            }
        }
        
        result = self.coordinator._convert_notion_to_obsidian(notion_content)
        
        self.assertIsNotNone(result)
        self.assertIn('title', result)
        self.assertIn('content', result)
        self.assertIn('frontmatter', result)
        self.assertIn('metadata', result)
        
        self.assertEqual(result['title'], 'Test Page')
        self.assertIn('notion_id', result['frontmatter'])
        self.assertEqual(result['frontmatter']['notion_id'], 'test_page_id')
    
    def test_convert_obsidian_to_notion(self):
        """ObsidianからNotionへの変換テスト"""
        obsidian_content = """# Test Note

This is a test note content.

## Subsection

Some more content here."""
        
        file_path = "/test/path/Test Note.md"
        
        result = self.coordinator._convert_obsidian_to_notion(obsidian_content, file_path)
        
        self.assertIsNotNone(result)
        self.assertIn('title', result)
        self.assertIn('blocks', result)
        self.assertIn('properties', result)
        self.assertIn('metadata', result)
        
        self.assertEqual(result['title'], 'Test Note')
        self.assertIn('obsidian_id', result['metadata'])
        self.assertEqual(result['metadata']['obsidian_id'], file_path)
    
    def test_generate_obsidian_file_path(self):
        """Obsidianファイルパスの生成テスト"""
        obsidian_content = {
            'title': 'Test Note',
            'content': 'Test content',
            'frontmatter': {'notion_id': 'test_id'},
            'metadata': {'source': 'notion'}
        }
        
        file_path = self.coordinator._generate_obsidian_file_path(obsidian_content)
        
        self.assertIsNotNone(file_path)
        self.assertIn('Test Note.md', file_path)
        self.assertIn(self.coordinator.obsidian_monitor.vault_path, file_path)
    
    def test_convert_content_to_blocks(self):
        """コンテンツをNotionブロックに変換するテスト"""
        content = """# Heading 1

This is a paragraph.

## Heading 2

- List item 1
- List item 2

1. Numbered item 1
2. Numbered item 2"""
        
        blocks = self.coordinator._convert_content_to_blocks(content)
        
        self.assertIsInstance(blocks, list)
        self.assertGreater(len(blocks), 0)
        
        # ブロックタイプの確認
        block_types = [block['type'] for block in blocks]
        self.assertIn('heading_1', block_types)
        self.assertIn('paragraph', block_types)
        self.assertIn('heading_2', block_types)
        self.assertIn('bulleted_list_item', block_types)
        self.assertIn('numbered_list_item', block_types)
    
    def test_get_sync_status(self):
        """同期ステータスの取得テスト"""
        status = self.coordinator.get_sync_status()
        
        self.assertIsNotNone(status)
        self.assertIn('success_count', status)
        self.assertIn('pending_count', status)
        self.assertIn('error_count', status)
        self.assertIn('last_sync', status)
        
        # 初期値の確認
        self.assertEqual(status['success_count'], 0)
        self.assertEqual(status['pending_count'], 0)
        self.assertEqual(status['error_count'], 0)
        self.assertIsNone(status['last_sync'])
    
    def test_trigger_sync(self):
        """手動同期の実行テスト"""
        sync_data = {
            'page_id': 'test_page_id',
            'action': 'update'
        }
        
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                self.coordinator.trigger_sync('notion_to_obsidian', sync_data)
            )
            
            self.assertTrue(result)
            
            # キューに追加されたことを確認
            self.assertGreater(self.coordinator.sync_queue.qsize(), 0)
            
        finally:
            loop.close()
    
    def test_trigger_sync_invalid_type(self):
        """無効な同期タイプのテスト"""
        sync_data = {
            'page_id': 'test_page_id',
            'action': 'update'
        }
        
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                self.coordinator.trigger_sync('invalid_type', sync_data)
            )
            
            self.assertTrue(result)
            
        finally:
            loop.close()
    
    def test_handle_obsidian_change(self):
        """Obsidian変更の処理テスト"""
        change_event = {
            'type': 'obsidian_change',
            'file_path': '/test/path/test.md',
            'action': 'modified',
            'timestamp': '2024-01-01T00:00:00Z'
        }
        
        # 変更を処理
        self.coordinator._handle_obsidian_change(change_event)
        
        # キューに追加されたことを確認
        self.assertGreater(self.coordinator.sync_queue.qsize(), 0)
        self.assertEqual(self.coordinator.sync_status['pending_count'], 1)
    
    def test_handle_obsidian_change_created(self):
        """Obsidianファイル作成の処理テスト"""
        change_event = {
            'type': 'obsidian_change',
            'file_path': '/test/path/new_file.md',
            'action': 'created',
            'timestamp': '2024-01-01T00:00:00Z'
        }
        
        # 変更を処理
        self.coordinator._handle_obsidian_change(change_event)
        
        # キューに追加されたことを確認
        self.assertGreater(self.coordinator.sync_queue.qsize(), 0)
        self.assertEqual(self.coordinator.sync_status['pending_count'], 1)
    
    def test_handle_obsidian_change_deleted(self):
        """Obsidianファイル削除の処理テスト"""
        change_event = {
            'type': 'obsidian_change',
            'file_path': '/test/path/deleted_file.md',
            'action': 'deleted',
            'timestamp': '2024-01-01T00:00:00Z'
        }
        
        # 変更を処理
        self.coordinator._handle_obsidian_change(change_event)
        
        # キューに追加されたことを確認
        self.assertGreater(self.coordinator.sync_queue.qsize(), 0)
        self.assertEqual(self.coordinator.sync_status['pending_count'], 1)
    
    def test_handle_obsidian_change_moved(self):
        """Obsidianファイル移動の処理テスト"""
        change_event = {
            'type': 'obsidian_change',
            'file_path': '/test/path/old_file.md',
            'action': 'moved',
            'dest_path': '/test/path/new_file.md',
            'timestamp': '2024-01-01T00:00:00Z'
        }
        
        # 変更を処理
        self.coordinator._handle_obsidian_change(change_event)
        
        # キューに追加されたことを確認
        self.assertGreater(self.coordinator.sync_queue.qsize(), 0)
        self.assertEqual(self.coordinator.sync_status['pending_count'], 1)
    
    def test_add_to_sync_queue(self):
        """同期キューへの追加テスト"""
        sync_item = {
            'type': 'notion_to_obsidian',
            'page_id': 'test_page_id',
            'action': 'update'
        }
        
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(self.coordinator._add_to_sync_queue(sync_item))
            
            # キューに追加されたことを確認
            self.assertGreater(self.coordinator.sync_queue.qsize(), 0)
            self.assertEqual(self.coordinator.sync_status['pending_count'], 1)
            
        finally:
            loop.close()
    
    def test_get_sync_history(self):
        """同期履歴の取得テスト"""
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            history = loop.run_until_complete(self.coordinator.get_sync_history(limit=10))
            
            self.assertIsInstance(history, list)
            
        finally:
            loop.close()

if __name__ == '__main__':
    unittest.main()
