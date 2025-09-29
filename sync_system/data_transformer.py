"""
データ変換器
NotionとObsidian間のデータ変換を行う
"""
import logging
import re
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

class DataTransformer:
    """データ変換クラス"""
    
    def __init__(self):
        self.block_type_mapping = {
            'paragraph': self._convert_paragraph,
            'heading_1': self._convert_heading_1,
            'heading_2': self._convert_heading_2,
            'heading_3': self._convert_heading_3,
            'bulleted_list_item': self._convert_bulleted_list,
            'numbered_list_item': self._convert_numbered_list,
            'quote': self._convert_quote,
            'code': self._convert_code,
            'callout': self._convert_callout,
            'toggle': self._convert_toggle,
            'divider': self._convert_divider
        }
    
    def convert_notion_to_obsidian(self, notion_content: Dict[str, Any]) -> Dict[str, Any]:
        """NotionからObsidianへの変換"""
        try:
            page = notion_content.get('page', {})
            blocks = notion_content.get('blocks', {})
            
            # タイトルの抽出
            title = self._extract_title(page)
            
            # コンテンツの変換
            content = self._convert_blocks_to_markdown(blocks)
            
            # フロントマターの作成
            frontmatter = self._create_frontmatter(page)
            
            return {
                'title': title,
                'content': content,
                'frontmatter': frontmatter,
                'metadata': {
                    'notion_id': page.get('id'),
                    'created_time': page.get('created_time'),
                    'last_edited_time': page.get('last_edited_time'),
                    'source': 'notion'
                }
            }
            
        except Exception as e:
            logger.error(f"Notion to Obsidian conversion failed: {e}")
            return {}
    
    def convert_obsidian_to_notion(self, obsidian_content: Dict[str, Any]) -> Dict[str, Any]:
        """ObsidianからNotionへの変換"""
        try:
            title = obsidian_content.get('title', 'Untitled')
            content = obsidian_content.get('content', '')
            frontmatter = obsidian_content.get('frontmatter', {})
            
            # ブロックの変換
            blocks = self._convert_markdown_to_blocks(content)
            
            # プロパティの作成
            properties = self._create_notion_properties(title, frontmatter)
            
            return {
                'title': title,
                'blocks': blocks,
                'properties': properties,
                'metadata': {
                    'obsidian_id': obsidian_content.get('id'),
                    'file_path': obsidian_content.get('file_path'),
                    'source': 'obsidian'
                }
            }
            
        except Exception as e:
            logger.error(f"Obsidian to Notion conversion failed: {e}")
            return {}
    
    def _extract_title(self, page: Dict[str, Any]) -> str:
        """ページからタイトルを抽出"""
        try:
            properties = page.get('properties', {})
            title_property = properties.get('title', {})
            title_array = title_property.get('title', [])
            
            if title_array:
                return title_array[0].get('text', {}).get('content', 'Untitled')
            return 'Untitled'
            
        except Exception as e:
            logger.error(f"Title extraction failed: {e}")
            return 'Untitled'
    
    def _convert_blocks_to_markdown(self, blocks: Dict[str, Any]) -> str:
        """NotionブロックをMarkdownに変換"""
        try:
            markdown_parts = []
            
            for block in blocks.get('results', []):
                block_type = block.get('type')
                
                if block_type in self.block_type_mapping:
                    converter = self.block_type_mapping[block_type]
                    markdown = converter(block)
                    if markdown:
                        markdown_parts.append(markdown)
            
            return '\n\n'.join(markdown_parts)
            
        except Exception as e:
            logger.error(f"Blocks to markdown conversion failed: {e}")
            return ""
    
    def _convert_paragraph(self, block: Dict[str, Any]) -> str:
        """段落ブロックの変換"""
        try:
            rich_text = block['paragraph']['rich_text']
            text = self._extract_rich_text(rich_text)
            return text if text else ""
            
        except Exception as e:
            logger.error(f"Paragraph conversion failed: {e}")
            return ""
    
    def _convert_heading_1(self, block: Dict[str, Any]) -> str:
        """見出し1ブロックの変換"""
        try:
            rich_text = block['heading_1']['rich_text']
            text = self._extract_rich_text(rich_text)
            return f"# {text}" if text else ""
            
        except Exception as e:
            logger.error(f"Heading 1 conversion failed: {e}")
            return ""
    
    def _convert_heading_2(self, block: Dict[str, Any]) -> str:
        """見出し2ブロックの変換"""
        try:
            rich_text = block['heading_2']['rich_text']
            text = self._extract_rich_text(rich_text)
            return f"## {text}" if text else ""
            
        except Exception as e:
            logger.error(f"Heading 2 conversion failed: {e}")
            return ""
    
    def _convert_heading_3(self, block: Dict[str, Any]) -> str:
        """見出し3ブロックの変換"""
        try:
            rich_text = block['heading_3']['rich_text']
            text = self._extract_rich_text(rich_text)
            return f"### {text}" if text else ""
            
        except Exception as e:
            logger.error(f"Heading 3 conversion failed: {e}")
            return ""
    
    def _convert_bulleted_list(self, block: Dict[str, Any]) -> str:
        """箇条書きリストブロックの変換"""
        try:
            rich_text = block['bulleted_list_item']['rich_text']
            text = self._extract_rich_text(rich_text)
            return f"- {text}" if text else ""
            
        except Exception as e:
            logger.error(f"Bulleted list conversion failed: {e}")
            return ""
    
    def _convert_numbered_list(self, block: Dict[str, Any]) -> str:
        """番号付きリストブロックの変換"""
        try:
            rich_text = block['numbered_list_item']['rich_text']
            text = self._extract_rich_text(rich_text)
            return f"1. {text}" if text else ""
            
        except Exception as e:
            logger.error(f"Numbered list conversion failed: {e}")
            return ""
    
    def _convert_quote(self, block: Dict[str, Any]) -> str:
        """引用ブロックの変換"""
        try:
            rich_text = block['quote']['rich_text']
            text = self._extract_rich_text(rich_text)
            return f"> {text}" if text else ""
            
        except Exception as e:
            logger.error(f"Quote conversion failed: {e}")
            return ""
    
    def _convert_code(self, block: Dict[str, Any]) -> str:
        """コードブロックの変換"""
        try:
            rich_text = block['code']['rich_text']
            code_text = self._extract_rich_text(rich_text)
            language = block['code'].get('language', '')
            
            if code_text:
                return f"```{language}\n{code_text}\n```"
            return ""
            
        except Exception as e:
            logger.error(f"Code conversion failed: {e}")
            return ""
    
    def _convert_callout(self, block: Dict[str, Any]) -> str:
        """コールアウトブロックの変換"""
        try:
            rich_text = block['callout']['rich_text']
            text = self._extract_rich_text(rich_text)
            icon = block['callout'].get('icon', {})
            
            if text:
                return f"> [!{icon.get('type', 'note')}] {text}"
            return ""
            
        except Exception as e:
            logger.error(f"Callout conversion failed: {e}")
            return ""
    
    def _convert_toggle(self, block: Dict[str, Any]) -> str:
        """トグルブロックの変換"""
        try:
            rich_text = block['toggle']['rich_text']
            text = self._extract_rich_text(rich_text)
            return f"<details>\n<summary>{text}</summary>\n\n</details>" if text else ""
            
        except Exception as e:
            logger.error(f"Toggle conversion failed: {e}")
            return ""
    
    def _convert_divider(self, block: Dict[str, Any]) -> str:
        """区切り線ブロックの変換"""
        return "---"
    
    def _extract_rich_text(self, rich_text_array: List[Dict[str, Any]]) -> str:
        """リッチテキスト配列からテキストを抽出"""
        try:
            text_parts = []
            for text_obj in rich_text_array:
                text_content = text_obj.get('text', {}).get('content', '')
                if text_content:
                    text_parts.append(text_content)
            return ''.join(text_parts)
            
        except Exception as e:
            logger.error(f"Rich text extraction failed: {e}")
            return ""
    
    def _create_frontmatter(self, page: Dict[str, Any]) -> Dict[str, Any]:
        """フロントマターの作成"""
        try:
            frontmatter = {
                'notion_id': page.get('id'),
                'created_time': page.get('created_time'),
                'last_edited_time': page.get('last_edited_time'),
                'source': 'notion'
            }
            
            # プロパティからタグを抽出
            properties = page.get('properties', {})
            tags = self._extract_tags_from_properties(properties)
            if tags:
                frontmatter['tags'] = tags
            
            return frontmatter
            
        except Exception as e:
            logger.error(f"Frontmatter creation failed: {e}")
            return {}
    
    def _extract_tags_from_properties(self, properties: Dict[str, Any]) -> List[str]:
        """プロパティからタグを抽出"""
        try:
            tags = []
            
            # マルチセレクトプロパティからタグを抽出
            for prop_name, prop_value in properties.items():
                if prop_value.get('type') == 'multi_select':
                    multi_select = prop_value.get('multi_select', [])
                    for option in multi_select:
                        tags.append(option.get('name', ''))
            
            return [tag for tag in tags if tag]
            
        except Exception as e:
            logger.error(f"Tag extraction failed: {e}")
            return []
    
    def _convert_markdown_to_blocks(self, markdown_content: str) -> List[Dict[str, Any]]:
        """MarkdownをNotionブロックに変換"""
        try:
            blocks = []
            lines = markdown_content.split('\n')
            
            for line in lines:
                if not line.strip():
                    continue
                
                if line.startswith('# '):
                    blocks.append({
                        'type': 'heading_1',
                        'heading_1': {'rich_text': [{'text': {'content': line[2:]}}]}
                    })
                elif line.startswith('## '):
                    blocks.append({
                        'type': 'heading_2',
                        'heading_2': {'rich_text': [{'text': {'content': line[3:]}}]}
                    })
                elif line.startswith('### '):
                    blocks.append({
                        'type': 'heading_3',
                        'heading_3': {'rich_text': [{'text': {'content': line[4:]}}]}
                    })
                elif line.startswith('- '):
                    blocks.append({
                        'type': 'bulleted_list_item',
                        'bulleted_list_item': {'rich_text': [{'text': {'content': line[2:]}}]}
                    })
                elif line.startswith('1. '):
                    blocks.append({
                        'type': 'numbered_list_item',
                        'numbered_list_item': {'rich_text': [{'text': {'content': line[3:]}}]}
                    })
                elif line.startswith('> '):
                    blocks.append({
                        'type': 'quote',
                        'quote': {'rich_text': [{'text': {'content': line[2:]}}]}
                    })
                elif line.startswith('```'):
                    # コードブロックの処理
                    language = line[3:] if len(line) > 3 else ''
                    code_lines = []
                    i = lines.index(line) + 1
                    while i < len(lines) and not lines[i].startswith('```'):
                        code_lines.append(lines[i])
                        i += 1
                    
                    blocks.append({
                        'type': 'code',
                        'code': {
                            'rich_text': [{'text': {'content': '\n'.join(code_lines)}}],
                            'language': language
                        }
                    })
                else:
                    # 通常の段落
                    blocks.append({
                        'type': 'paragraph',
                        'paragraph': {'rich_text': [{'text': {'content': line}}]}
                    })
            
            return blocks
            
        except Exception as e:
            logger.error(f"Markdown to blocks conversion failed: {e}")
            return []
    
    def _create_notion_properties(self, title: str, frontmatter: Dict[str, Any]) -> Dict[str, Any]:
        """Notionプロパティの作成"""
        try:
            properties = {
                'title': {'title': [{'text': {'content': title}}]}
            }
            
            # フロントマターからプロパティを抽出
            if 'tags' in frontmatter:
                properties['タグ'] = {
                    'multi_select': [{'name': tag} for tag in frontmatter['tags']]
                }
            
            if 'obsidian_id' in frontmatter:
                properties['Obsidian ID'] = {
                    'rich_text': [{'text': {'content': frontmatter['obsidian_id']}}]
                }
            
            return properties
            
        except Exception as e:
            logger.error(f"Notion properties creation failed: {e}")
            return {'title': {'title': [{'text': {'content': title}}]}}
    
    def convert_obsidian_links_to_notion(self, content: str) -> str:
        """ObsidianリンクをNotionリンクに変換"""
        try:
            # Obsidianリンクのパターン: [[link]]
            obsidian_link_pattern = r'\[\[([^\]]+)\]\]'
            
            def replace_obsidian_link(match):
                link_text = match.group(1)
                # Notionでは、リンクは通常のテキストとして扱われる
                return link_text
            
            converted_content = re.sub(obsidian_link_pattern, replace_obsidian_link, content)
            return converted_content
            
        except Exception as e:
            logger.error(f"Obsidian link conversion failed: {e}")
            return content
    
    def convert_notion_links_to_obsidian(self, content: str) -> str:
        """NotionリンクをObsidianリンクに変換"""
        try:
            # Notionのリンクは通常のテキストとして扱われるため、
            # 特別な変換は必要ない
            return content
            
        except Exception as e:
            logger.error(f"Notion link conversion failed: {e}")
            return content
    
    def extract_obsidian_frontmatter(self, content: str) -> Dict[str, Any]:
        """Obsidianのフロントマターを抽出"""
        try:
            frontmatter_pattern = r'^---\n(.*?)\n---'
            match = re.search(frontmatter_pattern, content, re.DOTALL)
            
            if match:
                frontmatter_text = match.group(1)
                # YAMLとして解析（実際の実装では、yamlライブラリを使用）
                frontmatter = {}
                for line in frontmatter_text.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        frontmatter[key.strip()] = value.strip()
                return frontmatter
            
            return {}
            
        except Exception as e:
            logger.error(f"Frontmatter extraction failed: {e}")
            return {}
    
    def create_obsidian_frontmatter(self, metadata: Dict[str, Any]) -> str:
        """Obsidianのフロントマターを作成"""
        try:
            if not metadata:
                return ""
            
            frontmatter_lines = ["---"]
            for key, value in metadata.items():
                if isinstance(value, list):
                    frontmatter_lines.append(f"{key}: {', '.join(value)}")
                else:
                    frontmatter_lines.append(f"{key}: {value}")
            frontmatter_lines.append("---")
            
            return '\n'.join(frontmatter_lines)
            
        except Exception as e:
            logger.error(f"Frontmatter creation failed: {e}")
            return ""
