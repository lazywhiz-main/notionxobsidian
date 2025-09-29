"""
基本的なダッシュボード機能
現在の状況を表示するシンプルなダッシュボード
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from analysis_engine.enhanced_analysis_engine import EnhancedAnalysisEngine
from notion_integration.notion_client import NotionClient
from obsidian_integration.markdown_parser import ObsidianMarkdownParser
from config import settings
import os

logger = logging.getLogger(__name__)

class BasicDashboardService:
    """基本的なダッシュボードサービス"""
    
    def __init__(self):
        self.analysis_engine = EnhancedAnalysisEngine()
        self.notion_client = NotionClient()
        self.markdown_parser = ObsidianMarkdownParser()
        
        logger.info("Basic Dashboard Service initialized")
    
    async def get_dashboard_data(self) -> Dict[str, Any]:
        """
        ダッシュボードの基本データを取得
        """
        try:
            logger.info("Generating dashboard data")
            
            # 1. 基本統計の取得
            basic_stats = await self._get_basic_stats()
            
            # 2. 最近の同期状況
            sync_status = await self._get_sync_status()
            
            # 3. 重複コンテンツの検出
            duplicates = await self._get_duplicates()
            
            # 4. 推奨事項
            recommendations = await self._get_recommendations()
            
            # 5. システムステータス
            system_status = await self._get_system_status()
            
            return {
                "timestamp": datetime.now().isoformat(),
                "basic_stats": basic_stats,
                "sync_status": sync_status,
                "duplicates": duplicates,
                "recommendations": recommendations,
                "system_status": system_status
            }
            
        except Exception as e:
            logger.error(f"Dashboard data generation failed: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "basic_stats": {"error": "Failed to load"},
                "sync_status": {"error": "Failed to load"},
                "duplicates": {"error": "Failed to load"},
                "recommendations": {"error": "Failed to load"},
                "system_status": {"error": "Failed to load"}
            }
    
    async def _get_basic_stats(self) -> Dict[str, Any]:
        """基本統計の取得"""
        try:
            stats = {
                "notion_pages": 0,
                "obsidian_files": 0,
                "total_content": 0,
                "last_analysis": None,
                "analysis_count": 0
            }
            
            # Notionページ数
            try:
                notion_pages = await self.notion_client.get_database_pages()
                stats["notion_pages"] = len(notion_pages) if notion_pages else 0
            except Exception as e:
                logger.warning(f"Failed to get Notion pages: {e}")
                stats["notion_pages"] = 0
            
            # Obsidianファイル数
            try:
                obsidian_files = self._scan_obsidian_files()
                stats["obsidian_files"] = len(obsidian_files)
            except Exception as e:
                logger.warning(f"Failed to scan Obsidian files: {e}")
                stats["obsidian_files"] = 0
            
            stats["total_content"] = stats["notion_pages"] + stats["obsidian_files"]
            
            return stats
            
        except Exception as e:
            logger.error(f"Basic stats generation failed: {e}")
            return {"error": str(e)}
    
    async def _get_sync_status(self) -> Dict[str, Any]:
        """同期状況の取得"""
        try:
            # 簡単な同期状況の取得
            sync_status = {
                "last_sync": "Never",
                "sync_type": "Manual",
                "status": "Ready",
                "next_sync": "Manual trigger required"
            }
            
            # 実際の実装では、同期ログから最新の同期時刻を取得
            # ここでは簡易的な実装
            
            return sync_status
            
        except Exception as e:
            logger.error(f"Sync status generation failed: {e}")
            return {"error": str(e)}
    
    async def _get_duplicates(self) -> Dict[str, Any]:
        """重複コンテンツの取得"""
        try:
            # 1. NotionとObsidianのコンテンツを取得
            contents = await self._get_all_contents()
            
            if not contents:
                return {
                    "count": 0,
                    "items": [],
                    "message": "No content found to analyze"
                }
            
            # 2. 重複検出を実行
            texts = [content["text"] for content in contents]
            duplicates = self.analysis_engine.content_analyzer.detect_duplicates(texts)
            
            # 3. 結果を整形
            duplicate_items = []
            for dup in duplicates:
                duplicate_items.append({
                    "content_a": contents[dup["index_a"]]["metadata"].get("title", f"Content {dup['index_a']}"),
                    "content_b": contents[dup["index_b"]]["metadata"].get("title", f"Content {dup['index_b']}"),
                    "similarity": dup["similarity"],
                    "source_a": contents[dup["index_a"]]["metadata"].get("source", "unknown"),
                    "source_b": contents[dup["index_b"]]["metadata"].get("source", "unknown")
                })
            
            return {
                "count": len(duplicates),
                "items": duplicate_items,
                "message": f"Found {len(duplicates)} potential duplicates"
            }
            
        except Exception as e:
            logger.error(f"Duplicate detection failed: {e}")
            return {"error": str(e)}
    
    async def _get_recommendations(self) -> Dict[str, Any]:
        """推奨事項の取得"""
        try:
            # 1. コンテンツを取得
            contents = await self._get_all_contents()
            
            if not contents:
                return {
                    "count": 0,
                    "items": [],
                    "message": "No content found to analyze"
                }
            
            # 2. 分析を実行
            analysis_results = await self.analysis_engine.analyze_content_comprehensive(contents)
            recommendations = analysis_results.get("recommendations", [])
            
            # 3. 結果を整形
            recommendation_items = []
            for rec in recommendations[:5]:  # 最大5件
                recommendation_items.append({
                    "title": rec.get("title", ""),
                    "description": rec.get("description", ""),
                    "priority": rec.get("priority", "medium"),
                    "action_type": rec.get("type", ""),
                    "estimated_time": rec.get("estimated_time", "Unknown")
                })
            
            return {
                "count": len(recommendations),
                "items": recommendation_items,
                "message": f"Generated {len(recommendations)} recommendations"
            }
            
        except Exception as e:
            logger.error(f"Recommendations generation failed: {e}")
            return {"error": str(e)}
    
    async def _get_system_status(self) -> Dict[str, Any]:
        """システムステータスの取得"""
        try:
            status = {
                "api_server": "Running",
                "notion_connection": "Unknown",
                "obsidian_connection": "Unknown",
                "analysis_engine": "Ready",
                "last_check": datetime.now().isoformat()
            }
            
            # Notion接続テスト
            try:
                await self.notion_client.get_database_pages()
                status["notion_connection"] = "Connected"
            except Exception as e:
                status["notion_connection"] = f"Error: {str(e)[:50]}"
            
            # Obsidian接続テスト
            try:
                vault_path = settings.OBSIDIAN_VAULT_PATH
                if vault_path and os.path.exists(vault_path):
                    status["obsidian_connection"] = "Connected"
                else:
                    status["obsidian_connection"] = "Path not configured"
            except Exception as e:
                status["obsidian_connection"] = f"Error: {str(e)[:50]}"
            
            return status
            
        except Exception as e:
            logger.error(f"System status generation failed: {e}")
            return {"error": str(e)}
    
    async def _get_all_contents(self) -> List[Dict[str, Any]]:
        """すべてのコンテンツを取得"""
        try:
            contents = []
            
            # Notionコンテンツ
            try:
                notion_pages = await self.notion_client.get_database_pages()
                if notion_pages:
                    for page in notion_pages[:5]:  # 最大5件
                        page_id = page["id"]
                        blocks = await self.notion_client.get_page_content(page_id)
                        text_content = self._extract_text_from_blocks(blocks)
                        
                        if text_content:
                            contents.append({
                                "id": page_id,
                                "text": text_content,
                                "metadata": {
                                    "title": self._extract_title_from_page(page),
                                    "source": "notion",
                                    "last_modified": page.get("last_edited_time", ""),
                                    "url": page.get("url", "")
                                }
                            })
            except Exception as e:
                logger.warning(f"Failed to get Notion content: {e}")
            
            # Obsidianコンテンツ
            try:
                obsidian_files = self._scan_obsidian_files()
                for file_path in obsidian_files[:5]:  # 最大5件
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        parsed_data = self.markdown_parser.parse_file(file_path, content)
                        if parsed_data and parsed_data.get('content', {}).get('raw_content'):
                            contents.append({
                                "id": file_path,
                                "text": parsed_data['content']['raw_content'],
                                "metadata": {
                                    "title": parsed_data.get('file_info', {}).get('name', ''),
                                    "source": "obsidian",
                                    "file_path": file_path,
                                    "last_modified": parsed_data.get('file_info', {}).get('modified_time', ''),
                                    "word_count": parsed_data.get('metadata', {}).get('word_count', 0)
                                }
                            })
                    except Exception as e:
                        logger.warning(f"Failed to parse file {file_path}: {e}")
                        continue
            except Exception as e:
                logger.warning(f"Failed to get Obsidian content: {e}")
            
            return contents
            
        except Exception as e:
            logger.error(f"Content retrieval failed: {e}")
            return []
    
    def _scan_obsidian_files(self) -> List[str]:
        """Obsidianファイルをスキャン"""
        try:
            vault_path = settings.OBSIDIAN_VAULT_PATH
            if not vault_path or not os.path.exists(vault_path):
                return []
            
            markdown_files = []
            for root, dirs, files in os.walk(vault_path):
                for file in files:
                    if file.endswith('.md'):
                        file_path = os.path.join(root, file)
                        markdown_files.append(file_path)
            
            return markdown_files[:10]  # 最大10件まで
            
        except Exception as e:
            logger.error(f"File scanning failed: {e}")
            return []
    
    def _extract_text_from_blocks(self, blocks: List[Dict[str, Any]]) -> str:
        """Notionブロックからテキストを抽出"""
        try:
            text_parts = []
            for block in blocks:
                block_type = block.get("type")
                if block_type == "paragraph":
                    rich_text = block.get("paragraph", {}).get("rich_text", [])
                    text = "".join([rt.get("plain_text", "") for rt in rich_text])
                    if text:
                        text_parts.append(text)
                elif block_type in ["heading_1", "heading_2", "heading_3"]:
                    rich_text = block.get(block_type, {}).get("rich_text", [])
                    text = "".join([rt.get("plain_text", "") for rt in rich_text])
                    if text:
                        text_parts.append(f"# {text}")
                elif block_type == "bulleted_list_item":
                    rich_text = block.get("bulleted_list_item", {}).get("rich_text", [])
                    text = "".join([rt.get("plain_text", "") for rt in rich_text])
                    if text:
                        text_parts.append(f"- {text}")
                elif block_type == "numbered_list_item":
                    rich_text = block.get("numbered_list_item", {}).get("rich_text", [])
                    text = "".join([rt.get("plain_text", "") for rt in rich_text])
                    if text:
                        text_parts.append(f"1. {text}")
            
            return "\n".join(text_parts)
            
        except Exception as e:
            logger.error(f"Text extraction failed: {e}")
            return ""
    
    def _extract_title_from_page(self, page: Dict[str, Any]) -> str:
        """Notionページからタイトルを抽出"""
        try:
            properties = page.get("properties", {})
            title_prop = properties.get("Name", {}).get("title", [])
            if title_prop:
                return title_prop[0].get("plain_text", "Untitled")
            return "Untitled"
        except Exception as e:
            logger.error(f"Title extraction failed: {e}")
            return "Untitled"
