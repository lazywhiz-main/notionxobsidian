"""
手動同期機能
ユーザーが即座に使える手動同期機能を実装
"""
import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from analysis_engine.enhanced_analysis_engine import EnhancedAnalysisEngine
from notion_integration.notion_client import NotionClient
from obsidian_integration.markdown_parser import ObsidianMarkdownParser
from obsidian_integration.dashboard_builder import ObsidianDashboardBuilder
from notion_integration.dashboard_builder import NotionDashboardBuilder
from config import settings

logger = logging.getLogger(__name__)

class ManualSyncService:
    """手動同期サービス"""
    
    def __init__(self):
        self.analysis_engine = EnhancedAnalysisEngine()
        self.notion_client = NotionClient()
        self.markdown_parser = ObsidianMarkdownParser()
        
        # Obsidianダッシュボードは設定がある場合のみ初期化
        try:
            self.obsidian_dashboard = ObsidianDashboardBuilder()
        except Exception as e:
            logger.warning(f"Obsidian dashboard initialization failed: {e}")
            self.obsidian_dashboard = None
        
        # Notionダッシュボードは設定がある場合のみ初期化
        try:
            self.notion_dashboard = NotionDashboardBuilder(self.notion_client)
        except Exception as e:
            logger.warning(f"Notion dashboard initialization failed: {e}")
            self.notion_dashboard = None
        
        logger.info("Manual Sync Service initialized")
    
    async def sync_notion_to_obsidian(self) -> Dict[str, Any]:
        """
        NotionからObsidianへの手動同期
        """
        try:
            logger.info("Starting manual sync: Notion → Obsidian")
            start_time = datetime.now()
            
            # 1. Notionからデータを取得
            notion_pages = await self.notion_client.get_database_pages()
            if not notion_pages:
                return {
                    "success": False,
                    "message": "No pages found in Notion database",
                    "sync_type": "notion_to_obsidian"
                }
            
            # 2. ページの内容を取得
            contents = []
            for page in notion_pages[:10]:  # 最大10件まで
                page_id = page["id"]
                blocks = await self.notion_client.get_page_content(page_id)
                
                # テキスト内容を抽出
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
            
            # 3. 基本的な分析を実行
            if contents:
                analysis_results = await self.analysis_engine.analyze_content_comprehensive(contents)
                
                # 4. Obsidianに結果を保存
                await self._save_analysis_to_obsidian(analysis_results)
                
                # 5. 同期ログを更新
                sync_log = {
                    "sync_type": "notion_to_obsidian",
                    "timestamp": datetime.now().isoformat(),
                    "pages_processed": len(contents),
                    "analysis_completed": True,
                    "duration_seconds": (datetime.now() - start_time).total_seconds()
                }
                
                logger.info(f"Manual sync completed: {len(contents)} pages processed")
                return {
                    "success": True,
                    "message": f"Successfully synced {len(contents)} pages from Notion to Obsidian",
                    "sync_log": sync_log,
                    "analysis_summary": analysis_results.get("summary", {})
                }
            else:
                return {
                    "success": False,
                    "message": "No content found in Notion pages",
                    "sync_type": "notion_to_obsidian"
                }
                
        except Exception as e:
            logger.error(f"Manual sync failed: {e}")
            return {
                "success": False,
                "message": f"Sync failed: {str(e)}",
                "sync_type": "notion_to_obsidian",
                "error": str(e)
            }
    
    async def sync_obsidian_to_notion(self) -> Dict[str, Any]:
        """
        ObsidianからNotionへの手動同期
        """
        try:
            logger.info("Starting manual sync: Obsidian → Notion")
            start_time = datetime.now()
            
            # 1. Obsidianファイルをスキャン
            obsidian_files = self._scan_obsidian_files()
            if not obsidian_files:
                return {
                    "success": False,
                    "message": "No files found in Obsidian vault",
                    "sync_type": "obsidian_to_notion"
                }
            
            # 2. ファイルの内容を解析
            contents = []
            for file_path in obsidian_files[:10]:  # 最大10件まで
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
            
            # 3. 基本的な分析を実行
            if contents:
                analysis_results = await self.analysis_engine.analyze_content_comprehensive(contents)
                
                # 4. Notionに結果を保存
                await self._save_analysis_to_notion(analysis_results)
                
                # 5. 同期ログを更新
                sync_log = {
                    "sync_type": "obsidian_to_notion",
                    "timestamp": datetime.now().isoformat(),
                    "files_processed": len(contents),
                    "analysis_completed": True,
                    "duration_seconds": (datetime.now() - start_time).total_seconds()
                }
                
                logger.info(f"Manual sync completed: {len(contents)} files processed")
                return {
                    "success": True,
                    "message": f"Successfully synced {len(contents)} files from Obsidian to Notion",
                    "sync_log": sync_log,
                    "analysis_summary": analysis_results.get("summary", {})
                }
            else:
                return {
                    "success": False,
                    "message": "No content found in Obsidian files",
                    "sync_type": "obsidian_to_notion"
                }
                
        except Exception as e:
            logger.error(f"Manual sync failed: {e}")
            return {
                "success": False,
                "message": f"Sync failed: {str(e)}",
                "sync_type": "obsidian_to_notion",
                "error": str(e)
            }
    
    async def full_sync(self) -> Dict[str, Any]:
        """
        双方向の完全同期
        """
        try:
            logger.info("Starting full manual sync")
            start_time = datetime.now()
            
            # 1. Notion → Obsidian
            notion_result = await self.sync_notion_to_obsidian()
            
            # 2. Obsidian → Notion
            obsidian_result = await self.sync_obsidian_to_notion()
            
            # 3. 結果を統合
            total_duration = (datetime.now() - start_time).total_seconds()
            
            return {
                "success": notion_result["success"] and obsidian_result["success"],
                "message": "Full sync completed",
                "notion_sync": notion_result,
                "obsidian_sync": obsidian_result,
                "total_duration_seconds": total_duration,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Full sync failed: {e}")
            return {
                "success": False,
                "message": f"Full sync failed: {str(e)}",
                "error": str(e)
            }
    
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
    
    def _scan_obsidian_files(self) -> List[str]:
        """Obsidianファイルをスキャン"""
        try:
            import os
            vault_path = settings.OBSIDIAN_VAULT_PATH
            if not vault_path or not os.path.exists(vault_path):
                return []
            
            markdown_files = []
            for root, dirs, files in os.walk(vault_path):
                for file in files:
                    if file.endswith('.md'):
                        file_path = os.path.join(root, file)
                        markdown_files.append(file_path)
            
            return markdown_files[:20]  # 最大20件まで
            
        except Exception as e:
            logger.error(f"File scanning failed: {e}")
            return []
    
    async def _save_analysis_to_obsidian(self, analysis_results: Dict[str, Any]):
        """分析結果をObsidianに保存"""
        try:
            # 分析結果のサマリーを作成
            summary = analysis_results.get("summary", {})
            insights = analysis_results.get("insights", [])
            recommendations = analysis_results.get("recommendations", [])
            
            # ダッシュボードを更新
            self.obsidian_dashboard.update_sync_status(
                last_sync_time=datetime.now().isoformat(),
                status_message="Manual sync completed",
                errors=0
            )
            
            # 分析結果ノートを作成
            if insights:
                insight_content = "## 分析インサイト\n\n"
                for insight in insights[:5]:
                    insight_content += f"### {insight.get('title', '')}\n"
                    insight_content += f"{insight.get('description', '')}\n\n"
                
                self.obsidian_dashboard.create_insight_note(
                    title=f"Analysis Insights - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                    content=insight_content,
                    front_matter={
                        "type": "analysis_insights",
                        "created": datetime.now().isoformat(),
                        "source": "manual_sync"
                    }
                )
            
            logger.info("Analysis results saved to Obsidian")
            
        except Exception as e:
            logger.error(f"Failed to save analysis to Obsidian: {e}")
    
    async def _save_analysis_to_notion(self, analysis_results: Dict[str, Any]):
        """分析結果をNotionに保存"""
        try:
            # 分析結果のサマリーを作成
            summary = analysis_results.get("summary", {})
            insights = analysis_results.get("insights", [])
            recommendations = analysis_results.get("recommendations", [])
            
            # ダッシュボードを更新
            await self.notion_dashboard.update_sync_status(
                last_sync_time=datetime.now().isoformat(),
                status_message="Manual sync completed",
                errors=0
            )
            
            # 分析結果をNotionに保存
            if insights:
                for insight in insights[:5]:
                    await self.notion_dashboard.display_analysis_results([{
                        "title": insight.get("title", ""),
                        "summary": insight.get("description", ""),
                        "analysis_type": [insight.get("type", "")],
                        "generated_at": datetime.now().isoformat()
                    }])
            
            logger.info("Analysis results saved to Notion")
            
        except Exception as e:
            logger.error(f"Failed to save analysis to Notion: {e}")
