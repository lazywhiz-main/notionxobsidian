"""
RecommendationSystemのテスト
"""
import unittest
import sys
import os
import time

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis_engine.recommendation_system import RecommendationSystem, ActionItem
from analysis_engine.insight_generator import Insight

class TestRecommendationSystem(unittest.TestCase):
    """RecommendationSystemのテストクラス"""
    
    def setUp(self):
        """テストの前処理"""
        self.system = RecommendationSystem()
    
    def test_generate_action_items(self):
        """アクションアイテムの生成テスト"""
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
        
        action_items = self.system.generate_action_items(insights)
        
        self.assertIsInstance(action_items, list)
        self.assertGreater(len(action_items), 0)
        
        # アクションアイテムのプロパティを確認
        for action in action_items:
            self.assertIsInstance(action, ActionItem)
            self.assertIsNotNone(action.title)
            self.assertIsNotNone(action.description)
            self.assertIsNotNone(action.action_type)
            self.assertIsNotNone(action.priority)
            self.assertIsNotNone(action.estimated_time)
            self.assertIsNotNone(action.steps)
            self.assertIsNotNone(action.insight_id)
    
    def test_action_item_priority_calculation(self):
        """アクションアイテムの優先度計算テスト"""
        # 高信頼度のインサイト
        high_confidence_insight = Insight(
            id='insight_1',
            type='similarity',
            title='High Confidence Insight',
            content='Test insight',
            confidence=0.9,
            source_data={},
            created_at=time.time(),
            tags=['similarity']
        )
        
        # 低信頼度のインサイト
        low_confidence_insight = Insight(
            id='insight_2',
            type='similarity',
            title='Low Confidence Insight',
            content='Test insight',
            confidence=0.3,
            source_data={},
            created_at=time.time(),
            tags=['similarity']
        )
        
        action_items = self.system.generate_action_items([high_confidence_insight, low_confidence_insight])
        
        self.assertGreater(len(action_items), 0)
        
        # 高信頼度のインサイトから生成されたアクションの優先度が高いことを確認
        high_priority_actions = [action for action in action_items if action.priority == 'high']
        self.assertGreater(len(high_priority_actions), 0)
    
    def test_action_item_types(self):
        """アクションアイテムのタイプテスト"""
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
            ),
            Insight(
                id='insight_3',
                type='topic',
                title='Topic Insight',
                content='Test insight',
                confidence=0.7,
                source_data={},
                created_at=time.time(),
                tags=['topic']
            ),
            Insight(
                id='insight_4',
                type='readability',
                title='Readability Insight',
                content='Test insight',
                confidence=0.6,
                source_data={},
                created_at=time.time(),
                tags=['readability']
            )
        ]
        
        action_items = self.system.generate_action_items(insights)
        
        self.assertGreater(len(action_items), 0)
        
        # 各タイプのアクションが生成されることを確認
        action_types = [action.action_type for action in action_items]
        self.assertIn('create_link', action_types)
        self.assertIn('merge_duplicate', action_types)
        self.assertIn('organize_by_topic', action_types)
        self.assertIn('improve_readability', action_types)
    
    def test_get_action_summary(self):
        """アクションサマリーの取得テスト"""
        action_items = [
            ActionItem(
                id='action_1',
                title='Test Action 1',
                description='Test description',
                action_type='create_link',
                priority='high',
                estimated_time='5分',
                steps=['Step 1', 'Step 2'],
                status='pending',
                insight_id='insight_1',
                created_at=time.time(),
                updated_at=time.time()
            ),
            ActionItem(
                id='action_2',
                title='Test Action 2',
                description='Test description',
                action_type='merge_duplicate',
                priority='medium',
                estimated_time='15分',
                steps=['Step 1', 'Step 2', 'Step 3'],
                status='pending',
                insight_id='insight_2',
                created_at=time.time(),
                updated_at=time.time()
            )
        ]
        
        summary = self.system.get_action_summary(action_items)
        
        self.assertIsNotNone(summary)
        self.assertEqual(summary['total_actions'], 2)
        self.assertIn('actions_by_priority', summary)
        self.assertIn('actions_by_type', summary)
        self.assertIn('estimated_total_time', summary)
        self.assertIn('high_priority_count', summary)
        
        # 優先度別の集計を確認
        self.assertEqual(summary['actions_by_priority']['high'], 1)
        self.assertEqual(summary['actions_by_priority']['medium'], 1)
        
        # タイプ別の集計を確認
        self.assertEqual(summary['actions_by_type']['create_link'], 1)
        self.assertEqual(summary['actions_by_type']['merge_duplicate'], 1)
        
        # 高優先度アクションの集計を確認
        self.assertEqual(summary['high_priority_count'], 1)
        
        # 推定時間の集計を確認
        self.assertIn('分', summary['estimated_total_time'])
    
    def test_filter_actions_by_priority(self):
        """優先度でのフィルタリングテスト"""
        action_items = [
            ActionItem(
                id='action_1',
                title='High Priority Action',
                description='Test description',
                action_type='create_link',
                priority='high',
                estimated_time='5分',
                steps=['Step 1'],
                status='pending',
                insight_id='insight_1',
                created_at=time.time(),
                updated_at=time.time()
            ),
            ActionItem(
                id='action_2',
                title='Medium Priority Action',
                description='Test description',
                action_type='merge_duplicate',
                priority='medium',
                estimated_time='15分',
                steps=['Step 1'],
                status='pending',
                insight_id='insight_2',
                created_at=time.time(),
                updated_at=time.time()
            )
        ]
        
        high_priority_actions = self.system.filter_actions_by_priority(action_items, 'high')
        medium_priority_actions = self.system.filter_actions_by_priority(action_items, 'medium')
        
        self.assertEqual(len(high_priority_actions), 1)
        self.assertEqual(len(medium_priority_actions), 1)
        self.assertEqual(high_priority_actions[0].title, 'High Priority Action')
        self.assertEqual(medium_priority_actions[0].title, 'Medium Priority Action')
    
    def test_filter_actions_by_type(self):
        """アクションタイプでのフィルタリングテスト"""
        action_items = [
            ActionItem(
                id='action_1',
                title='Link Action',
                description='Test description',
                action_type='create_link',
                priority='high',
                estimated_time='5分',
                steps=['Step 1'],
                status='pending',
                insight_id='insight_1',
                created_at=time.time(),
                updated_at=time.time()
            ),
            ActionItem(
                id='action_2',
                title='Merge Action',
                description='Test description',
                action_type='merge_duplicate',
                priority='medium',
                estimated_time='15分',
                steps=['Step 1'],
                status='pending',
                insight_id='insight_2',
                created_at=time.time(),
                updated_at=time.time()
            )
        ]
        
        link_actions = self.system.filter_actions_by_type(action_items, 'create_link')
        merge_actions = self.system.filter_actions_by_type(action_items, 'merge_duplicate')
        
        self.assertEqual(len(link_actions), 1)
        self.assertEqual(len(merge_actions), 1)
        self.assertEqual(link_actions[0].title, 'Link Action')
        self.assertEqual(merge_actions[0].title, 'Merge Action')
    
    def test_get_next_actions(self):
        """次のアクションの取得テスト"""
        action_items = [
            ActionItem(
                id='action_1',
                title='High Priority Action',
                description='Test description',
                action_type='create_link',
                priority='high',
                estimated_time='5分',
                steps=['Step 1'],
                status='pending',
                insight_id='insight_1',
                created_at=time.time(),
                updated_at=time.time()
            ),
            ActionItem(
                id='action_2',
                title='Medium Priority Action',
                description='Test description',
                action_type='merge_duplicate',
                priority='medium',
                estimated_time='15分',
                steps=['Step 1'],
                status='pending',
                insight_id='insight_2',
                created_at=time.time(),
                updated_at=time.time()
            ),
            ActionItem(
                id='action_3',
                title='Low Priority Action',
                description='Test description',
                action_type='improve_readability',
                priority='low',
                estimated_time='10分',
                steps=['Step 1'],
                status='pending',
                insight_id='insight_3',
                created_at=time.time(),
                updated_at=time.time()
            )
        ]
        
        next_actions = self.system.get_next_actions(action_items, limit=2)
        
        self.assertEqual(len(next_actions), 2)
        # 優先度順にソートされていることを確認
        self.assertEqual(next_actions[0].priority, 'high')
        self.assertEqual(next_actions[1].priority, 'medium')
    
    def test_update_action_status(self):
        """アクションステータスの更新テスト"""
        action_item = ActionItem(
            id='action_1',
            title='Test Action',
            description='Test description',
            action_type='create_link',
            priority='high',
            estimated_time='5分',
            steps=['Step 1'],
            status='pending',
            insight_id='insight_1',
            created_at=time.time(),
            updated_at=time.time()
        )
        
        updated_action = self.system.update_action_status(action_item, 'completed')
        
        self.assertEqual(updated_action.status, 'completed')
        self.assertGreater(updated_action.updated_at, action_item.updated_at)
    
    def test_get_action_progress(self):
        """アクション進捗の取得テスト"""
        action_items = [
            ActionItem(
                id='action_1',
                title='Completed Action',
                description='Test description',
                action_type='create_link',
                priority='high',
                estimated_time='5分',
                steps=['Step 1'],
                status='completed',
                insight_id='insight_1',
                created_at=time.time(),
                updated_at=time.time()
            ),
            ActionItem(
                id='action_2',
                title='In Progress Action',
                description='Test description',
                action_type='merge_duplicate',
                priority='medium',
                estimated_time='15分',
                steps=['Step 1'],
                status='in_progress',
                insight_id='insight_2',
                created_at=time.time(),
                updated_at=time.time()
            ),
            ActionItem(
                id='action_3',
                title='Pending Action',
                description='Test description',
                action_type='improve_readability',
                priority='low',
                estimated_time='10分',
                steps=['Step 1'],
                status='pending',
                insight_id='insight_3',
                created_at=time.time(),
                updated_at=time.time()
            )
        ]
        
        progress = self.system.get_action_progress(action_items)
        
        self.assertIsNotNone(progress)
        self.assertEqual(progress['total_actions'], 3)
        self.assertEqual(progress['completed_actions'], 1)
        self.assertEqual(progress['in_progress_actions'], 1)
        self.assertEqual(progress['pending_actions'], 1)
        self.assertEqual(progress['progress_percentage'], 33.33)

if __name__ == '__main__':
    unittest.main()
