"""
統合テスト
"""
import unittest
import sys
import os
import asyncio
import tempfile
import shutil
from unittest.mock import Mock, patch

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import NotionObsidianSyncApp
from analysis_engine.analysis_engine import AnalysisEngine
from sync_system.sync_coordinator import SyncCoordinator
from sync_system.conflict_resolver import ConflictResolver
from sync_system.event_manager import EventManager

class TestIntegration(unittest.TestCase):
    """統合テストクラス"""
    
    def setUp(self):
        """テストの前処理"""
        # 一時ディレクトリを作成
        self.temp_dir = tempfile.mkdtemp()
        
        # モックオブジェクトを作成
        self.mock_notion_client = Mock()
        self.mock_obsidian_monitor = Mock()
        self.mock_analysis_engine = Mock()
        self.mock_sync_coordinator = Mock()
        
        # アプリケーションのインスタンスを作成
        self.app = NotionObsidianSyncApp()
        self.app.analysis_engine = self.mock_analysis_engine
        self.app.notion_client = self.mock_notion_client
        self.app.obsidian_monitor = self.mock_obsidian_monitor
        self.app.sync_coordinator = self.mock_sync_coordinator
    
    def tearDown(self):
        """テストの後処理"""
        # 一時ディレクトリを削除
        shutil.rmtree(self.temp_dir)
    
    def test_app_initialization(self):
        """アプリケーションの初期化テスト"""
        self.assertIsNotNone(self.app)
        self.assertIsNotNone(self.app.analysis_engine)
        self.assertIsNotNone(self.app.notion_client)
        self.assertIsNotNone(self.app.obsidian_monitor)
        self.assertIsNotNone(self.app.sync_coordinator)
    
    def test_analysis_engine_initialization(self):
        """分析エンジンの初期化テスト"""
        engine = AnalysisEngine()
        
        self.assertIsNotNone(engine.content_analyzer)
        self.assertIsNotNone(engine.insight_generator)
        self.assertIsNotNone(engine.recommendation_system)
        self.assertFalse(engine.running)
        self.assertIsNotNone(engine.analysis_queue)
        self.assertIsNotNone(engine.results_cache)
    
    def test_sync_coordinator_initialization(self):
        """同期コーディネーターの初期化テスト"""
        coordinator = SyncCoordinator(
            self.mock_notion_client,
            self.mock_obsidian_monitor,
            self.mock_analysis_engine
        )
        
        self.assertIsNotNone(coordinator.notion_client)
        self.assertIsNotNone(coordinator.obsidian_monitor)
        self.assertIsNotNone(coordinator.analysis_engine)
        self.assertFalse(coordinator.running)
        self.assertIsNotNone(coordinator.sync_queue)
        self.assertIsNotNone(coordinator.sync_status)
    
    def test_conflict_resolver_initialization(self):
        """競合解決器の初期化テスト"""
        resolver = ConflictResolver()
        
        self.assertIsNotNone(resolver.conflict_rules)
        self.assertIsNotNone(resolver.conflict_history)
        self.assertIsNotNone(resolver.priority_weights)
    
    def test_event_manager_initialization(self):
        """イベントマネージャーの初期化テスト"""
        manager = EventManager()
        
        self.assertIsNotNone(manager.event_queue)
        self.assertIsNotNone(manager.event_handlers)
        self.assertFalse(manager.running)
        self.assertIsNone(manager.event_thread)
        self.assertIsNotNone(manager.event_history)
        self.assertEqual(manager.max_history_size, 1000)
    
    def test_analysis_engine_content_analysis(self):
        """分析エンジンのコンテンツ分析テスト"""
        engine = AnalysisEngine()
        
        content_list = [
            {
                'id': 'content_1',
                'title': 'Test Content 1',
                'content': 'This is a test content for analysis.',
                'source': 'notion'
            },
            {
                'id': 'content_2',
                'title': 'Test Content 2',
                'content': 'This is another test content for analysis.',
                'source': 'obsidian'
            }
        ]
        
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(engine.analyze_content(content_list))
            
            self.assertIsNotNone(result)
            self.assertIn('analysis_id', result)
            self.assertIn('results', result)
            self.assertIn('summary', result)
            
            # 分析結果の確認
            results = result['results']
            self.assertIn('similarity', results)
            self.assertIn('duplicates', results)
            self.assertIn('topics', results)
            self.assertIn('sentiment', results)
            self.assertIn('readability', results)
            self.assertIn('insights', results)
            self.assertIn('recommendations', results)
            self.assertIn('action_items', results)
            
        finally:
            loop.close()
    
    def test_conflict_resolver_conflict_detection(self):
        """競合解決器の競合検出テスト"""
        resolver = ConflictResolver()
        
        notion_content = {
            'title': 'Notion Title',
            'content': 'Notion content',
            'last_edited_time': '2024-01-01T00:00:00Z'
        }
        
        obsidian_content = {
            'title': 'Obsidian Title',
            'content': 'Obsidian content',
            'modified_time': '2024-01-01T00:00:00Z'
        }
        
        conflicts = resolver.detect_conflict(notion_content, obsidian_content)
        
        self.assertIsInstance(conflicts, list)
        self.assertGreater(len(conflicts), 0)
        
        # タイトル競合が検出されることを確認
        title_conflicts = [c for c in conflicts if c['type'] == 'title_conflict']
        self.assertGreater(len(title_conflicts), 0)
        
        # コンテンツ競合が検出されることを確認
        content_conflicts = [c for c in conflicts if c['type'] == 'content_conflict']
        self.assertGreater(len(content_conflicts), 0)
    
    def test_conflict_resolver_conflict_resolution(self):
        """競合解決器の競合解決テスト"""
        resolver = ConflictResolver()
        
        conflict = {
            'type': 'title_conflict',
            'field': 'title',
            'notion_value': 'Notion Title',
            'obsidian_value': 'Obsidian Title',
            'notion_timestamp': '2024-01-01T00:00:00Z',
            'obsidian_timestamp': '2024-01-01T00:00:00Z',
            'severity': 'medium'
        }
        
        # Notion優先で解決
        resolution = resolver.resolve_conflict(conflict, 'notion_priority')
        
        self.assertIsNotNone(resolution)
        self.assertEqual(resolution['resolved_value'], 'Notion Title')
        self.assertEqual(resolution['resolution_reason'], 'Notion priority rule')
        self.assertFalse(resolution['requires_user_input'])
        
        # Obsidian優先で解決
        resolution = resolver.resolve_conflict(conflict, 'obsidian_priority')
        
        self.assertIsNotNone(resolution)
        self.assertEqual(resolution['resolved_value'], 'Obsidian Title')
        self.assertEqual(resolution['resolution_reason'], 'Obsidian priority rule')
        self.assertFalse(resolution['requires_user_input'])
        
        # ユーザー選択で解決
        resolution = resolver.resolve_conflict(conflict, 'user_choice')
        
        self.assertIsNotNone(resolution)
        self.assertIsNone(resolution['resolved_value'])
        self.assertTrue(resolution['requires_user_input'])
        self.assertIn('options', resolution)
        self.assertEqual(len(resolution['options']), 3)
    
    def test_event_manager_event_handling(self):
        """イベントマネージャーのイベント処理テスト"""
        manager = EventManager()
        
        # テストハンドラーを作成
        handler_called = False
        handler_data = None
        
        def test_handler(event):
            nonlocal handler_called, handler_data
            handler_called = True
            handler_data = event.data
        
        # ハンドラーを登録
        manager.register_handler('test_event', test_handler)
        
        # イベントを発生
        manager.emit_event('test_event', {'message': 'test'}, 'test_source', 1)
        
        # 少し待ってからハンドラーが呼ばれたかチェック
        import time
        time.sleep(0.1)
        
        self.assertTrue(handler_called)
        self.assertEqual(handler_data['message'], 'test')
    
    def test_event_manager_event_history(self):
        """イベントマネージャーのイベント履歴テスト"""
        manager = EventManager()
        
        # 複数のイベントを発生
        manager.emit_event('test_event_1', {'message': 'test1'}, 'test_source', 1)
        manager.emit_event('test_event_2', {'message': 'test2'}, 'test_source', 2)
        manager.emit_event('test_event_1', {'message': 'test3'}, 'test_source', 1)
        
        # 少し待ってから履歴をチェック
        import time
        time.sleep(0.1)
        
        # 全履歴を取得
        history = manager.get_event_history()
        self.assertGreaterEqual(len(history), 3)
        
        # 特定のタイプの履歴を取得
        test_event_1_history = manager.get_event_history('test_event_1')
        self.assertGreaterEqual(len(test_event_1_history), 2)
        
        # 統計を取得
        stats = manager.get_event_stats()
        self.assertIsNotNone(stats)
        self.assertIn('total_events', stats)
        self.assertIn('events_by_type', stats)
        self.assertIn('events_by_source', stats)
        self.assertIn('events_by_priority', stats)
    
    def test_sync_coordinator_data_conversion(self):
        """同期コーディネーターのデータ変換テスト"""
        coordinator = SyncCoordinator(
            self.mock_notion_client,
            self.mock_obsidian_monitor,
            self.mock_analysis_engine
        )
        
        # NotionからObsidianへの変換
        notion_content = {
            'title': 'Test Page',
            'content': 'This is a test page content.',
            'page': {
                'id': 'test_page_id',
                'created_time': '2024-01-01T00:00:00Z',
                'last_edited_time': '2024-01-01T00:00:00Z'
            }
        }
        
        obsidian_content = coordinator._convert_notion_to_obsidian(notion_content)
        
        self.assertIsNotNone(obsidian_content)
        self.assertIn('title', obsidian_content)
        self.assertIn('content', obsidian_content)
        self.assertIn('frontmatter', obsidian_content)
        self.assertIn('metadata', obsidian_content)
        
        self.assertEqual(obsidian_content['title'], 'Test Page')
        self.assertIn('notion_id', obsidian_content['frontmatter'])
        self.assertEqual(obsidian_content['frontmatter']['notion_id'], 'test_page_id')
        
        # ObsidianからNotionへの変換
        obsidian_content_text = """# Test Note

This is a test note content.

## Subsection

Some more content here."""
        
        file_path = "/test/path/Test Note.md"
        
        notion_content = coordinator._convert_obsidian_to_notion(obsidian_content_text, file_path)
        
        self.assertIsNotNone(notion_content)
        self.assertIn('title', notion_content)
        self.assertIn('blocks', notion_content)
        self.assertIn('properties', notion_content)
        self.assertIn('metadata', notion_content)
        
        self.assertEqual(notion_content['title'], 'Test Note')
        self.assertIn('obsidian_id', notion_content['metadata'])
        self.assertEqual(notion_content['metadata']['obsidian_id'], file_path)
    
    def test_sync_coordinator_content_to_blocks_conversion(self):
        """同期コーディネーターのコンテンツからブロックへの変換テスト"""
        coordinator = SyncCoordinator(
            self.mock_notion_client,
            self.mock_obsidian_monitor,
            self.mock_analysis_engine
        )
        
        content = """# Heading 1

This is a paragraph.

## Heading 2

- List item 1
- List item 2

1. Numbered item 1
2. Numbered item 2"""
        
        blocks = coordinator._convert_content_to_blocks(content)
        
        self.assertIsInstance(blocks, list)
        self.assertGreater(len(blocks), 0)
        
        # ブロックタイプの確認
        block_types = [block['type'] for block in blocks]
        self.assertIn('heading_1', block_types)
        self.assertIn('paragraph', block_types)
        self.assertIn('heading_2', block_types)
        self.assertIn('bulleted_list_item', block_types)
        self.assertIn('numbered_list_item', block_types)
    
    def test_sync_coordinator_sync_status(self):
        """同期コーディネーターの同期ステータステスト"""
        coordinator = SyncCoordinator(
            self.mock_notion_client,
            self.mock_obsidian_monitor,
            self.mock_analysis_engine
        )
        
        status = coordinator.get_sync_status()
        
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

if __name__ == '__main__':
    unittest.main()
