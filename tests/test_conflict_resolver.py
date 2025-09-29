"""
ConflictResolverのテスト
"""
import unittest
import sys
import os

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sync_system.conflict_resolver import ConflictResolver

class TestConflictResolver(unittest.TestCase):
    """ConflictResolverのテストクラス"""
    
    def setUp(self):
        """テストの前処理"""
        self.resolver = ConflictResolver()
    
    def test_detect_conflict_title(self):
        """タイトル競合の検出テスト"""
        notion_content = {
            'title': 'Notion Title',
            'content': 'Same content',
            'last_edited_time': '2024-01-01T00:00:00Z'
        }
        
        obsidian_content = {
            'title': 'Obsidian Title',
            'content': 'Same content',
            'modified_time': '2024-01-01T00:00:00Z'
        }
        
        conflicts = self.resolver.detect_conflict(notion_content, obsidian_content)
        
        self.assertIsInstance(conflicts, list)
        self.assertGreater(len(conflicts), 0)
        
        # タイトル競合が検出されることを確認
        title_conflicts = [c for c in conflicts if c['type'] == 'title_conflict']
        self.assertGreater(len(title_conflicts), 0)
    
    def test_detect_conflict_content(self):
        """コンテンツ競合の検出テスト"""
        notion_content = {
            'title': 'Same Title',
            'content': 'Notion content',
            'last_edited_time': '2024-01-01T00:00:00Z'
        }
        
        obsidian_content = {
            'title': 'Same Title',
            'content': 'Obsidian content',
            'modified_time': '2024-01-01T00:00:00Z'
        }
        
        conflicts = self.resolver.detect_conflict(notion_content, obsidian_content)
        
        self.assertIsInstance(conflicts, list)
        self.assertGreater(len(conflicts), 0)
        
        # コンテンツ競合が検出されることを確認
        content_conflicts = [c for c in conflicts if c['type'] == 'content_conflict']
        self.assertGreater(len(content_conflicts), 0)
    
    def test_resolve_conflict_notion_priority(self):
        """Notion優先での競合解決テスト"""
        conflict = {
            'type': 'title_conflict',
            'field': 'title',
            'notion_value': 'Notion Title',
            'obsidian_value': 'Obsidian Title',
            'notion_timestamp': '2024-01-01T00:00:00Z',
            'obsidian_timestamp': '2024-01-01T00:00:00Z',
            'severity': 'medium'
        }
        
        resolution = self.resolver.resolve_conflict(conflict, 'notion_priority')
        
        self.assertIsNotNone(resolution)
        self.assertEqual(resolution['resolved_value'], 'Notion Title')
        self.assertEqual(resolution['resolution_reason'], 'Notion priority rule')
        self.assertFalse(resolution['requires_user_input'])
    
    def test_resolve_conflict_obsidian_priority(self):
        """Obsidian優先での競合解決テスト"""
        conflict = {
            'type': 'title_conflict',
            'field': 'title',
            'notion_value': 'Notion Title',
            'obsidian_value': 'Obsidian Title',
            'notion_timestamp': '2024-01-01T00:00:00Z',
            'obsidian_timestamp': '2024-01-01T00:00:00Z',
            'severity': 'medium'
        }
        
        resolution = self.resolver.resolve_conflict(conflict, 'obsidian_priority')
        
        self.assertIsNotNone(resolution)
        self.assertEqual(resolution['resolved_value'], 'Obsidian Title')
        self.assertEqual(resolution['resolution_reason'], 'Obsidian priority rule')
        self.assertFalse(resolution['requires_user_input'])
    
    def test_resolve_conflict_user_choice(self):
        """ユーザー選択での競合解決テスト"""
        conflict = {
            'type': 'title_conflict',
            'field': 'title',
            'notion_value': 'Notion Title',
            'obsidian_value': 'Obsidian Title',
            'notion_timestamp': '2024-01-01T00:00:00Z',
            'obsidian_timestamp': '2024-01-01T00:00:00Z',
            'severity': 'medium'
        }
        
        resolution = self.resolver.resolve_conflict(conflict, 'user_choice')
        
        self.assertIsNotNone(resolution)
        self.assertIsNone(resolution['resolved_value'])
        self.assertTrue(resolution['requires_user_input'])
        self.assertIn('options', resolution)
        self.assertEqual(len(resolution['options']), 3)
    
    def test_resolve_multiple_conflicts(self):
        """複数競合の解決テスト"""
        conflicts = [
            {
                'type': 'title_conflict',
                'field': 'title',
                'notion_value': 'Notion Title',
                'obsidian_value': 'Obsidian Title',
                'notion_timestamp': '2024-01-01T00:00:00Z',
                'obsidian_timestamp': '2024-01-01T00:00:00Z',
                'severity': 'medium'
            },
            {
                'type': 'content_conflict',
                'field': 'content',
                'notion_value': 'Notion content',
                'obsidian_value': 'Obsidian content',
                'notion_timestamp': '2024-01-01T00:00:00Z',
                'obsidian_timestamp': '2024-01-01T00:00:00Z',
                'severity': 'high'
            }
        ]
        
        resolutions = self.resolver.resolve_multiple_conflicts(conflicts, 'notion_priority')
        
        self.assertIsInstance(resolutions, list)
        self.assertEqual(len(resolutions), 2)
        
        for resolution in resolutions:
            self.assertIn('conflict', resolution)
            self.assertIn('resolution', resolution)
    
    def test_get_conflict_stats(self):
        """競合統計の取得テスト"""
        # テスト用の競合履歴を追加
        self.resolver.conflict_history = [
            {
                'conflict': {'type': 'title_conflict', 'severity': 'medium'},
                'resolution': {'requires_user_input': False},
                'strategy': 'notion_priority',
                'resolved_at': '2024-01-01T00:00:00Z'
            },
            {
                'conflict': {'type': 'content_conflict', 'severity': 'high'},
                'resolution': {'requires_user_input': True},
                'strategy': 'user_choice',
                'resolved_at': '2024-01-01T00:00:00Z'
            }
        ]
        
        stats = self.resolver.get_conflict_stats()
        
        self.assertIsNotNone(stats)
        self.assertEqual(stats['total_conflicts'], 2)
        self.assertEqual(stats['resolved_conflicts'], 1)
        self.assertEqual(stats['unresolved_conflicts'], 1)
        self.assertEqual(stats['resolution_rate'], 0.5)

if __name__ == '__main__':
    unittest.main()
