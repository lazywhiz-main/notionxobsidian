"""
基本的なテスト
"""
import unittest
import sys
import os

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import Settings, settings

class TestBasic(unittest.TestCase):
    """基本的なテストクラス"""
    
    def test_settings_loading(self):
        """設定の読み込みテスト"""
        # 設定オブジェクトが正しく作成されることを確認
        self.assertIsInstance(settings, Settings)
        
        # 設定値が文字列型であることを確認
        self.assertIsInstance(settings.NOTION_API_KEY, str)
        self.assertIsInstance(settings.NOTION_DATABASE_ID, str)
        self.assertIsInstance(settings.OBSIDIAN_VAULT_PATH, str)
        self.assertIsInstance(settings.OPENAI_API_KEY, str)
        self.assertIsInstance(settings.ANTHROPIC_API_KEY, str)
    
    def test_imports(self):
        """インポートテスト"""
        # 各モジュールが正しくインポートできることを確認
        try:
            from analysis_engine.content_analyzer import ContentAnalyzer
            from analysis_engine.insight_generator import InsightGenerator
            from analysis_engine.recommendation_system import RecommendationSystem
            from analysis_engine.analysis_engine import AnalysisEngine
            from notion_integration.notion_client import NotionClient
            from notion_integration.data_transformer import NotionDataTransformer
            from notion_integration.dashboard_builder import NotionDashboardBuilder
            from obsidian_integration.file_monitor import ObsidianFileMonitor
            from obsidian_integration.markdown_parser import MarkdownParser
            from obsidian_integration.dashboard_builder import ObsidianDashboardBuilder
            from sync_system.sync_coordinator import SyncCoordinator
            from sync_system.conflict_resolver import ConflictResolver
            from sync_system.data_transformer import SyncDataTransformer
            from sync_system.event_manager import EventManager
        except ImportError as e:
            self.fail(f"Import failed: {e}")
    
    def test_main_app(self):
        """メインアプリケーションのテスト"""
        try:
            from main import app
            self.assertIsNotNone(app)
        except ImportError as e:
            self.fail(f"Main app import failed: {e}")

if __name__ == '__main__':
    unittest.main()
