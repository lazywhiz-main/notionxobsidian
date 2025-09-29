"""
セキュリティテスト
"""
import unittest
import sys
import os
import tempfile
import shutil
from unittest.mock import Mock, patch

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import Settings
from analysis_engine.content_analyzer import ContentAnalyzer
from sync_system.data_transformer import DataTransformer
from obsidian_integration.file_monitor import ObsidianFileMonitor

class TestSecurity(unittest.TestCase):
    """セキュリティテストクラス"""
    
    def setUp(self):
        """テストの前処理"""
        # 一時ディレクトリを作成
        self.temp_dir = tempfile.mkdtemp()
        
        # テスト用のオブジェクトを作成
        self.analyzer = ContentAnalyzer()
        self.transformer = DataTransformer()
        self.monitor = ObsidianFileMonitor(self.temp_dir)
    
    def tearDown(self):
        """テストの後処理"""
        # 一時ディレクトリを削除
        shutil.rmtree(self.temp_dir)
    
    def test_settings_token_validation(self):
        """設定のトークン検証テスト"""
        # 空のトークン
        with self.assertRaises(ValueError):
            settings = Settings(
                notion_token="",
                obsidian_path="/test/path"
            )
            settings.validate()
        
        # Noneのトークン
        with self.assertRaises(ValueError):
            settings = Settings(
                notion_token=None,
                obsidian_path="/test/path"
            )
            settings.validate()
    
    def test_settings_path_validation(self):
        """設定のパス検証テスト"""
        # 空のパス
        with self.assertRaises(ValueError):
            settings = Settings(
                notion_token="test_token",
                obsidian_path=""
            )
            settings.validate()
        
        # Noneのパス
        with self.assertRaises(ValueError):
            settings = Settings(
                notion_token="test_token",
                obsidian_path=None
            )
            settings.validate()
        
        # 存在しないパス
        with self.assertRaises(ValueError):
            settings = Settings(
                notion_token="test_token",
                obsidian_path="/nonexistent/path"
            )
            settings.validate()
    
    def test_content_analyzer_input_validation(self):
        """ContentAnalyzerの入力検証テスト"""
        # Noneのテキスト
        result = self.analyzer.analyze_text(None)
        self.assertIsNotNone(result)
        self.assertEqual(result.word_count, 0)
        self.assertEqual(result.sentence_count, 0)
        
        # 空のテキスト
        result = self.analyzer.analyze_text("")
        self.assertIsNotNone(result)
        self.assertEqual(result.word_count, 0)
        self.assertEqual(result.sentence_count, 0)
        
        # 非常に長いテキスト（DoS攻撃のシミュレーション）
        very_long_text = "x" * 1000000  # 1MBのテキスト
        result = self.analyzer.analyze_text(very_long_text)
        self.assertIsNotNone(result)
        self.assertGreater(result.word_count, 0)
    
    def test_content_analyzer_malicious_input(self):
        """ContentAnalyzerの悪意のある入力テスト"""
        # SQLインジェクション攻撃のシミュレーション
        malicious_text = "'; DROP TABLE users; --"
        result = self.analyzer.analyze_text(malicious_text)
        self.assertIsNotNone(result)
        self.assertGreater(result.word_count, 0)
        
        # XSS攻撃のシミュレーション
        xss_text = "<script>alert('XSS')</script>"
        result = self.analyzer.analyze_text(xss_text)
        self.assertIsNotNone(result)
        self.assertGreater(result.word_count, 0)
        
        # パストラバーサル攻撃のシミュレーション
        path_traversal_text = "../../../etc/passwd"
        result = self.analyzer.analyze_text(path_traversal_text)
        self.assertIsNotNone(result)
        self.assertGreater(result.word_count, 0)
    
    def test_data_transformer_input_validation(self):
        """DataTransformerの入力検証テスト"""
        # Noneのコンテンツ
        result = self.transformer.convert_notion_to_obsidian(None)
        self.assertIsNotNone(result)
        self.assertEqual(result, {})
        
        # 空のコンテンツ
        result = self.transformer.convert_notion_to_obsidian({})
        self.assertIsNotNone(result)
        self.assertEqual(result, {})
        
        # 不正な構造のコンテンツ
        invalid_content = {
            'page': None,
            'blocks': None
        }
        result = self.transformer.convert_notion_to_obsidian(invalid_content)
        self.assertIsNotNone(result)
        self.assertEqual(result, {})
    
    def test_data_transformer_malicious_content(self):
        """DataTransformerの悪意のあるコンテンツテスト"""
        # 悪意のあるNotionコンテンツ
        malicious_notion_content = {
            'page': {
                'id': '<script>alert("XSS")</script>',
                'created_time': '2024-01-01T00:00:00Z',
                'last_edited_time': '2024-01-01T00:00:00Z',
                'properties': {
                    'title': {
                        'title': [{'text': {'content': '<script>alert("XSS")</script>'}}]
                    }
                }
            },
            'blocks': {
                'results': [
                    {
                        'type': 'paragraph',
                        'paragraph': {
                            'rich_text': [{'text': {'content': '<script>alert("XSS")</script>'}}]
                        }
                    }
                ]
            }
        }
        
        result = self.transformer.convert_notion_to_obsidian(malicious_notion_content)
        self.assertIsNotNone(result)
        self.assertIn('title', result)
        self.assertIn('content', result)
        
        # スクリプトタグがエスケープされていることを確認
        self.assertNotIn('<script>', result['content'])
        self.assertNotIn('</script>', result['content'])
    
    def test_file_monitor_path_validation(self):
        """ファイルモニターのパス検証テスト"""
        # 存在しないパス
        with self.assertRaises(ValueError):
            monitor = ObsidianFileMonitor("/nonexistent/path")
            monitor.initialize()
        
        # ファイルパス（ディレクトリではない）
        test_file = os.path.join(self.temp_dir, 'test.md')
        with open(test_file, 'w') as f:
            f.write('# Test')
        
        with self.assertRaises(ValueError):
            monitor = ObsidianFileMonitor(test_file)
            monitor.initialize()
    
    def test_file_monitor_path_traversal(self):
        """ファイルモニターのパストラバーサルテスト"""
        # パストラバーサル攻撃のシミュレーション
        malicious_path = os.path.join(self.temp_dir, '../../../etc/passwd')
        
        # ファイルの作成を試行
        result = self.monitor.write_file_content(malicious_path, 'malicious content')
        
        # パストラバーサル攻撃が防がれていることを確認
        self.assertFalse(result)
        self.assertFalse(os.path.exists(malicious_path))
    
    def test_file_monitor_malicious_filename(self):
        """ファイルモニターの悪意のあるファイル名テスト"""
        # 悪意のあるファイル名
        malicious_filenames = [
            'test<script>alert("XSS")</script>.md',
            'test../../../etc/passwd.md',
            'test\x00null.md',
            'test\nnewline.md',
            'test\ttab.md'
        ]
        
        for filename in malicious_filenames:
            file_path = os.path.join(self.temp_dir, filename)
            
            # ファイルの作成を試行
            result = self.monitor.write_file_content(file_path, 'test content')
            
            # ファイルが作成されないことを確認
            self.assertFalse(result)
            self.assertFalse(os.path.exists(file_path))
    
    def test_file_monitor_large_file(self):
        """ファイルモニターの大きなファイルテスト"""
        # 非常に大きなファイル（DoS攻撃のシミュレーション）
        large_content = 'x' * 10000000  # 10MBのコンテンツ
        
        test_file = os.path.join(self.temp_dir, 'large_file.md')
        
        # ファイルの作成を試行
        result = self.monitor.write_file_content(test_file, large_content)
        
        # ファイルが作成されることを確認（メモリ制限内であれば）
        if result:
            self.assertTrue(os.path.exists(test_file))
            
            # ファイルサイズを確認
            file_size = os.path.getsize(test_file)
            self.assertGreater(file_size, 0)
    
    def test_file_monitor_concurrent_access(self):
        """ファイルモニターの並行アクセステスト"""
        import threading
        import time
        
        # 複数のスレッドで同時にファイルを作成
        def create_file(thread_id):
            file_path = os.path.join(self.temp_dir, f'concurrent_{thread_id}.md')
            content = f'# Concurrent File {thread_id}\n\nThis is file {thread_id}.'
            
            result = self.monitor.write_file_content(file_path, content)
            return result
        
        # 複数のスレッドで同時実行
        threads = []
        results = []
        
        for i in range(10):
            thread = threading.Thread(target=lambda i=i: results.append(create_file(i)))
            threads.append(thread)
            thread.start()
        
        # すべてのスレッドの完了を待機
        for thread in threads:
            thread.join()
        
        # 結果の確認
        self.assertEqual(len(results), 10)
        
        # すべてのファイルが作成されたことを確認
        for i in range(10):
            file_path = os.path.join(self.temp_dir, f'concurrent_{i}.md')
            self.assertTrue(os.path.exists(file_path))
    
    def test_file_monitor_permission_handling(self):
        """ファイルモニターの権限処理テスト"""
        # 読み取り専用ディレクトリを作成
        read_only_dir = os.path.join(self.temp_dir, 'readonly')
        os.makedirs(read_only_dir)
        os.chmod(read_only_dir, 0o444)  # 読み取り専用
        
        try:
            # 読み取り専用ディレクトリにファイルを作成しようとする
            file_path = os.path.join(read_only_dir, 'test.md')
            result = self.monitor.write_file_content(file_path, 'test content')
            
            # ファイルが作成されないことを確認
            self.assertFalse(result)
            self.assertFalse(os.path.exists(file_path))
            
        finally:
            # 権限を元に戻す
            os.chmod(read_only_dir, 0o755)
    
    def test_file_monitor_symlink_handling(self):
        """ファイルモニターのシンボリックリンク処理テスト"""
        # シンボリックリンクを作成
        target_file = os.path.join(self.temp_dir, 'target.md')
        with open(target_file, 'w') as f:
            f.write('# Target File')
        
        symlink_file = os.path.join(self.temp_dir, 'symlink.md')
        os.symlink(target_file, symlink_file)
        
        # シンボリックリンクの内容を読み取り
        content = self.monitor.get_file_content(symlink_file)
        
        # シンボリックリンクの内容が読み取れることを確認
        self.assertIsNotNone(content)
        self.assertEqual(content, '# Target File')
    
    def test_file_monitor_hidden_files(self):
        """ファイルモニターの隠しファイル処理テスト"""
        # 隠しファイルを作成
        hidden_file = os.path.join(self.temp_dir, '.hidden.md')
        with open(hidden_file, 'w') as f:
            f.write('# Hidden File')
        
        # 隠しファイルの内容を読み取り
        content = self.monitor.get_file_content(hidden_file)
        
        # 隠しファイルの内容が読み取れることを確認
        self.assertIsNotNone(content)
        self.assertEqual(content, '# Hidden File')
    
    def test_file_monitor_special_characters(self):
        """ファイルモニターの特殊文字処理テスト"""
        # 特殊文字を含むファイル名
        special_chars = ['test file.md', 'test-file.md', 'test_file.md', 'test.file.md']
        
        for filename in special_chars:
            file_path = os.path.join(self.temp_dir, filename)
            content = f'# {filename}\n\nThis is a test file.'
            
            # ファイルの作成
            result = self.monitor.write_file_content(file_path, content)
            
            # ファイルが作成されることを確認
            self.assertTrue(result)
            self.assertTrue(os.path.exists(file_path))
            
            # ファイルの内容を読み取り
            read_content = self.monitor.get_file_content(file_path)
            self.assertEqual(read_content, content)

if __name__ == '__main__':
    unittest.main()
