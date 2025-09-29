"""
ObsidianMarkdownParserのテスト
"""
import unittest
import sys
import os

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from obsidian_integration.markdown_parser import ObsidianMarkdownParser

class TestObsidianMarkdownParser(unittest.TestCase):
    """ObsidianMarkdownParserのテストクラス"""
    
    def setUp(self):
        """テストの前処理"""
        self.parser = ObsidianMarkdownParser()
    
    def test_parse_file_basic(self):
        """基本的なファイル解析のテスト"""
        content = """# Test Note

This is a test note with some content.

## Subsection

- Item 1
- Item 2

[[Related Note]]
#test #note"""
        
        result = self.parser.parse_file("/test/path.md", content)
        
        self.assertIsNotNone(result)
        self.assertIn('file_info', result)
        self.assertIn('content', result)
        self.assertIn('links', result)
        self.assertIn('tags', result)
        self.assertIn('metadata', result)
    
    def test_parse_frontmatter(self):
        """フロントマターの解析テスト"""
        content = """---
title: Test Note
tags: [test, note]
created: 2024-01-01
---

# Test Note

This is a test note."""
        
        result = self.parser.parse_file("/test/path.md", content)
        
        self.assertIsNotNone(result)
        self.assertIn('frontmatter', result)
        frontmatter = result['frontmatter']
        self.assertIn('title', frontmatter)
        self.assertIn('tags', frontmatter)
        self.assertEqual(frontmatter['title'], 'Test Note')
    
    def test_parse_headings(self):
        """見出しの解析テスト"""
        content = """# Heading 1

## Heading 2

### Heading 3

Some content here."""
        
        result = self.parser.parse_file("/test/path.md", content)
        
        self.assertIsNotNone(result)
        self.assertIn('content', result)
        headings = result['content']['headings']
        
        self.assertEqual(len(headings), 3)
        self.assertEqual(headings[0]['level'], 1)
        self.assertEqual(headings[0]['text'], 'Heading 1')
        self.assertEqual(headings[1]['level'], 2)
        self.assertEqual(headings[1]['text'], 'Heading 2')
        self.assertEqual(headings[2]['level'], 3)
        self.assertEqual(headings[2]['text'], 'Heading 3')
    
    def test_parse_links(self):
        """リンクの解析テスト"""
        content = """# Test Note

This is a test note with [[Obsidian Link]] and [Markdown Link](https://example.com).

Another [[Another Link]] here."""
        
        result = self.parser.parse_file("/test/path.md", content)
        
        self.assertIsNotNone(result)
        self.assertIn('links', result)
        links = result['links']
        
        self.assertGreaterEqual(len(links), 2)
        
        # Obsidianリンクの確認
        obsidian_links = [link for link in links if link['type'] == 'obsidian_link']
        self.assertGreaterEqual(len(obsidian_links), 2)
        
        # Markdownリンクの確認
        markdown_links = [link for link in links if link['type'] == 'markdown_link']
        self.assertGreaterEqual(len(markdown_links), 1)
    
    def test_parse_tags(self):
        """タグの解析テスト"""
        content = """# Test Note

This is a test note with #test and #note tags.

Also has #nested/tag here."""
        
        result = self.parser.parse_file("/test/path.md", content)
        
        self.assertIsNotNone(result)
        self.assertIn('tags', result)
        tags = result['tags']
        
        self.assertGreaterEqual(len(tags), 3)
        
        tag_names = [tag['tag'] for tag in tags]
        self.assertIn('test', tag_names)
        self.assertIn('note', tag_names)
        self.assertIn('nested/tag', tag_names)
    
    def test_parse_lists(self):
        """リストの解析テスト"""
        content = """# Test Note

- Unordered item 1
- Unordered item 2

1. Ordered item 1
2. Ordered item 2"""
        
        result = self.parser.parse_file("/test/path.md", content)
        
        self.assertIsNotNone(result)
        self.assertIn('content', result)
        lists = result['content']['lists']
        
        self.assertGreaterEqual(len(lists), 2)
        
        # 箇条書きリストの確認
        unordered_lists = [lst for lst in lists if lst['type'] == 'unordered']
        self.assertGreaterEqual(len(unordered_lists), 1)
        
        # 番号付きリストの確認
        ordered_lists = [lst for lst in lists if lst['type'] == 'ordered']
        self.assertGreaterEqual(len(ordered_lists), 1)
    
    def test_parse_code_blocks(self):
        """コードブロックの解析テスト"""
        content = """# Test Note

```python
def hello():
    print("Hello, World!")
```

```javascript
console.log("Hello, World!");
```"""
        
        result = self.parser.parse_file("/test/path.md", content)
        
        self.assertIsNotNone(result)
        self.assertIn('code_blocks', result)
        code_blocks = result['code_blocks']
        
        self.assertEqual(len(code_blocks), 2)
        self.assertEqual(code_blocks[0]['language'], 'python')
        self.assertEqual(code_blocks[1]['language'], 'javascript')
    
    def test_count_words(self):
        """単語数のカウントテスト"""
        content = """# Test Note

This is a test note with some content.

```python
def hello():
    print("Hello, World!")
```

More content here."""
        
        result = self.parser.parse_file("/test/path.md", content)
        
        self.assertIsNotNone(result)
        self.assertIn('metadata', result)
        word_count = result['metadata']['word_count']
        
        self.assertGreater(word_count, 0)
        # コードブロックは除外されるので、期待値より少なくなる
        self.assertLess(word_count, 20)
    
    def test_extract_metadata(self):
        """メタデータの抽出テスト"""
        content = """# Test Note

This is a test note with [[Link]] and #test #note tags."""
        
        result = self.parser.parse_file("/test/path.md", content)
        metadata = self.parser.extract_metadata(result)
        
        self.assertIsNotNone(metadata)
        self.assertIn('title', metadata)
        self.assertIn('word_count', metadata)
        self.assertIn('link_count', metadata)
        self.assertIn('tag_count', metadata)
        
        self.assertEqual(metadata['title'], 'test/path.md')
        self.assertGreater(metadata['word_count'], 0)
        self.assertGreater(metadata['link_count'], 0)
        self.assertGreater(metadata['tag_count'], 0)
    
    def test_get_linked_files(self):
        """リンクされたファイルの取得テスト"""
        content = """# Test Note

This note links to [[Note 1]] and [[Note 2]].

Also has [External Link](https://example.com)."""
        
        result = self.parser.parse_file("/test/path.md", content)
        linked_files = self.parser.get_linked_files(result)
        
        self.assertIsNotNone(linked_files)
        self.assertEqual(len(linked_files), 2)
        self.assertIn('Note 1', linked_files)
        self.assertIn('Note 2', linked_files)
    
    def test_get_tags(self):
        """タグの取得テスト"""
        content = """# Test Note

This note has #test #note #nested/tag tags."""
        
        result = self.parser.parse_file("/test/path.md", content)
        tags = self.parser.get_tags(result)
        
        self.assertIsNotNone(tags)
        self.assertEqual(len(tags), 3)
        self.assertIn('test', tags)
        self.assertIn('note', tags)
        self.assertIn('nested/tag', tags)

if __name__ == '__main__':
    unittest.main()
