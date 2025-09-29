"""
NotionClientのテスト
"""
import unittest
import sys
import os
import asyncio
from unittest.mock import Mock, patch

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from notion_integration.notion_client import NotionClient

class TestNotionClient(unittest.TestCase):
    """NotionClientのテストクラス"""
    
    def setUp(self):
        """テストの前処理"""
        self.client = NotionClient("test_token")
    
    def test_client_initialization(self):
        """クライアントの初期化テスト"""
        self.assertEqual(self.client.token, "test_token")
        self.assertIsNone(self.client.client)
        self.assertFalse(self.client.running)
        self.assertIsInstance(self.client.database_ids, dict)
    
    def test_extract_title(self):
        """タイトルの抽出テスト"""
        page = {
            'properties': {
                'title': {
                    'title': [{'text': {'content': 'Test Page Title'}}]
                }
            }
        }
        
        title = self.client._extract_title(page)
        self.assertEqual(title, 'Test Page Title')
    
    def test_extract_title_empty(self):
        """空のタイトルの抽出テスト"""
        page = {
            'properties': {
                'title': {
                    'title': []
                }
            }
        }
        
        title = self.client._extract_title(page)
        self.assertEqual(title, 'Untitled')
    
    def test_extract_title_no_properties(self):
        """プロパティがない場合のタイトル抽出テスト"""
        page = {}
        
        title = self.client._extract_title(page)
        self.assertEqual(title, 'Untitled')
    
    def test_extract_content_paragraph(self):
        """段落ブロックのコンテンツ抽出テスト"""
        blocks = {
            'results': [
                {
                    'type': 'paragraph',
                    'paragraph': {
                        'rich_text': [{'text': {'content': 'This is a test paragraph.'}}]
                    }
                }
            ]
        }
        
        content = self.client._extract_content(blocks)
        self.assertEqual(content, 'This is a test paragraph.')
    
    def test_extract_content_heading(self):
        """見出しブロックのコンテンツ抽出テスト"""
        blocks = {
            'results': [
                {
                    'type': 'heading_1',
                    'heading_1': {
                        'rich_text': [{'text': {'content': 'Test Heading'}}]
                    }
                }
            ]
        }
        
        content = self.client._extract_content(blocks)
        self.assertEqual(content, '# Test Heading')
    
    def test_extract_content_list(self):
        """リストブロックのコンテンツ抽出テスト"""
        blocks = {
            'results': [
                {
                    'type': 'bulleted_list_item',
                    'bulleted_list_item': {
                        'rich_text': [{'text': {'content': 'List item 1'}}]
                    }
                },
                {
                    'type': 'numbered_list_item',
                    'numbered_list_item': {
                        'rich_text': [{'text': {'content': 'Numbered item 1'}}]
                    }
                }
            ]
        }
        
        content = self.client._extract_content(blocks)
        self.assertIn('- List item 1', content)
        self.assertIn('1. Numbered item 1', content)
    
    def test_extract_content_quote(self):
        """引用ブロックのコンテンツ抽出テスト"""
        blocks = {
            'results': [
                {
                    'type': 'quote',
                    'quote': {
                        'rich_text': [{'text': {'content': 'This is a quote.'}}]
                    }
                }
            ]
        }
        
        content = self.client._extract_content(blocks)
        self.assertEqual(content, '> This is a quote.')
    
    def test_extract_content_code(self):
        """コードブロックのコンテンツ抽出テスト"""
        blocks = {
            'results': [
                {
                    'type': 'code',
                    'code': {
                        'rich_text': [{'text': {'content': 'print("Hello, World!")'}}],
                        'language': 'python'
                    }
                }
            ]
        }
        
        content = self.client._extract_content(blocks)
        self.assertIn('```python', content)
        self.assertIn('print("Hello, World!")', content)
        self.assertIn('```', content)
    
    def test_extract_content_empty(self):
        """空のブロックのコンテンツ抽出テスト"""
        blocks = {'results': []}
        
        content = self.client._extract_content(blocks)
        self.assertEqual(content, '')
    
    def test_extract_rich_text(self):
        """リッチテキストの抽出テスト"""
        rich_text_array = [
            {'text': {'content': 'Hello'}},
            {'text': {'content': ' '}},
            {'text': {'content': 'World'}}
        ]
        
        text = self.client._extract_rich_text(rich_text_array)
        self.assertEqual(text, 'Hello World')
    
    def test_extract_rich_text_empty(self):
        """空のリッチテキストの抽出テスト"""
        rich_text_array = []
        
        text = self.client._extract_rich_text(rich_text_array)
        self.assertEqual(text, '')
    
    def test_extract_rich_text_no_content(self):
        """コンテンツがないリッチテキストの抽出テスト"""
        rich_text_array = [
            {'text': {'content': ''}},
            {'text': {'content': 'Hello'}},
            {'text': {'content': ''}}
        ]
        
        text = self.client._extract_rich_text(rich_text_array)
        self.assertEqual(text, 'Hello')
    
    def test_get_sync_status(self):
        """同期ステータスの取得テスト"""
        status = self.client.get_sync_status()
        
        self.assertIsNotNone(status)
        self.assertIn('success_count', status)
        self.assertIn('pending_count', status)
        self.assertIn('error_count', status)
        self.assertIn('last_sync', status)
    
    def test_get_sync_history(self):
        """同期履歴の取得テスト"""
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            history = loop.run_until_complete(self.client.get_sync_history(limit=10))
            
            self.assertIsInstance(history, list)
            
        finally:
            loop.close()
    
    def test_get_database_properties(self):
        """データベースプロパティの取得テスト"""
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            properties = loop.run_until_complete(
                self.client.get_database_properties("test_database_id")
            )
            
            self.assertIsInstance(properties, dict)
            
        finally:
            loop.close()
    
    def test_search_content(self):
        """コンテンツの検索テスト"""
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            results = loop.run_until_complete(
                self.client.search_content("test query", limit=20)
            )
            
            self.assertIsInstance(results, list)
            
        finally:
            loop.close()
    
    def test_get_pages(self):
        """ページ一覧の取得テスト"""
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            pages = loop.run_until_complete(self.client.get_pages(limit=100))
            
            self.assertIsInstance(pages, list)
            
        finally:
            loop.close()
    
    def test_get_page_content(self):
        """ページコンテンツの取得テスト"""
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            content = loop.run_until_complete(
                self.client.get_page_content("test_page_id")
            )
            
            self.assertIsInstance(content, dict)
            
        finally:
            loop.close()
    
    def test_create_insight_page(self):
        """インサイトページの作成テスト"""
        insight_data = {
            'title': 'Test Insight',
            'type': 'similarity',
            'confidence': 0.8
        }
        
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            page_id = loop.run_until_complete(
                self.client.create_insight_page(insight_data)
            )
            
            # データベースが設定されていない場合はNoneが返される
            self.assertIsNone(page_id)
            
        finally:
            loop.close()
    
    def test_create_task_page(self):
        """タスクページの作成テスト"""
        task_data = {
            'title': 'Test Task',
            'priority': 'high',
            'estimated_time': '10分'
        }
        
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            page_id = loop.run_until_complete(
                self.client.create_task_page(task_data)
            )
            
            # データベースが設定されていない場合はNoneが返される
            self.assertIsNone(page_id)
            
        finally:
            loop.close()
    
    def test_update_sync_status(self):
        """同期ステータスの更新テスト"""
        status_data = {
            'success_count': 5,
            'pending_count': 2,
            'error_count': 0
        }
        
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                self.client.update_sync_status(status_data)
            )
            
            # ページIDが設定されていない場合はFalseが返される
            self.assertFalse(result)
            
        finally:
            loop.close()

if __name__ == '__main__':
    unittest.main()
