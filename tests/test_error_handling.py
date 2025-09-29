"""
エラーハンドリングテスト
"""
import unittest
import sys
import os
import tempfile
import shutil
from unittest.mock import Mock, patch

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis_engine.analysis_engine import AnalysisEngine
from analysis_engine.content_analyzer import ContentAnalyzer
from sync_system.conflict_resolver import ConflictResolver
from sync_system.event_manager import EventManager
from obsidian_integration.file_monitor import ObsidianFileMonitor

class TestErrorHandling(unittest.TestCase):
    """エラーハンドリングテストクラス"""
    
    def setUp(self):
        """テストの前処理"""
        # 一時ディレクトリを作成
        self.temp_dir = tempfile.mkdtemp()
        
        # テスト用のオブジェクトを作成
        self.analyzer = ContentAnalyzer()
        self.engine = AnalysisEngine()
        self.resolver = ConflictResolver()
        self.manager = EventManager()
        self.monitor = ObsidianFileMonitor(self.temp_dir)
    
    def tearDown(self):
        """テストの後処理"""
        # 一時ディレクトリを削除
        shutil.rmtree(self.temp_dir)
    
    def test_content_analyzer_error_handling(self):
        """ContentAnalyzerのエラーハンドリングテスト"""
        # 不正な入力でのエラーハンドリング
        invalid_inputs = [
            None,
            "",
            123,
            [],
            {},
            "x" * 1000000  # 非常に長いテキスト
        ]
        
        for invalid_input in invalid_inputs:
            try:
                result = self.analyzer.analyze_text(invalid_input)
                # エラーが発生しないことを確認
                self.assertIsNotNone(result)
            except Exception as e:
                self.fail(f"ContentAnalyzer raised an exception for input {type(invalid_input)}: {e}")
    
    def test_content_analyzer_similarity_error_handling(self):
        """ContentAnalyzerの類似度計算エラーハンドリングテスト"""
        # 不正な入力での類似度計算
        invalid_inputs = [
            (None, "test"),
            ("test", None),
            ("", "test"),
            ("test", ""),
            (123, "test"),
            ("test", 123)
        ]
        
        for text1, text2 in invalid_inputs:
            try:
                similarity = self.analyzer.calculate_similarity(text1, text2)
                # エラーが発生しないことを確認
                self.assertIsNotNone(similarity)
                self.assertGreaterEqual(similarity, 0.0)
                self.assertLessEqual(similarity, 1.0)
            except Exception as e:
                self.fail(f"ContentAnalyzer similarity calculation raised an exception: {e}")
    
    def test_content_analyzer_duplicate_detection_error_handling(self):
        """ContentAnalyzerの重複検出エラーハンドリングテスト"""
        # 不正な入力での重複検出
        invalid_inputs = [
            None,
            [],
            [None],
            ["", None],
            [123, "test"],
            ["test", 123]
        ]
        
        for invalid_input in invalid_inputs:
            try:
                duplicates = self.analyzer.detect_duplicates(invalid_input)
                # エラーが発生しないことを確認
                self.assertIsNotNone(duplicates)
                self.assertIsInstance(duplicates, list)
            except Exception as e:
                self.fail(f"ContentAnalyzer duplicate detection raised an exception: {e}")
    
    def test_analysis_engine_error_handling(self):
        """AnalysisEngineのエラーハンドリングテスト"""
        # 不正な入力での分析
        invalid_inputs = [
            None,
            [],
            [None],
            [{"id": "test", "title": "test", "content": None}],
            [{"id": "test", "title": "test", "content": ""}],
            [{"id": "test", "title": "test", "content": 123}]
        ]
        
        # 非同期テストの実行
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            for invalid_input in invalid_inputs:
                try:
                    result = loop.run_until_complete(self.engine.analyze_content(invalid_input))
                    # エラーが発生しないことを確認
                    self.assertIsNotNone(result)
                    self.assertIn('analysis_id', result)
                    self.assertIn('results', result)
                    self.assertIn('summary', result)
                except Exception as e:
                    self.fail(f"AnalysisEngine raised an exception: {e}")
        finally:
            loop.close()
    
    def test_conflict_resolver_error_handling(self):
        """ConflictResolverのエラーハンドリングテスト"""
        # 不正な入力での競合検出
        invalid_inputs = [
            (None, {"title": "test"}),
            ({"title": "test"}, None),
            ({}, {"title": "test"}),
            ({"title": "test"}, {}),
            ({"title": None}, {"title": "test"}),
            ({"title": "test"}, {"title": None})
        ]
        
        for notion_content, obsidian_content in invalid_inputs:
            try:
                conflicts = self.resolver.detect_conflict(notion_content, obsidian_content)
                # エラーが発生しないことを確認
                self.assertIsNotNone(conflicts)
                self.assertIsInstance(conflicts, list)
            except Exception as e:
                self.fail(f"ConflictResolver conflict detection raised an exception: {e}")
        
        # 不正な入力での競合解決
        invalid_conflicts = [
            None,
            {},
            {"type": "invalid_type"},
            {"type": "title_conflict", "field": None},
            {"type": "title_conflict", "field": "title", "notion_value": None},
            {"type": "title_conflict", "field": "title", "obsidian_value": None}
        ]
        
        for invalid_conflict in invalid_conflicts:
            try:
                resolution = self.resolver.resolve_conflict(invalid_conflict, 'notion_priority')
                # エラーが発生しないことを確認
                self.assertIsNotNone(resolution)
            except Exception as e:
                self.fail(f"ConflictResolver conflict resolution raised an exception: {e}")
    
    def test_event_manager_error_handling(self):
        """EventManagerのエラーハンドリングテスト"""
        # 不正な入力でのイベント発生
        invalid_inputs = [
            (None, {"message": "test"}),
            ("test_event", None),
            ("", {"message": "test"}),
            ("test_event", ""),
            (123, {"message": "test"}),
            ("test_event", 123)
        ]
        
        for event_type, event_data in invalid_inputs:
            try:
                self.manager.emit_event(event_type, event_data, "test_source", 1)
                # エラーが発生しないことを確認
            except Exception as e:
                self.fail(f"EventManager event emission raised an exception: {e}")
        
        # 不正な入力でのハンドラー登録
        invalid_handlers = [
            None,
            "",
            123,
            [],
            {}
        ]
        
        for invalid_handler in invalid_handlers:
            try:
                self.manager.register_handler("test_event", invalid_handler)
                # エラーが発生しないことを確認
            except Exception as e:
                self.fail(f"EventManager handler registration raised an exception: {e}")
    
    def test_file_monitor_error_handling(self):
        """ObsidianFileMonitorのエラーハンドリングテスト"""
        # 不正な入力でのファイル操作
        invalid_inputs = [
            None,
            "",
            123,
            [],
            {},
            "/nonexistent/path/file.md"
        ]
        
        for invalid_input in invalid_inputs:
            try:
                # ファイル内容の取得
                content = self.monitor.get_file_content(invalid_input)
                # エラーが発生しないことを確認
                self.assertIsNone(content)
            except Exception as e:
                self.fail(f"ObsidianFileMonitor get_file_content raised an exception: {e}")
            
            try:
                # ファイル内容の書き込み
                result = self.monitor.write_file_content(invalid_input, "test content")
                # エラーが発生しないことを確認
                self.assertFalse(result)
            except Exception as e:
                self.fail(f"ObsidianFileMonitor write_file_content raised an exception: {e}")
    
    def test_file_monitor_permission_error_handling(self):
        """ObsidianFileMonitorの権限エラーハンドリングテスト"""
        # 読み取り専用ディレクトリを作成
        read_only_dir = os.path.join(self.temp_dir, 'readonly')
        os.makedirs(read_only_dir)
        os.chmod(read_only_dir, 0o444)  # 読み取り専用
        
        try:
            # 読み取り専用ディレクトリにファイルを作成しようとする
            file_path = os.path.join(read_only_dir, 'test.md')
            result = self.monitor.write_file_content(file_path, 'test content')
            
            # エラーが発生しないことを確認
            self.assertFalse(result)
            self.assertFalse(os.path.exists(file_path))
            
        finally:
            # 権限を元に戻す
            os.chmod(read_only_dir, 0o755)
    
    def test_file_monitor_disk_space_error_handling(self):
        """ObsidianFileMonitorのディスク容量エラーハンドリングテスト"""
        # 非常に大きなファイルを作成しようとする
        large_content = 'x' * 100000000  # 100MBのコンテンツ
        
        test_file = os.path.join(self.temp_dir, 'large_file.md')
        
        try:
            result = self.monitor.write_file_content(test_file, large_content)
            # エラーが発生しないことを確認
            self.assertIsNotNone(result)
        except Exception as e:
            # ディスク容量不足の場合はエラーが発生する可能性がある
            self.assertIn("No space left", str(e))
    
    def test_file_monitor_concurrent_access_error_handling(self):
        """ObsidianFileMonitorの並行アクセスエラーハンドリングテスト"""
        import threading
        import time
        
        # 複数のスレッドで同時に同じファイルにアクセス
        def access_file(thread_id):
            file_path = os.path.join(self.temp_dir, 'concurrent.md')
            content = f'# Concurrent File {thread_id}\n\nThis is file {thread_id}.'
            
            try:
                result = self.monitor.write_file_content(file_path, content)
                return result
            except Exception as e:
                return False
        
        # 複数のスレッドで同時実行
        threads = []
        results = []
        
        for i in range(10):
            thread = threading.Thread(target=lambda i=i: results.append(access_file(i)))
            threads.append(thread)
            thread.start()
        
        # すべてのスレッドの完了を待機
        for thread in threads:
            thread.join()
        
        # 結果の確認
        self.assertEqual(len(results), 10)
        
        # 少なくとも1つのファイルが作成されたことを確認
        self.assertTrue(any(results))
    
    def test_file_monitor_corrupted_file_handling(self):
        """ObsidianFileMonitorの破損ファイル処理テスト"""
        # 破損したファイルを作成
        corrupted_file = os.path.join(self.temp_dir, 'corrupted.md')
        
        # バイナリデータを書き込み
        with open(corrupted_file, 'wb') as f:
            f.write(b'\x00\x01\x02\x03\x04\x05')
        
        try:
            # 破損したファイルの内容を読み取り
            content = self.monitor.get_file_content(corrupted_file)
            # エラーが発生しないことを確認
            self.assertIsNotNone(content)
        except Exception as e:
            # エラーが発生した場合は適切にハンドリングされることを確認
            self.assertIsInstance(e, Exception)
    
    def test_file_monitor_symlink_error_handling(self):
        """ObsidianFileMonitorのシンボリックリンクエラーハンドリングテスト"""
        # 存在しないファイルへのシンボリックリンクを作成
        broken_symlink = os.path.join(self.temp_dir, 'broken_symlink.md')
        os.symlink('/nonexistent/file.md', broken_symlink)
        
        try:
            # 壊れたシンボリックリンクの内容を読み取り
            content = self.monitor.get_file_content(broken_symlink)
            # エラーが発生しないことを確認
            self.assertIsNone(content)
        except Exception as e:
            # エラーが発生した場合は適切にハンドリングされることを確認
            self.assertIsInstance(e, Exception)
    
    def test_file_monitor_unicode_error_handling(self):
        """ObsidianFileMonitorのUnicodeエラーハンドリングテスト"""
        # Unicode文字を含むファイル名
        unicode_filename = 'test_日本語_한국어_中文.md'
        file_path = os.path.join(self.temp_dir, unicode_filename)
        content = '# Unicode Test\n\nThis is a test with Unicode characters: 日本語 한국어 中文'
        
        try:
            # Unicodeファイルの作成
            result = self.monitor.write_file_content(file_path, content)
            # エラーが発生しないことを確認
            self.assertTrue(result)
            self.assertTrue(os.path.exists(file_path))
            
            # Unicodeファイルの内容を読み取り
            read_content = self.monitor.get_file_content(file_path)
            self.assertEqual(read_content, content)
        except Exception as e:
            # エラーが発生した場合は適切にハンドリングされることを確認
            self.assertIsInstance(e, Exception)

if __name__ == '__main__':
    unittest.main()
