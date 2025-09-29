"""
エッジケーステスト
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

class TestEdgeCases(unittest.TestCase):
    """エッジケーステストクラス"""
    
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
    
    def test_content_analyzer_edge_cases(self):
        """ContentAnalyzerのエッジケーステスト"""
        # 非常に短いテキスト
        short_text = "a"
        result = self.analyzer.analyze_text(short_text)
        self.assertIsNotNone(result)
        self.assertEqual(result.word_count, 1)
        self.assertEqual(result.sentence_count, 1)
        
        # 1文字のテキスト
        single_char_text = "a"
        result = self.analyzer.analyze_text(single_char_text)
        self.assertIsNotNone(result)
        self.assertEqual(result.word_count, 1)
        
        # 空白のみのテキスト
        whitespace_text = "   \n\t   "
        result = self.analyzer.analyze_text(whitespace_text)
        self.assertIsNotNone(result)
        self.assertEqual(result.word_count, 0)
        self.assertEqual(result.sentence_count, 0)
        
        # 特殊文字のみのテキスト
        special_chars_text = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        result = self.analyzer.analyze_text(special_chars_text)
        self.assertIsNotNone(result)
        self.assertEqual(result.word_count, 0)
        self.assertEqual(result.sentence_count, 0)
        
        # 数字のみのテキスト
        numbers_text = "1234567890"
        result = self.analyzer.analyze_text(numbers_text)
        self.assertIsNotNone(result)
        self.assertEqual(result.word_count, 1)
        
        # 改行のみのテキスト
        newlines_text = "\n\n\n"
        result = self.analyzer.analyze_text(newlines_text)
        self.assertIsNotNone(result)
        self.assertEqual(result.word_count, 0)
        self.assertEqual(result.sentence_count, 0)
    
    def test_content_analyzer_similarity_edge_cases(self):
        """ContentAnalyzerの類似度計算エッジケーステスト"""
        # 同一テキスト
        text = "This is a test text."
        similarity = self.analyzer.calculate_similarity(text, text)
        self.assertEqual(similarity, 1.0)
        
        # 完全に異なるテキスト
        text1 = "This is a test text."
        text2 = "Completely different content here."
        similarity = self.analyzer.calculate_similarity(text1, text2)
        self.assertGreaterEqual(similarity, 0.0)
        self.assertLessEqual(similarity, 1.0)
        
        # 空のテキストとの比較
        text = "This is a test text."
        empty_text = ""
        similarity = self.analyzer.calculate_similarity(text, empty_text)
        self.assertEqual(similarity, 0.0)
        
        # 空のテキスト同士の比較
        similarity = self.analyzer.calculate_similarity("", "")
        self.assertEqual(similarity, 0.0)
        
        # 1文字のテキスト同士の比較
        similarity = self.analyzer.calculate_similarity("a", "a")
        self.assertEqual(similarity, 1.0)
        
        similarity = self.analyzer.calculate_similarity("a", "b")
        self.assertGreaterEqual(similarity, 0.0)
        self.assertLessEqual(similarity, 1.0)
    
    def test_content_analyzer_duplicate_detection_edge_cases(self):
        """ContentAnalyzerの重複検出エッジケーステスト"""
        # 空のリスト
        duplicates = self.analyzer.detect_duplicates([])
        self.assertIsInstance(duplicates, list)
        self.assertEqual(len(duplicates), 0)
        
        # 1つのテキストのみ
        duplicates = self.analyzer.detect_duplicates(["Single text"])
        self.assertIsInstance(duplicates, list)
        self.assertEqual(len(duplicates), 0)
        
        # 2つの同一テキスト
        duplicates = self.analyzer.detect_duplicates(["Same text", "Same text"])
        self.assertIsInstance(duplicates, list)
        self.assertGreater(len(duplicates), 0)
        
        # 2つの異なるテキスト
        duplicates = self.analyzer.detect_duplicates(["Text 1", "Text 2"])
        self.assertIsInstance(duplicates, list)
        self.assertEqual(len(duplicates), 0)
        
        # 空のテキストを含むリスト
        duplicates = self.analyzer.detect_duplicates(["Text", "", "Text"])
        self.assertIsInstance(duplicates, list)
        self.assertGreater(len(duplicates), 0)
    
    def test_analysis_engine_edge_cases(self):
        """AnalysisEngineのエッジケーステスト"""
        # 空のコンテンツリスト
        content_list = []
        
        # 非同期テストの実行
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(self.engine.analyze_content(content_list))
            self.assertIsNotNone(result)
            self.assertIn('analysis_id', result)
            self.assertIn('results', result)
            self.assertIn('summary', result)
        finally:
            loop.close()
        
        # 1つのコンテンツのみ
        content_list = [{
            'id': 'single_content',
            'title': 'Single Content',
            'content': 'This is a single content.',
            'source': 'notion'
        }]
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(self.engine.analyze_content(content_list))
            self.assertIsNotNone(result)
            self.assertIn('analysis_id', result)
            self.assertIn('results', result)
            self.assertIn('summary', result)
        finally:
            loop.close()
        
        # 非常に短いコンテンツ
        content_list = [{
            'id': 'short_content',
            'title': 'Short',
            'content': 'a',
            'source': 'notion'
        }]
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(self.engine.analyze_content(content_list))
            self.assertIsNotNone(result)
            self.assertIn('analysis_id', result)
            self.assertIn('results', result)
            self.assertIn('summary', result)
        finally:
            loop.close()
    
    def test_conflict_resolver_edge_cases(self):
        """ConflictResolverのエッジケーステスト"""
        # 空のコンテンツ
        notion_content = {'title': '', 'content': '', 'last_edited_time': ''}
        obsidian_content = {'title': '', 'content': '', 'modified_time': ''}
        
        conflicts = self.resolver.detect_conflict(notion_content, obsidian_content)
        self.assertIsInstance(conflicts, list)
        self.assertEqual(len(conflicts), 0)
        
        # 同一コンテンツ
        notion_content = {'title': 'Same', 'content': 'Same', 'last_edited_time': '2024-01-01T00:00:00Z'}
        obsidian_content = {'title': 'Same', 'content': 'Same', 'modified_time': '2024-01-01T00:00:00Z'}
        
        conflicts = self.resolver.detect_conflict(notion_content, obsidian_content)
        self.assertIsInstance(conflicts, list)
        self.assertEqual(len(conflicts), 0)
        
        # タイトルのみ異なる
        notion_content = {'title': 'Notion Title', 'content': 'Same', 'last_edited_time': '2024-01-01T00:00:00Z'}
        obsidian_content = {'title': 'Obsidian Title', 'content': 'Same', 'modified_time': '2024-01-01T00:00:00Z'}
        
        conflicts = self.resolver.detect_conflict(notion_content, obsidian_content)
        self.assertIsInstance(conflicts, list)
        self.assertGreater(len(conflicts), 0)
        
        # コンテンツのみ異なる
        notion_content = {'title': 'Same', 'content': 'Notion Content', 'last_edited_time': '2024-01-01T00:00:00Z'}
        obsidian_content = {'title': 'Same', 'content': 'Obsidian Content', 'modified_time': '2024-01-01T00:00:00Z'}
        
        conflicts = self.resolver.detect_conflict(notion_content, obsidian_content)
        self.assertIsInstance(conflicts, list)
        self.assertGreater(len(conflicts), 0)
    
    def test_event_manager_edge_cases(self):
        """EventManagerのエッジケーステスト"""
        # 空のイベントタイプ
        self.manager.emit_event("", {"message": "test"}, "test_source", 1)
        
        # 空のイベントデータ
        self.manager.emit_event("test_event", {}, "test_source", 1)
        
        # 空のソース
        self.manager.emit_event("test_event", {"message": "test"}, "", 1)
        
        # 負の優先度
        self.manager.emit_event("test_event", {"message": "test"}, "test_source", -1)
        
        # 非常に高い優先度
        self.manager.emit_event("test_event", {"message": "test"}, "test_source", 1000)
        
        # 特殊文字を含むイベントタイプ
        self.manager.emit_event("test_event_!@#$%", {"message": "test"}, "test_source", 1)
        
        # 特殊文字を含むソース
        self.manager.emit_event("test_event", {"message": "test"}, "test_source_!@#$%", 1)
    
    def test_file_monitor_edge_cases(self):
        """ObsidianFileMonitorのエッジケーステスト"""
        # 空のファイル名
        empty_filename = ""
        file_path = os.path.join(self.temp_dir, empty_filename)
        result = self.monitor.write_file_content(file_path, "test content")
        self.assertFalse(result)
        
        # 非常に長いファイル名
        long_filename = "a" * 1000 + ".md"
        file_path = os.path.join(self.temp_dir, long_filename)
        result = self.monitor.write_file_content(file_path, "test content")
        self.assertFalse(result)
        
        # 特殊文字を含むファイル名
        special_filename = "test!@#$%^&*().md"
        file_path = os.path.join(self.temp_dir, special_filename)
        result = self.monitor.write_file_content(file_path, "test content")
        self.assertFalse(result)
        
        # 空のコンテンツ
        test_file = os.path.join(self.temp_dir, 'empty.md')
        result = self.monitor.write_file_content(test_file, "")
        self.assertTrue(result)
        self.assertTrue(os.path.exists(test_file))
        
        # 非常に長いコンテンツ
        long_content = "x" * 1000000  # 1MBのコンテンツ
        test_file = os.path.join(self.temp_dir, 'long.md')
        result = self.monitor.write_file_content(test_file, long_content)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(test_file))
        
        # 改行のみのコンテンツ
        newlines_content = "\n\n\n"
        test_file = os.path.join(self.temp_dir, 'newlines.md')
        result = self.monitor.write_file_content(test_file, newlines_content)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(test_file))
        
        # タブのみのコンテンツ
        tabs_content = "\t\t\t"
        test_file = os.path.join(self.temp_dir, 'tabs.md')
        result = self.monitor.write_file_content(test_file, tabs_content)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(test_file))
    
    def test_file_monitor_nested_directories(self):
        """ObsidianFileMonitorのネストしたディレクトリテスト"""
        # 深いネストしたディレクトリを作成
        deep_path = os.path.join(self.temp_dir, 'level1', 'level2', 'level3', 'level4', 'level5')
        test_file = os.path.join(deep_path, 'deep.md')
        content = '# Deep File\n\nThis is a file in a deep directory.'
        
        result = self.monitor.write_file_content(test_file, content)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(test_file))
        
        # ファイルの内容を読み取り
        read_content = self.monitor.get_file_content(test_file)
        self.assertEqual(read_content, content)
    
    def test_file_monitor_special_files(self):
        """ObsidianFileMonitorの特殊ファイルテスト"""
        # 隠しファイル
        hidden_file = os.path.join(self.temp_dir, '.hidden.md')
        content = '# Hidden File\n\nThis is a hidden file.'
        
        result = self.monitor.write_file_content(hidden_file, content)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(hidden_file))
        
        # ファイルの内容を読み取り
        read_content = self.monitor.get_file_content(hidden_file)
        self.assertEqual(read_content, content)
        
        # 数字で始まるファイル名
        numeric_file = os.path.join(self.temp_dir, '123test.md')
        content = '# Numeric File\n\nThis file starts with a number.'
        
        result = self.monitor.write_file_content(numeric_file, content)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(numeric_file))
        
        # ファイルの内容を読み取り
        read_content = self.monitor.get_file_content(numeric_file)
        self.assertEqual(read_content, content)
    
    def test_file_monitor_unicode_edge_cases(self):
        """ObsidianFileMonitorのUnicodeエッジケーステスト"""
        # 絵文字を含むファイル名
        emoji_file = os.path.join(self.temp_dir, 'test_😀🎉🚀.md')
        content = '# Emoji File\n\nThis file has emojis: 😀🎉🚀'
        
        result = self.monitor.write_file_content(emoji_file, content)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(emoji_file))
        
        # ファイルの内容を読み取り
        read_content = self.monitor.get_file_content(emoji_file)
        self.assertEqual(read_content, content)
        
        # 特殊なUnicode文字を含むファイル名
        unicode_file = os.path.join(self.temp_dir, 'test_αβγδε.md')
        content = '# Unicode File\n\nThis file has Greek letters: αβγδε'
        
        result = self.monitor.write_file_content(unicode_file, content)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(unicode_file))
        
        # ファイルの内容を読み取り
        read_content = self.monitor.get_file_content(unicode_file)
        self.assertEqual(read_content, content)
    
    def test_file_monitor_concurrent_edge_cases(self):
        """ObsidianFileMonitorの並行エッジケーステスト"""
        import threading
        import time
        
        # 複数のスレッドで同時に同じファイルに異なる内容を書き込み
        def write_file(thread_id):
            file_path = os.path.join(self.temp_dir, 'concurrent.md')
            content = f'# Concurrent File {thread_id}\n\nThis is file {thread_id}.'
            
            result = self.monitor.write_file_content(file_path, content)
            return result
        
        # 複数のスレッドで同時実行
        threads = []
        results = []
        
        for i in range(5):
            thread = threading.Thread(target=lambda i=i: results.append(write_file(i)))
            threads.append(thread)
            thread.start()
        
        # すべてのスレッドの完了を待機
        for thread in threads:
            thread.join()
        
        # 結果の確認
        self.assertEqual(len(results), 5)
        
        # 少なくとも1つのファイルが作成されたことを確認
        self.assertTrue(any(results))
        
        # ファイルが存在することを確認
        file_path = os.path.join(self.temp_dir, 'concurrent.md')
        self.assertTrue(os.path.exists(file_path))

if __name__ == '__main__':
    unittest.main()
