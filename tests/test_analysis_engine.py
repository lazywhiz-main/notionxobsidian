"""
AnalysisEngineのテスト
"""
import unittest
import sys
import os
import asyncio

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis_engine.analysis_engine import AnalysisEngine

class TestAnalysisEngine(unittest.TestCase):
    """AnalysisEngineのテストクラス"""
    
    def setUp(self):
        """テストの前処理"""
        self.engine = AnalysisEngine()
    
    def test_engine_initialization(self):
        """エンジンの初期化テスト"""
        self.assertIsNotNone(self.engine.content_analyzer)
        self.assertIsNotNone(self.engine.insight_generator)
        self.assertIsNotNone(self.engine.recommendation_system)
        self.assertFalse(self.engine.running)
    
    def test_analyze_content_basic(self):
        """基本的なコンテンツ分析のテスト"""
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
            result = loop.run_until_complete(self.engine.analyze_content(content_list))
            
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
    
    def test_analyze_content_empty(self):
        """空のコンテンツリストの分析テスト"""
        content_list = []
        
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(self.engine.analyze_content(content_list))
            
            self.assertIsNotNone(result)
            self.assertIn('analysis_id', result)
            self.assertIn('results', result)
            self.assertIn('summary', result)
            
            # 空のリストでも結果が生成されることを確認
            results = result['results']
            self.assertIsInstance(results['similarity'], list)
            self.assertIsInstance(results['duplicates'], list)
            self.assertIsInstance(results['topics'], list)
            
        finally:
            loop.close()
    
    def test_analyze_content_single_item(self):
        """単一アイテムの分析テスト"""
        content_list = [
            {
                'id': 'content_1',
                'title': 'Single Test Content',
                'content': 'This is a single test content for analysis.',
                'source': 'notion'
            }
        ]
        
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(self.engine.analyze_content(content_list))
            
            self.assertIsNotNone(result)
            self.assertIn('analysis_id', result)
            self.assertIn('results', result)
            self.assertIn('summary', result)
            
            # 単一アイテムでも分析が実行されることを確認
            results = result['results']
            self.assertIsInstance(results['similarity'], list)
            self.assertIsInstance(results['duplicates'], list)
            self.assertIsInstance(results['topics'], list)
            
        finally:
            loop.close()
    
    def test_analyze_content_with_duplicates(self):
        """重複コンテンツの分析テスト"""
        content_list = [
            {
                'id': 'content_1',
                'title': 'Duplicate Content',
                'content': 'This is a test content for analysis.',
                'source': 'notion'
            },
            {
                'id': 'content_2',
                'title': 'Duplicate Content',
                'content': 'This is a test content for analysis.',
                'source': 'obsidian'
            }
        ]
        
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(self.engine.analyze_content(content_list))
            
            self.assertIsNotNone(result)
            self.assertIn('analysis_id', result)
            self.assertIn('results', result)
            self.assertIn('summary', result)
            
            # 重複が検出されることを確認
            results = result['results']
            self.assertGreater(len(results['duplicates']), 0)
            
        finally:
            loop.close()
    
    def test_analyze_content_with_similar_content(self):
        """類似コンテンツの分析テスト"""
        content_list = [
            {
                'id': 'content_1',
                'title': 'Similar Content 1',
                'content': 'This is a test content for analysis with some keywords.',
                'source': 'notion'
            },
            {
                'id': 'content_2',
                'title': 'Similar Content 2',
                'content': 'This is another test content for analysis with similar keywords.',
                'source': 'obsidian'
            },
            {
                'id': 'content_3',
                'title': 'Different Content',
                'content': 'This is completely different content about something else.',
                'source': 'notion'
            }
        ]
        
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(self.engine.analyze_content(content_list))
            
            self.assertIsNotNone(result)
            self.assertIn('analysis_id', result)
            self.assertIn('results', result)
            self.assertIn('summary', result)
            
            # 類似コンテンツが検出されることを確認
            results = result['results']
            self.assertGreater(len(results['similarity']), 0)
            
        finally:
            loop.close()
    
    def test_get_analysis_result(self):
        """分析結果の取得テスト"""
        content_list = [
            {
                'id': 'content_1',
                'title': 'Test Content',
                'content': 'This is a test content for analysis.',
                'source': 'notion'
            }
        ]
        
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(self.engine.analyze_content(content_list))
            analysis_id = result['analysis_id']
            
            # 分析結果を取得
            retrieved_result = self.engine.get_analysis_result(analysis_id)
            
            self.assertIsNotNone(retrieved_result)
            self.assertEqual(retrieved_result, result['results'])
            
        finally:
            loop.close()
    
    def test_get_recent_analyses(self):
        """最近の分析結果の取得テスト"""
        content_list = [
            {
                'id': 'content_1',
                'title': 'Test Content',
                'content': 'This is a test content for analysis.',
                'source': 'notion'
            }
        ]
        
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # 複数の分析を実行
            result1 = loop.run_until_complete(self.engine.analyze_content(content_list))
            result2 = loop.run_until_complete(self.engine.analyze_content(content_list))
            
            # 最近の分析結果を取得
            recent_analyses = self.engine.get_recent_analyses(limit=2)
            
            self.assertIsInstance(recent_analyses, list)
            self.assertGreaterEqual(len(recent_analyses), 2)
            
        finally:
            loop.close()
    
    def test_clear_cache(self):
        """キャッシュのクリアテスト"""
        content_list = [
            {
                'id': 'content_1',
                'title': 'Test Content',
                'content': 'This is a test content for analysis.',
                'source': 'notion'
            }
        ]
        
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # 分析を実行
            result = loop.run_until_complete(self.engine.analyze_content(content_list))
            analysis_id = result['analysis_id']
            
            # キャッシュをクリア
            self.engine.clear_cache()
            
            # 分析結果が取得できないことを確認
            retrieved_result = self.engine.get_analysis_result(analysis_id)
            self.assertIsNone(retrieved_result)
            
        finally:
            loop.close()
    
    def test_queue_analysis(self):
        """分析キューのテスト"""
        content_list = [
            {
                'id': 'content_1',
                'title': 'Test Content',
                'content': 'This is a test content for analysis.',
                'source': 'notion'
            }
        ]
        
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # 分析をキューに追加
            loop.run_until_complete(self.engine.queue_analysis(content_list))
            
            # キューに追加されたことを確認
            self.assertGreater(self.engine.analysis_queue.qsize(), 0)
            
        finally:
            loop.close()

if __name__ == '__main__':
    unittest.main()
