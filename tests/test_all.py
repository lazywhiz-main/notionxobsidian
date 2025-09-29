"""
すべてのテストを実行するテストスイート
"""
import unittest
import sys
import os

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# テストモジュールをインポート
from tests.test_content_analyzer import TestContentAnalyzer
from tests.test_config import TestSettings
from tests.test_data_transformer import TestDataTransformer
from tests.test_conflict_resolver import TestConflictResolver
from tests.test_event_manager import TestEventManager
from tests.test_markdown_parser import TestObsidianMarkdownParser
from tests.test_insight_generator import TestInsightGenerator
from tests.test_recommendation_system import TestRecommendationSystem
from tests.test_analysis_engine import TestAnalysisEngine
from tests.test_sync_coordinator import TestSyncCoordinator
from tests.test_notion_client import TestNotionClient
from tests.test_obsidian_file_monitor import TestObsidianFileMonitor
from tests.test_main import TestNotionObsidianSyncApp

def create_test_suite():
    """テストスイートを作成"""
    suite = unittest.TestSuite()
    
    # テストケースを追加
    suite.addTest(unittest.makeSuite(TestContentAnalyzer))
    suite.addTest(unittest.makeSuite(TestSettings))
    suite.addTest(unittest.makeSuite(TestDataTransformer))
    suite.addTest(unittest.makeSuite(TestConflictResolver))
    suite.addTest(unittest.makeSuite(TestEventManager))
    suite.addTest(unittest.makeSuite(TestObsidianMarkdownParser))
    suite.addTest(unittest.makeSuite(TestInsightGenerator))
    suite.addTest(unittest.makeSuite(TestRecommendationSystem))
    suite.addTest(unittest.makeSuite(TestAnalysisEngine))
    suite.addTest(unittest.makeSuite(TestSyncCoordinator))
    suite.addTest(unittest.makeSuite(TestNotionClient))
    suite.addTest(unittest.makeSuite(TestObsidianFileMonitor))
    suite.addTest(unittest.makeSuite(TestNotionObsidianSyncApp))
    
    return suite

def run_tests():
    """テストを実行"""
    # テストスイートを作成
    suite = create_test_suite()
    
    # テストランナーを作成
    runner = unittest.TextTestRunner(verbosity=2)
    
    # テストを実行
    result = runner.run(suite)
    
    # 結果を返す
    return result

if __name__ == '__main__':
    # テストを実行
    result = run_tests()
    
    # 終了コードを設定
    sys.exit(0 if result.wasSuccessful() else 1)
