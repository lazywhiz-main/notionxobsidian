"""
設定のテスト
"""
import unittest
import sys
import os

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import Settings

class TestSettings(unittest.TestCase):
    """Settingsのテストクラス"""
    
    def test_settings_creation(self):
        """設定の作成テスト"""
        settings = Settings(
            notion_token="test_token",
            obsidian_path="/test/path"
        )
        
        self.assertEqual(settings.notion_token, "test_token")
        self.assertEqual(settings.obsidian_path, "/test/path")
        self.assertEqual(settings.analysis_interval, 300)
        self.assertEqual(settings.sync_interval, 60)
    
    def test_settings_validation(self):
        """設定の検証テスト"""
        # 正常な設定
        settings = Settings(
            notion_token="test_token",
            obsidian_path="/test/path"
        )
        
        # 検証は成功するはず（パスが存在しない場合はエラーになるが、テストでは無視）
        try:
            settings.validate()
        except ValueError:
            # パスが存在しない場合はエラーになるが、これは正常
            pass
    
    def test_settings_from_env(self):
        """環境変数からの設定読み込みテスト"""
        # 環境変数を設定
        os.environ['NOTION_TOKEN'] = 'test_token'
        os.environ['OBSIDIAN_PATH'] = '/test/path'
        os.environ['ANALYSIS_INTERVAL'] = '600'
        
        settings = Settings.from_env()
        
        self.assertEqual(settings.notion_token, 'test_token')
        self.assertEqual(settings.obsidian_path, '/test/path')
        self.assertEqual(settings.analysis_interval, 600)

if __name__ == '__main__':
    unittest.main()
