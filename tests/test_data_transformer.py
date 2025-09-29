"""
DataTransformerのテスト
"""
import unittest
import sys
import os

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sync_system.data_transformer import DataTransformer

class TestDataTransformer(unittest.TestCase):
    """DataTransformerのテストクラス"""
    
    def setUp(self):
        """テストの前処理"""
        self.transformer = DataTransformer()
    
    def test_convert_notion_to_obsidian(self):
        """NotionからObsidianへの変換テスト"""
        notion_content = {
            'page': {
                'id': 'test_page_id',
                'created_time': '2024-01-01T00:00:00Z',
                'last_edited_time': '2024-01-01T00:00:00Z',
                'properties': {
                    'title': {
                        'title': [{'text': {'content': 'Test Page'}}]
                    }
                }
            },
            'blocks': {
                'results': [
                    {
                        'type': 'paragraph',
                        'paragraph': {
                            'rich_text': [{'text': {'content': 'This is a test paragraph.'}}]
                        }
                    }
                ]
            }
        }
        
        result = self.transformer.convert_notion_to_obsidian(notion_content)
        
        self.assertIsNotNone(result)
        self.assertIn('title', result)
        self.assertIn('content', result)
        self.assertIn('frontmatter', result)
        self.assertEqual(result['title'], 'Test Page')
    
    def test_convert_obsidian_to_notion(self):
        """ObsidianからNotionへの変換テスト"""
        obsidian_content = {
            'title': 'Test Note',
            'content': '# Test Note\n\nThis is a test note.',
            'frontmatter': {
                'tags': ['test', 'note'],
                'obsidian_id': 'test_note_id'
            }
        }
        
        result = self.transformer.convert_obsidian_to_notion(obsidian_content)
        
        self.assertIsNotNone(result)
        self.assertIn('title', result)
        self.assertIn('blocks', result)
        self.assertIn('properties', result)
        self.assertEqual(result['title'], 'Test Note')
    
    def test_extract_obsidian_frontmatter(self):
        """Obsidianフロントマターの抽出テスト"""
        content = """---
title: Test Note
tags: [test, note]
created: 2024-01-01
---

# Test Note

This is a test note."""
        
        frontmatter = self.transformer.extract_obsidian_frontmatter(content)
        
        self.assertIsNotNone(frontmatter)
        self.assertIn('title', frontmatter)
        self.assertIn('tags', frontmatter)
        self.assertEqual(frontmatter['title'], 'Test Note')
    
    def test_create_obsidian_frontmatter(self):
        """Obsidianフロントマターの作成テスト"""
        metadata = {
            'title': 'Test Note',
            'tags': ['test', 'note'],
            'created': '2024-01-01'
        }
        
        frontmatter = self.transformer.create_obsidian_frontmatter(metadata)
        
        self.assertIsNotNone(frontmatter)
        self.assertIn('---', frontmatter)
        self.assertIn('title: Test Note', frontmatter)
        self.assertIn('tags: test, note', frontmatter)

if __name__ == '__main__':
    unittest.main()
