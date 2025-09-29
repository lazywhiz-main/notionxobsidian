"""
パフォーマンステスト
"""
import unittest
import sys
import os
import time
import asyncio
from unittest.mock import Mock

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis_engine.analysis_engine import AnalysisEngine
from analysis_engine.content_analyzer import ContentAnalyzer
from sync_system.conflict_resolver import ConflictResolver
from sync_system.event_manager import EventManager

class TestPerformance(unittest.TestCase):
    """パフォーマンステストクラス"""
    
    def setUp(self):
        """テストの前処理"""
        self.analyzer = ContentAnalyzer()
        self.engine = AnalysisEngine()
        self.resolver = ConflictResolver()
        self.manager = EventManager()
    
    def test_content_analyzer_performance(self):
        """ContentAnalyzerのパフォーマンステスト"""
        # 大量のテキストを作成
        large_text = "This is a test text. " * 1000  # 約25,000文字
        
        start_time = time.time()
        
        # テキスト分析を実行
        result = self.analyzer.analyze_text(large_text)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # 結果の確認
        self.assertIsNotNone(result)
        self.assertGreater(result.word_count, 0)
        self.assertGreater(result.sentence_count, 0)
        
        # パフォーマンスの確認（1秒以内に完了することを期待）
        self.assertLess(duration, 1.0, f"Text analysis took {duration:.2f} seconds")
        
        print(f"Large text analysis completed in {duration:.2f} seconds")
    
    def test_content_analyzer_similarity_performance(self):
        """ContentAnalyzerの類似度計算パフォーマンステスト"""
        # 大量のテキストを作成
        text1 = "This is a test text for similarity calculation. " * 500
        text2 = "This is another test text for similarity calculation. " * 500
        
        start_time = time.time()
        
        # 類似度計算を実行
        similarity = self.analyzer.calculate_similarity(text1, text2)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # 結果の確認
        self.assertGreaterEqual(similarity, 0.0)
        self.assertLessEqual(similarity, 1.0)
        
        # パフォーマンスの確認（1秒以内に完了することを期待）
        self.assertLess(duration, 1.0, f"Similarity calculation took {duration:.2f} seconds")
        
        print(f"Similarity calculation completed in {duration:.2f} seconds")
    
    def test_content_analyzer_duplicate_detection_performance(self):
        """ContentAnalyzerの重複検出パフォーマンステスト"""
        # 大量のテキストを作成
        texts = []
        for i in range(100):
            texts.append(f"This is test text number {i}. " * 50)
        
        start_time = time.time()
        
        # 重複検出を実行
        duplicates = self.analyzer.detect_duplicates(texts)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # 結果の確認
        self.assertIsInstance(duplicates, list)
        
        # パフォーマンスの確認（5秒以内に完了することを期待）
        self.assertLess(duration, 5.0, f"Duplicate detection took {duration:.2f} seconds")
        
        print(f"Duplicate detection completed in {duration:.2f} seconds")
    
    def test_analysis_engine_performance(self):
        """AnalysisEngineのパフォーマンステスト"""
        # 大量のコンテンツを作成
        content_list = []
        for i in range(50):
            content_list.append({
                'id': f'content_{i}',
                'title': f'Test Content {i}',
                'content': f'This is test content number {i}. ' * 100,
                'source': 'notion' if i % 2 == 0 else 'obsidian'
            })
        
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            start_time = time.time()
            
            # 分析を実行
            result = loop.run_until_complete(self.engine.analyze_content(content_list))
            
            end_time = time.time()
            duration = end_time - start_time
            
            # 結果の確認
            self.assertIsNotNone(result)
            self.assertIn('analysis_id', result)
            self.assertIn('results', result)
            self.assertIn('summary', result)
            
            # パフォーマンスの確認（10秒以内に完了することを期待）
            self.assertLess(duration, 10.0, f"Content analysis took {duration:.2f} seconds")
            
            print(f"Content analysis completed in {duration:.2f} seconds")
            
        finally:
            loop.close()
    
    def test_conflict_resolver_performance(self):
        """ConflictResolverのパフォーマンステスト"""
        # 大量の競合を作成
        conflicts = []
        for i in range(1000):
            conflicts.append({
                'type': 'title_conflict',
                'field': 'title',
                'notion_value': f'Notion Title {i}',
                'obsidian_value': f'Obsidian Title {i}',
                'notion_timestamp': '2024-01-01T00:00:00Z',
                'obsidian_timestamp': '2024-01-01T00:00:00Z',
                'severity': 'medium'
            })
        
        start_time = time.time()
        
        # 競合解決を実行
        resolutions = self.resolver.resolve_multiple_conflicts(conflicts, 'notion_priority')
        
        end_time = time.time()
        duration = end_time - start_time
        
        # 結果の確認
        self.assertIsInstance(resolutions, list)
        self.assertEqual(len(resolutions), len(conflicts))
        
        # パフォーマンスの確認（1秒以内に完了することを期待）
        self.assertLess(duration, 1.0, f"Conflict resolution took {duration:.2f} seconds")
        
        print(f"Conflict resolution completed in {duration:.2f} seconds")
    
    def test_event_manager_performance(self):
        """EventManagerのパフォーマンステスト"""
        # 大量のイベントを発生
        start_time = time.time()
        
        for i in range(1000):
            self.manager.emit_event('test_event', {'message': f'test_{i}'}, 'test_source', 1)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # パフォーマンスの確認（1秒以内に完了することを期待）
        self.assertLess(duration, 1.0, f"Event emission took {duration:.2f} seconds")
        
        print(f"Event emission completed in {duration:.2f} seconds")
        
        # 少し待ってから履歴をチェック
        time.sleep(0.1)
        
        # 履歴の取得パフォーマンス
        start_time = time.time()
        
        history = self.manager.get_event_history(limit=100)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # パフォーマンスの確認（0.1秒以内に完了することを期待）
        self.assertLess(duration, 0.1, f"History retrieval took {duration:.2f} seconds")
        
        print(f"History retrieval completed in {duration:.2f} seconds")
    
    def test_memory_usage(self):
        """メモリ使用量のテスト"""
        import psutil
        import gc
        
        # プロセスのメモリ使用量を取得
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # 大量のデータを作成
        large_data = []
        for i in range(1000):
            large_data.append({
                'id': f'item_{i}',
                'content': 'x' * 1000,  # 1KB per item
                'metadata': {'index': i}
            })
        
        # メモリ使用量を再取得
        current_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = current_memory - initial_memory
        
        print(f"Memory usage increased by {memory_increase:.2f} MB")
        
        # メモリ使用量の増加が適切な範囲内であることを確認
        self.assertLess(memory_increase, 100, f"Memory usage increased by {memory_increase:.2f} MB")
        
        # データをクリア
        large_data.clear()
        gc.collect()
        
        # メモリ使用量を再取得
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_decrease = current_memory - final_memory
        
        print(f"Memory usage decreased by {memory_decrease:.2f} MB after cleanup")
    
    def test_concurrent_operations(self):
        """並行操作のパフォーマンステスト"""
        import threading
        import queue
        
        # 結果を格納するキュー
        results = queue.Queue()
        
        def worker(worker_id):
            """ワーカー関数"""
            start_time = time.time()
            
            # テキスト分析を実行
            text = f"This is test text from worker {worker_id}. " * 100
            result = self.analyzer.analyze_text(text)
            
            end_time = time.time()
            duration = end_time - start_time
            
            results.put({
                'worker_id': worker_id,
                'duration': duration,
                'word_count': result.word_count
            })
        
        # 複数のスレッドで並行実行
        threads = []
        num_threads = 10
        
        start_time = time.time()
        
        for i in range(num_threads):
            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # すべてのスレッドの完了を待機
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        total_duration = end_time - start_time
        
        # 結果を収集
        worker_results = []
        while not results.empty():
            worker_results.append(results.get())
        
        # 結果の確認
        self.assertEqual(len(worker_results), num_threads)
        
        # パフォーマンスの確認
        self.assertLess(total_duration, 5.0, f"Concurrent operations took {total_duration:.2f} seconds")
        
        print(f"Concurrent operations completed in {total_duration:.2f} seconds")
        print(f"Average duration per worker: {sum(r['duration'] for r in worker_results) / len(worker_results):.2f} seconds")

if __name__ == '__main__':
    unittest.main()
