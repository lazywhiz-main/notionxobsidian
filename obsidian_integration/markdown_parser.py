"""
Obsidian Markdown パーサー
ObsidianのMarkdownファイルを解析する
"""
import logging
import re
import yaml
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

class ObsidianMarkdownParser:
    """Obsidian Markdownパーサークラス"""
    
    def __init__(self):
        self.link_pattern = r'\[\[([^\]]+)\]\]'
        self.tag_pattern = r'#([a-zA-Z0-9_/]+)'
        self.image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        self.code_block_pattern = r'```(\w+)?\n(.*?)\n```'
        self.frontmatter_pattern = r'^---\n(.*?)\n---'
    
    def parse_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Markdownファイルを解析"""
        try:
            # ファイル情報の取得
            file_info = self._get_file_info(file_path)
            
            # フロントマターの解析
            frontmatter = self._parse_frontmatter(content)
            
            # コンテンツの解析
            parsed_content = self._parse_content(content)
            
            # リンクの解析
            links = self._parse_links(content)
            
            # タグの解析
            tags = self._parse_tags(content)
            
            # 画像の解析
            images = self._parse_images(content)
            
            # コードブロックの解析
            code_blocks = self._parse_code_blocks(content)
            
            return {
                'file_info': file_info,
                'frontmatter': frontmatter,
                'content': parsed_content,
                'links': links,
                'tags': tags,
                'images': images,
                'code_blocks': code_blocks,
                'metadata': {
                    'word_count': self._count_words(content),
                    'character_count': len(content),
                    'line_count': len(content.split('\n')),
                    'parsed_at': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"File parsing failed: {e}")
            return {}
    
    def _get_file_info(self, file_path: str) -> Dict[str, Any]:
        """ファイル情報の取得"""
        try:
            file_path_obj = Path(file_path)
            
            if not file_path_obj.exists():
                return {}
            
            stat = file_path_obj.stat()
            
            return {
                'path': str(file_path),
                'name': file_path_obj.name,
                'stem': file_path_obj.stem,
                'suffix': file_path_obj.suffix,
                'size': stat.st_size,
                'created_time': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified_time': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'parent': str(file_path_obj.parent),
                'relative_path': str(file_path_obj.relative_to(file_path_obj.parent))
            }
            
        except Exception as e:
            logger.error(f"File info retrieval failed: {e}")
            return {}
    
    def _parse_frontmatter(self, content: str) -> Dict[str, Any]:
        """フロントマターの解析"""
        try:
            # フロントマターの抽出
            match = re.search(self.frontmatter_pattern, content, re.DOTALL)
            if not match:
                return {}
            
            frontmatter_text = match.group(1)
            
            # YAMLとして解析
            frontmatter = yaml.safe_load(frontmatter_text)
            return frontmatter if frontmatter else {}
            
        except Exception as e:
            logger.error(f"Frontmatter parsing failed: {e}")
            return {}
    
    def _parse_content(self, content: str) -> Dict[str, Any]:
        """コンテンツの解析"""
        try:
            # フロントマターを除去
            content_without_frontmatter = re.sub(self.frontmatter_pattern, '', content, flags=re.DOTALL).strip()
            
            # 見出しの解析
            headings = self._parse_headings(content_without_frontmatter)
            
            # 段落の解析
            paragraphs = self._parse_paragraphs(content_without_frontmatter)
            
            # リストの解析
            lists = self._parse_lists(content_without_frontmatter)
            
            # 引用の解析
            quotes = self._parse_quotes(content_without_frontmatter)
            
            return {
                'headings': headings,
                'paragraphs': paragraphs,
                'lists': lists,
                'quotes': quotes,
                'raw_content': content_without_frontmatter
            }
            
        except Exception as e:
            logger.error(f"Content parsing failed: {e}")
            return {}
    
    def _parse_headings(self, content: str) -> List[Dict[str, Any]]:
        """見出しの解析"""
        try:
            headings = []
            heading_pattern = r'^(#{1,6})\s+(.+)$'
            
            for line_num, line in enumerate(content.split('\n'), 1):
                match = re.match(heading_pattern, line)
                if match:
                    level = len(match.group(1))
                    text = match.group(2).strip()
                    
                    headings.append({
                        'level': level,
                        'text': text,
                        'line_number': line_num,
                        'id': self._generate_heading_id(text)
                    })
            
            return headings
            
        except Exception as e:
            logger.error(f"Heading parsing failed: {e}")
            return []
    
    def _parse_paragraphs(self, content: str) -> List[Dict[str, Any]]:
        """段落の解析"""
        try:
            paragraphs = []
            lines = content.split('\n')
            current_paragraph = []
            line_number = 1
            
            for line in lines:
                if line.strip() == '':
                    if current_paragraph:
                        paragraphs.append({
                            'text': '\n'.join(current_paragraph),
                            'line_number': line_number - len(current_paragraph),
                            'length': len('\n'.join(current_paragraph))
                        })
                        current_paragraph = []
                else:
                    current_paragraph.append(line)
                line_number += 1
            
            # 最後の段落を追加
            if current_paragraph:
                paragraphs.append({
                    'text': '\n'.join(current_paragraph),
                    'line_number': line_number - len(current_paragraph),
                    'length': len('\n'.join(current_paragraph))
                })
            
            return paragraphs
            
        except Exception as e:
            logger.error(f"Paragraph parsing failed: {e}")
            return []
    
    def _parse_lists(self, content: str) -> List[Dict[str, Any]]:
        """リストの解析"""
        try:
            lists = []
            lines = content.split('\n')
            current_list = []
            list_type = None
            line_number = 1
            
            for line in lines:
                if re.match(r'^[-*+]\s+', line):
                    if list_type != 'unordered':
                        if current_list:
                            lists.append({
                                'type': list_type,
                                'items': current_list,
                                'line_number': line_number - len(current_list)
                            })
                        current_list = []
                        list_type = 'unordered'
                    
                    item_text = re.sub(r'^[-*+]\s+', '', line)
                    current_list.append({
                        'text': item_text,
                        'line_number': line_number
                    })
                elif re.match(r'^\d+\.\s+', line):
                    if list_type != 'ordered':
                        if current_list:
                            lists.append({
                                'type': list_type,
                                'items': current_list,
                                'line_number': line_number - len(current_list)
                            })
                        current_list = []
                        list_type = 'ordered'
                    
                    item_text = re.sub(r'^\d+\.\s+', '', line)
                    current_list.append({
                        'text': item_text,
                        'line_number': line_number
                    })
                else:
                    if current_list:
                        lists.append({
                            'type': list_type,
                            'items': current_list,
                            'line_number': line_number - len(current_list)
                        })
                        current_list = []
                        list_type = None
                
                line_number += 1
            
            # 最後のリストを追加
            if current_list:
                lists.append({
                    'type': list_type,
                    'items': current_list,
                    'line_number': line_number - len(current_list)
                })
            
            return lists
            
        except Exception as e:
            logger.error(f"List parsing failed: {e}")
            return []
    
    def _parse_quotes(self, content: str) -> List[Dict[str, Any]]:
        """引用の解析"""
        try:
            quotes = []
            lines = content.split('\n')
            current_quote = []
            line_number = 1
            
            for line in lines:
                if line.startswith('> '):
                    current_quote.append({
                        'text': line[2:],
                        'line_number': line_number
                    })
                else:
                    if current_quote:
                        quotes.append({
                            'items': current_quote,
                            'line_number': line_number - len(current_quote)
                        })
                        current_quote = []
                line_number += 1
            
            # 最後の引用を追加
            if current_quote:
                quotes.append({
                    'items': current_quote,
                    'line_number': line_number - len(current_quote)
                })
            
            return quotes
            
        except Exception as e:
            logger.error(f"Quote parsing failed: {e}")
            return []
    
    def _parse_links(self, content: str) -> List[Dict[str, Any]]:
        """リンクの解析"""
        try:
            links = []
            
            # Obsidianリンクの解析
            obsidian_links = re.findall(self.link_pattern, content)
            for link in obsidian_links:
                links.append({
                    'type': 'obsidian_link',
                    'target': link,
                    'text': link,
                    'display_text': link
                })
            
            # Markdownリンクの解析
            markdown_link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
            markdown_links = re.findall(markdown_link_pattern, content)
            for text, url in markdown_links:
                links.append({
                    'type': 'markdown_link',
                    'target': url,
                    'text': text,
                    'display_text': text
                })
            
            return links
            
        except Exception as e:
            logger.error(f"Link parsing failed: {e}")
            return []
    
    def _parse_tags(self, content: str) -> List[Dict[str, Any]]:
        """タグの解析"""
        try:
            tags = []
            tag_matches = re.finditer(self.tag_pattern, content)
            
            for match in tag_matches:
                tag = match.group(1)
                tags.append({
                    'tag': tag,
                    'position': match.start(),
                    'line_number': content[:match.start()].count('\n') + 1
                })
            
            return tags
            
        except Exception as e:
            logger.error(f"Tag parsing failed: {e}")
            return []
    
    def _parse_images(self, content: str) -> List[Dict[str, Any]]:
        """画像の解析"""
        try:
            images = []
            image_matches = re.finditer(self.image_pattern, content)
            
            for match in image_matches:
                alt_text = match.group(1)
                image_path = match.group(2)
                images.append({
                    'alt_text': alt_text,
                    'path': image_path,
                    'position': match.start(),
                    'line_number': content[:match.start()].count('\n') + 1
                })
            
            return images
            
        except Exception as e:
            logger.error(f"Image parsing failed: {e}")
            return []
    
    def _parse_code_blocks(self, content: str) -> List[Dict[str, Any]]:
        """コードブロックの解析"""
        try:
            code_blocks = []
            code_matches = re.finditer(self.code_block_pattern, content, re.DOTALL)
            
            for match in code_matches:
                language = match.group(1) or 'text'
                code = match.group(2)
                code_blocks.append({
                    'language': language,
                    'code': code,
                    'position': match.start(),
                    'line_number': content[:match.start()].count('\n') + 1,
                    'length': len(code)
                })
            
            return code_blocks
            
        except Exception as e:
            logger.error(f"Code block parsing failed: {e}")
            return []
    
    def _count_words(self, content: str) -> int:
        """単語数のカウント"""
        try:
            # フロントマターを除去
            content_without_frontmatter = re.sub(self.frontmatter_pattern, '', content, flags=re.DOTALL)
            
            # コードブロックを除去
            content_without_code = re.sub(self.code_block_pattern, '', content_without_frontmatter, flags=re.DOTALL)
            
            # 単語をカウント
            words = re.findall(r'\b\w+\b', content_without_code)
            return len(words)
            
        except Exception as e:
            logger.error(f"Word counting failed: {e}")
            return 0
    
    def _generate_heading_id(self, text: str) -> str:
        """見出しIDの生成"""
        try:
            # 特殊文字を除去し、小文字に変換
            id_text = re.sub(r'[^\w\s-]', '', text.lower())
            id_text = re.sub(r'[-\s]+', '-', id_text)
            return id_text.strip('-')
            
        except Exception as e:
            logger.error(f"Heading ID generation failed: {e}")
            return ""
    
    def extract_metadata(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """メタデータの抽出"""
        try:
            metadata = {
                'title': parsed_data.get('file_info', {}).get('name', ''),
                'created_time': parsed_data.get('file_info', {}).get('created_time', ''),
                'modified_time': parsed_data.get('file_info', {}).get('modified_time', ''),
                'word_count': parsed_data.get('metadata', {}).get('word_count', 0),
                'character_count': parsed_data.get('metadata', {}).get('character_count', 0),
                'line_count': parsed_data.get('metadata', {}).get('line_count', 0),
                'heading_count': len(parsed_data.get('content', {}).get('headings', [])),
                'link_count': len(parsed_data.get('links', [])),
                'tag_count': len(parsed_data.get('tags', [])),
                'image_count': len(parsed_data.get('images', [])),
                'code_block_count': len(parsed_data.get('code_blocks', []))
            }
            
            # フロントマターからメタデータを追加
            frontmatter = parsed_data.get('frontmatter', {})
            if frontmatter:
                metadata.update(frontmatter)
            
            return metadata
            
        except Exception as e:
            logger.error(f"Metadata extraction failed: {e}")
            return {}
    
    def get_linked_files(self, parsed_data: Dict[str, Any]) -> List[str]:
        """リンクされたファイルの一覧を取得"""
        try:
            linked_files = []
            links = parsed_data.get('links', [])
            
            for link in links:
                if link['type'] == 'obsidian_link':
                    linked_files.append(link['target'])
            
            return list(set(linked_files))  # 重複を除去
            
        except Exception as e:
            logger.error(f"Linked files extraction failed: {e}")
            return []
    
    def get_tags(self, parsed_data: Dict[str, Any]) -> List[str]:
        """タグの一覧を取得"""
        try:
            tags = []
            tag_data = parsed_data.get('tags', [])
            
            for tag_info in tag_data:
                tags.append(tag_info['tag'])
            
            return list(set(tags))  # 重複を除去
            
        except Exception as e:
            logger.error(f"Tags extraction failed: {e}")
            return []
