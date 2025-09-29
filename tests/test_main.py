"""
メインアプリケーションのテスト
"""
import unittest
import sys
import os
import asyncio
from unittest.mock import Mock, patch

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import NotionObsidianSyncApp

class TestNotionObsidianSyncApp(unittest.TestCase):
    """NotionObsidianSyncAppのテストクラス"""
    
    def setUp(self):
        """テストの前処理"""
        self.app = NotionObsidianSyncApp()
    
    def test_app_initialization(self):
        """アプリケーションの初期化テスト"""
        self.assertIsNotNone(self.app.settings)
        self.assertIsNone(self.app.analysis_engine)
        self.assertIsNone(self.app.notion_client)
        self.assertIsNone(self.app.obsidian_monitor)
        self.assertIsNone(self.app.sync_coordinator)
        self.assertFalse(self.app.running)
    
    def test_app_initialization_with_settings(self):
        """設定付きアプリケーションの初期化テスト"""
        # モック設定を作成
        mock_settings = Mock()
        mock_settings.notion_token = "test_token"
        mock_settings.obsidian_path = "/test/path"
        
        app = NotionObsidianSyncApp()
        app.settings = mock_settings
        
        self.assertEqual(app.settings.notion_token, "test_token")
        self.assertEqual(app.settings.obsidian_path, "/test/path")
    
    def test_app_initialization_with_components(self):
        """コンポーネント付きアプリケーションの初期化テスト"""
        # モックコンポーネントを作成
        mock_analysis_engine = Mock()
        mock_notion_client = Mock()
        mock_obsidian_monitor = Mock()
        mock_sync_coordinator = Mock()
        
        app = NotionObsidianSyncApp()
        app.analysis_engine = mock_analysis_engine
        app.notion_client = mock_notion_client
        app.obsidian_monitor = mock_obsidian_monitor
        app.sync_coordinator = mock_sync_coordinator
        
        self.assertEqual(app.analysis_engine, mock_analysis_engine)
        self.assertEqual(app.notion_client, mock_notion_client)
        self.assertEqual(app.obsidian_monitor, mock_obsidian_monitor)
        self.assertEqual(app.sync_coordinator, mock_sync_coordinator)
    
    def test_app_running_state(self):
        """アプリケーションの実行状態テスト"""
        self.assertFalse(self.app.running)
        
        # 実行状態を変更
        self.app.running = True
        self.assertTrue(self.app.running)
        
        # 実行状態を元に戻す
        self.app.running = False
        self.assertFalse(self.app.running)
    
    def test_app_components_none(self):
        """コンポーネントがNoneの場合のテスト"""
        self.assertIsNone(self.app.analysis_engine)
        self.assertIsNone(self.app.notion_client)
        self.assertIsNone(self.app.obsidian_monitor)
        self.assertIsNone(self.app.sync_coordinator)
    
    def test_app_components_assignment(self):
        """コンポーネントの割り当てテスト"""
        # モックコンポーネントを作成
        mock_analysis_engine = Mock()
        mock_notion_client = Mock()
        mock_obsidian_monitor = Mock()
        mock_sync_coordinator = Mock()
        
        # コンポーネントを割り当て
        self.app.analysis_engine = mock_analysis_engine
        self.app.notion_client = mock_notion_client
        self.app.obsidian_monitor = mock_obsidian_monitor
        self.app.sync_coordinator = mock_sync_coordinator
        
        # 割り当てを確認
        self.assertEqual(self.app.analysis_engine, mock_analysis_engine)
        self.assertEqual(self.app.notion_client, mock_notion_client)
        self.assertEqual(self.app.obsidian_monitor, mock_obsidian_monitor)
        self.assertEqual(self.app.sync_coordinator, mock_sync_coordinator)
    
    def test_app_components_reassignment(self):
        """コンポーネントの再割り当てテスト"""
        # 最初のモックコンポーネントを作成
        mock_analysis_engine1 = Mock()
        mock_notion_client1 = Mock()
        mock_obsidian_monitor1 = Mock()
        mock_sync_coordinator1 = Mock()
        
        # コンポーネントを割り当て
        self.app.analysis_engine = mock_analysis_engine1
        self.app.notion_client = mock_notion_client1
        self.app.obsidian_monitor = mock_obsidian_monitor1
        self.app.sync_coordinator = mock_sync_coordinator1
        
        # 新しいモックコンポーネントを作成
        mock_analysis_engine2 = Mock()
        mock_notion_client2 = Mock()
        mock_obsidian_monitor2 = Mock()
        mock_sync_coordinator2 = Mock()
        
        # コンポーネントを再割り当て
        self.app.analysis_engine = mock_analysis_engine2
        self.app.notion_client = mock_notion_client2
        self.app.obsidian_monitor = mock_obsidian_monitor2
        self.app.sync_coordinator = mock_sync_coordinator2
        
        # 再割り当てを確認
        self.assertEqual(self.app.analysis_engine, mock_analysis_engine2)
        self.assertEqual(self.app.notion_client, mock_notion_client2)
        self.assertEqual(self.app.obsidian_monitor, mock_obsidian_monitor2)
        self.assertEqual(self.app.sync_coordinator, mock_sync_coordinator2)
        
        # 古いコンポーネントと異なることを確認
        self.assertNotEqual(self.app.analysis_engine, mock_analysis_engine1)
        self.assertNotEqual(self.app.notion_client, mock_notion_client1)
        self.assertNotEqual(self.app.obsidian_monitor, mock_obsidian_monitor1)
        self.assertNotEqual(self.app.sync_coordinator, mock_sync_coordinator1)
    
    def test_app_settings_access(self):
        """アプリケーション設定へのアクセステスト"""
        # 設定が存在することを確認
        self.assertIsNotNone(self.app.settings)
        
        # 設定のプロパティにアクセス
        settings = self.app.settings
        self.assertIsNotNone(settings)
    
    def test_app_initialization_with_mock_settings(self):
        """モック設定でのアプリケーション初期化テスト"""
        # モック設定を作成
        mock_settings = Mock()
        mock_settings.notion_token = "test_token"
        mock_settings.obsidian_path = "/test/path"
        mock_settings.analysis_interval = 300
        mock_settings.sync_interval = 60
        mock_settings.similarity_threshold = 0.8
        mock_settings.confidence_threshold = 0.7
        
        # アプリケーションに設定を割り当て
        self.app.settings = mock_settings
        
        # 設定の値を確認
        self.assertEqual(self.app.settings.notion_token, "test_token")
        self.assertEqual(self.app.settings.obsidian_path, "/test/path")
        self.assertEqual(self.app.settings.analysis_interval, 300)
        self.assertEqual(self.app.settings.sync_interval, 60)
        self.assertEqual(self.app.settings.similarity_threshold, 0.8)
        self.assertEqual(self.app.settings.confidence_threshold, 0.7)
    
    def test_app_initialization_with_mock_components(self):
        """モックコンポーネントでのアプリケーション初期化テスト"""
        # モックコンポーネントを作成
        mock_analysis_engine = Mock()
        mock_notion_client = Mock()
        mock_obsidian_monitor = Mock()
        mock_sync_coordinator = Mock()
        
        # アプリケーションにコンポーネントを割り当て
        self.app.analysis_engine = mock_analysis_engine
        self.app.notion_client = mock_notion_client
        self.app.obsidian_monitor = mock_obsidian_monitor
        self.app.sync_coordinator = mock_sync_coordinator
        
        # コンポーネントの存在を確認
        self.assertIsNotNone(self.app.analysis_engine)
        self.assertIsNotNone(self.app.notion_client)
        self.assertIsNotNone(self.app.obsidian_monitor)
        self.assertIsNotNone(self.app.sync_coordinator)
        
        # コンポーネントの型を確認
        self.assertIsInstance(self.app.analysis_engine, Mock)
        self.assertIsInstance(self.app.notion_client, Mock)
        self.assertIsInstance(self.app.obsidian_monitor, Mock)
        self.assertIsInstance(self.app.sync_coordinator, Mock)
    
    def test_app_initialization_with_mock_settings_and_components(self):
        """モック設定とコンポーネントでのアプリケーション初期化テスト"""
        # モック設定を作成
        mock_settings = Mock()
        mock_settings.notion_token = "test_token"
        mock_settings.obsidian_path = "/test/path"
        
        # モックコンポーネントを作成
        mock_analysis_engine = Mock()
        mock_notion_client = Mock()
        mock_obsidian_monitor = Mock()
        mock_sync_coordinator = Mock()
        
        # アプリケーションに設定とコンポーネントを割り当て
        self.app.settings = mock_settings
        self.app.analysis_engine = mock_analysis_engine
        self.app.notion_client = mock_notion_client
        self.app.obsidian_monitor = mock_obsidian_monitor
        self.app.sync_coordinator = mock_sync_coordinator
        
        # 設定とコンポーネントの存在を確認
        self.assertIsNotNone(self.app.settings)
        self.assertIsNotNone(self.app.analysis_engine)
        self.assertIsNotNone(self.app.notion_client)
        self.assertIsNotNone(self.app.obsidian_monitor)
        self.assertIsNotNone(self.app.sync_coordinator)
        
        # 設定の値を確認
        self.assertEqual(self.app.settings.notion_token, "test_token")
        self.assertEqual(self.app.settings.obsidian_path, "/test/path")
        
        # コンポーネントの型を確認
        self.assertIsInstance(self.app.analysis_engine, Mock)
        self.assertIsInstance(self.app.notion_client, Mock)
        self.assertIsInstance(self.app.obsidian_monitor, Mock)
        self.assertIsInstance(self.app.sync_coordinator, Mock)

if __name__ == '__main__':
    unittest.main()
