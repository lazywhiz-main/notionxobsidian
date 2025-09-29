"""
ContentAnalyzerのテスト
"""
import unittest
import sys
import os

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis_engine.content_analyzer import ContentAnalyzer

class TestContentAnalyzer(unittest.TestCase):
    """ContentAnalyzerのテストクラス"""
    
    def setUp(self):
        """テストの前処理"""
        self.analyzer = ContentAnalyzer()
    
    def test_analyze_text_basic(self):
        """基本的なテキスト分析のテスト"""
        text = "これはテスト用のテキストです。"
        result = self.analyzer.analyze_text(text)
        
        self.assertIsNotNone(result)
        self.assertIn('word_count', result.__dict__)
        self.assertIn('sentence_count', result.__dict__)
        self.assertIn('keywords', result.__dict__)
        self.assertIn('sentiment', result.__dict__)
    
    def test_analyze_text_empty(self):
        """空のテキストのテスト"""
        text = ""
        result = self.analyzer.analyze_text(text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.word_count, 0)
        self.assertEqual(result.sentence_count, 0)
        self.assertEqual(len(result.keywords), 0)
    
    def test_calculate_similarity_identical(self):
        """同一テキストの類似度テスト"""
        text1 = "これはテスト用のテキストです。"
        text2 = "これはテスト用のテキストです。"
        
        similarity = self.analyzer.calculate_similarity(text1, text2)
        self.assertEqual(similarity, 1.0)
    
    def test_calculate_similarity_different(self):
        """異なるテキストの類似度テスト"""
        text1 = "これはテスト用のテキストです。"
        text2 = "これは全く異なる内容のテキストです。"
        
        similarity = self.analyzer.calculate_similarity(text1, text2)
        self.assertGreaterEqual(similarity, 0.0)
        self.assertLessEqual(similarity, 1.0)
    
    def test_detect_duplicates(self):
        """重複検出のテスト"""
        texts = [
            "これはテスト用のテキストです。",
            "これはテスト用のテキストです。",
            "これは別のテキストです。"
        ]
        
        duplicates = self.analyzer.detect_duplicates(texts)
        self.assertIsInstance(duplicates, list)
        # 重複が検出されることを確認
        self.assertGreater(len(duplicates), 0)
    
    def test_find_similar_content(self):
        """類似コンテンツ検索のテスト"""
        target_text = "これはテスト用のテキストです。"
        candidate_texts = [
            "これはテスト用のテキストです。",
            "これは全く異なる内容のテキストです。",
            "これは別のテスト用のテキストです。"
        ]
        
        similar_content = self.analyzer.find_similar_content(target_text, candidate_texts)
        self.assertIsInstance(similar_content, list)
        # 類似コンテンツが検出されることを確認
        self.assertGreater(len(similar_content), 0)

if __name__ == '__main__':
    unittest.main()
