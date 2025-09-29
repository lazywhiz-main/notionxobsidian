"""
InsightGeneratorのテスト
"""
import unittest
import sys
import os

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis_engine.insight_generator import InsightGenerator, Insight

class TestInsightGenerator(unittest.TestCase):
    """InsightGeneratorのテストクラス"""
    
    def setUp(self):
        """テストの前処理"""
        self.generator = InsightGenerator()
    
    def test_generate_insights_similarity(self):
        """類似度インサイトの生成テスト"""
        analysis_results = {
            'similarity': [
                {
                    'content1_index': 0,
                    'content2_index': 1,
                    'similarity': 0.85,
                    'content1_preview': 'Test content 1',
                    'content2_preview': 'Test content 2'
                }
            ]
        }
        
        insights = self.generator.generate_insights(analysis_results)
        
        self.assertIsInstance(insights, list)
        self.assertGreater(len(insights), 0)
        
        similarity_insights = [i for i in insights if i.type == 'similarity']
        self.assertGreater(len(similarity_insights), 0)
        
        insight = similarity_insights[0]
        self.assertEqual(insight.type, 'similarity')
        self.assertEqual(insight.confidence, 0.85)
        self.assertIn('類似度', insight.title)
    
    def test_generate_insights_duplicate(self):
        """重複インサイトの生成テスト"""
        analysis_results = {
            'duplicates': [
                {
                    'text1_index': 0,
                    'text2_index': 1,
                    'similarity': 0.95,
                    'text1_preview': 'Duplicate content 1',
                    'text2_preview': 'Duplicate content 2'
                }
            ]
        }
        
        insights = self.generator.generate_insights(analysis_results)
        
        self.assertIsInstance(insights, list)
        self.assertGreater(len(insights), 0)
        
        duplicate_insights = [i for i in insights if i.type == 'duplicate']
        self.assertGreater(len(duplicate_insights), 0)
        
        insight = duplicate_insights[0]
        self.assertEqual(insight.type, 'duplicate')
        self.assertEqual(insight.confidence, 0.95)
        self.assertIn('重複', insight.title)
    
    def test_generate_insights_topic(self):
        """トピックインサイトの生成テスト"""
        analysis_results = {
            'topics': [
                {
                    'topic': 'AI',
                    'count': 5,
                    'confidence': 0.8
                }
            ]
        }
        
        insights = self.generator.generate_insights(analysis_results)
        
        self.assertIsInstance(insights, list)
        self.assertGreater(len(insights), 0)
        
        topic_insights = [i for i in insights if i.type == 'topic']
        self.assertGreater(len(topic_insights), 0)
        
        insight = topic_insights[0]
        self.assertEqual(insight.type, 'topic')
        self.assertEqual(insight.confidence, 0.8)
        self.assertIn('AI', insight.title)
    
    def test_generate_insights_sentiment(self):
        """感情分析インサイトの生成テスト"""
        analysis_results = {
            'sentiment': [
                {
                    'content_id': 'test_content',
                    'content_title': 'Test Content',
                    'sentiment': 'POSITIVE',
                    'confidence': 0.9
                }
            ]
        }
        
        insights = self.generator.generate_insights(analysis_results)
        
        self.assertIsInstance(insights, list)
        self.assertGreater(len(insights), 0)
        
        sentiment_insights = [i for i in insights if i.type == 'sentiment']
        self.assertGreater(len(sentiment_insights), 0)
        
        insight = sentiment_insights[0]
        self.assertEqual(insight.type, 'sentiment')
        self.assertEqual(insight.confidence, 0.9)
        self.assertIn('POSITIVE', insight.title)
    
    def test_generate_insights_readability(self):
        """可読性インサイトの生成テスト"""
        analysis_results = {
            'readability': [
                {
                    'content_id': 'test_content',
                    'content_title': 'Test Content',
                    'readability_score': 0.3
                }
            ]
        }
        
        insights = self.generator.generate_insights(analysis_results)
        
        self.assertIsInstance(insights, list)
        self.assertGreater(len(insights), 0)
        
        readability_insights = [i for i in insights if i.type == 'readability']
        self.assertGreater(len(readability_insights), 0)
        
        insight = readability_insights[0]
        self.assertEqual(insight.type, 'readability')
        self.assertEqual(insight.confidence, 0.8)
        self.assertIn('可読性', insight.title)
    
    def test_generate_recommendations(self):
        """推奨アクションの生成テスト"""
        insights = [
            Insight(
                id='insight_1',
                type='similarity',
                title='Similarity Insight',
                content='Test insight',
                confidence=0.8,
                source_data={},
                created_at=time.time(),
                tags=['similarity']
            ),
            Insight(
                id='insight_2',
                type='duplicate',
                title='Duplicate Insight',
                content='Test insight',
                confidence=0.9,
                source_data={},
                created_at=time.time(),
                tags=['duplicate']
            )
        ]
        
        recommendations = self.generator.generate_recommendations(insights)
        
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
        
        # 推奨アクションのタイプを確認
        action_types = [rec.action_type for rec in recommendations]
        self.assertIn('create_link', action_types)
        self.assertIn('merge_duplicate', action_types)
    
    def test_get_insight_summary(self):
        """インサイトサマリーの取得テスト"""
        insights = [
            Insight(
                id='insight_1',
                type='similarity',
                title='Similarity Insight',
                content='Test insight',
                confidence=0.8,
                source_data={},
                created_at=time.time(),
                tags=['similarity']
            ),
            Insight(
                id='insight_2',
                type='duplicate',
                title='Duplicate Insight',
                content='Test insight',
                confidence=0.9,
                source_data={},
                created_at=time.time(),
                tags=['duplicate']
            )
        ]
        
        summary = self.generator.get_insight_summary(insights)
        
        self.assertIsNotNone(summary)
        self.assertEqual(summary['total_insights'], 2)
        self.assertIn('insights_by_type', summary)
        self.assertIn('high_confidence_insights', summary)
        self.assertIn('recommended_actions', summary)
        
        # タイプ別の集計を確認
        self.assertEqual(summary['insights_by_type']['similarity'], 1)
        self.assertEqual(summary['insights_by_type']['duplicate'], 1)
        
        # 高信頼度インサイトの集計を確認
        self.assertEqual(summary['high_confidence_insights'], 1)

if __name__ == '__main__':
    import time
    unittest.main()
