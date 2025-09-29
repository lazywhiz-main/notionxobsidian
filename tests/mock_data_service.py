"""
モックデータでのテスト機能
Notion/Obsidianの設定なしでも動作確認できるテスト機能
"""
import asyncio
import logging
from typing import Dict, Any, List
from datetime import datetime
from analysis_engine.enhanced_analysis_engine import EnhancedAnalysisEngine
from analysis_engine.content_analyzer import ContentAnalyzer
from analysis_engine.ai_service_integration import AIServiceIntegration

logger = logging.getLogger(__name__)

class MockDataService:
    """モックデータサービス"""
    
    def __init__(self):
        self.analysis_engine = EnhancedAnalysisEngine()
        self.content_analyzer = ContentAnalyzer()
        self.ai_service = AIServiceIntegration()
        
        logger.info("Mock Data Service initialized")
    
    def get_mock_notion_data(self) -> List[Dict[str, Any]]:
        """モックNotionデータ"""
        return [
            {
                "id": "notion_page_1",
                "text": "This is a comprehensive overview of artificial intelligence and machine learning technologies. AI and ML are transforming various industries with their advanced capabilities.",
                "metadata": {
                    "title": "AI and ML Overview",
                    "source": "notion",
                    "last_modified": "2024-01-01T10:00:00Z",
                    "url": "https://notion.so/ai-overview"
                }
            },
            {
                "id": "notion_page_2",
                "text": "Machine learning algorithms are revolutionizing healthcare with diagnostic tools. These technologies improve patient outcomes and reduce medical errors.",
                "metadata": {
                    "title": "ML in Healthcare",
                    "source": "notion",
                    "last_modified": "2024-01-01T11:00:00Z",
                    "url": "https://notion.so/ml-healthcare"
                }
            },
            {
                "id": "notion_page_3",
                "text": "This is a comprehensive overview of artificial intelligence and machine learning technologies. AI and ML are transforming various industries with their advanced capabilities.",
                "metadata": {
                    "title": "AI Overview Duplicate",
                    "source": "notion",
                    "last_modified": "2024-01-01T12:00:00Z",
                    "url": "https://notion.so/ai-overview-duplicate"
                }
            }
        ]
    
    def get_mock_obsidian_data(self) -> List[Dict[str, Any]]:
        """モックObsidianデータ"""
        return [
            {
                "id": "obsidian_file_1",
                "text": "# Project Planning\n\nThis document outlines the project planning process for our new initiative.\n\n## Key Objectives\n- Improve efficiency\n- Reduce costs\n- Enhance quality",
                "metadata": {
                    "title": "Project Planning.md",
                    "source": "obsidian",
                    "file_path": "/vault/Project Planning.md",
                    "last_modified": "2024-01-01T09:00:00Z",
                    "word_count": 25
                }
            },
            {
                "id": "obsidian_file_2",
                "text": "# Meeting Notes\n\n## Today's Discussion\n- Budget allocation\n- Timeline updates\n- Resource requirements\n\n## Action Items\n- [ ] Review budget\n- [ ] Update timeline\n- [ ] Assign resources",
                "metadata": {
                    "title": "Meeting Notes.md",
                    "source": "obsidian",
                    "file_path": "/vault/Meeting Notes.md",
                    "last_modified": "2024-01-01T14:00:00Z",
                    "word_count": 30
                }
            },
            {
                "id": "obsidian_file_3",
                "text": "# Project Planning\n\nThis document outlines the project planning process for our new initiative.\n\n## Key Objectives\n- Improve efficiency\n- Reduce costs\n- Enhance quality",
                "metadata": {
                    "title": "Project Planning Duplicate.md",
                    "source": "obsidian",
                    "file_path": "/vault/Project Planning Duplicate.md",
                    "last_modified": "2024-01-01T15:00:00Z",
                    "word_count": 25
                }
            }
        ]
    
    async def test_comprehensive_analysis(self) -> Dict[str, Any]:
        """包括的分析のテスト"""
        try:
            logger.info("Testing comprehensive analysis with mock data")
            
            # モックデータを取得
            notion_data = self.get_mock_notion_data()
            obsidian_data = self.get_mock_obsidian_data()
            all_data = notion_data + obsidian_data
            
            # 包括的分析を実行
            results = await self.analysis_engine.analyze_content_comprehensive(all_data)
            
            return {
                "success": True,
                "message": "Comprehensive analysis test completed",
                "results": results,
                "data_count": len(all_data)
            }
            
        except Exception as e:
            logger.error(f"Comprehensive analysis test failed: {e}")
            return {
                "success": False,
                "message": f"Test failed: {str(e)}",
                "error": str(e)
            }
    
    async def test_duplicate_detection(self) -> Dict[str, Any]:
        """重複検出のテスト"""
        try:
            logger.info("Testing duplicate detection with mock data")
            
            # モックデータを取得
            notion_data = self.get_mock_notion_data()
            obsidian_data = self.get_mock_obsidian_data()
            all_data = notion_data + obsidian_data
            
            # テキストを抽出
            texts = [item["text"] for item in all_data]
            
            # 重複検出を実行
            duplicates = self.content_analyzer.detect_duplicates(texts)
            
            # 結果を整形
            duplicate_items = []
            for dup in duplicates:
                duplicate_items.append({
                    "content_a": all_data[dup["index_a"]]["metadata"]["title"],
                    "content_b": all_data[dup["index_b"]]["metadata"]["title"],
                    "similarity": dup["similarity"],
                    "source_a": all_data[dup["index_a"]]["metadata"]["source"],
                    "source_b": all_data[dup["index_b"]]["metadata"]["source"]
                })
            
            return {
                "success": True,
                "message": f"Found {len(duplicates)} duplicates",
                "duplicates": duplicate_items,
                "total_content": len(all_data)
            }
            
        except Exception as e:
            logger.error(f"Duplicate detection test failed: {e}")
            return {
                "success": False,
                "message": f"Test failed: {str(e)}",
                "error": str(e)
            }
    
    async def test_ai_services(self) -> Dict[str, Any]:
        """AIサービスのテスト"""
        try:
            logger.info("Testing AI services with mock data")
            
            # モックデータを取得
            notion_data = self.get_mock_notion_data()
            
            # AI要約のテスト
            summary_result = self.ai_service.generate_summary(notion_data[0]["text"], max_length=100)
            
            # AIインサイトのテスト
            insights_result = self.ai_service.generate_insights(notion_data)
            
            # AI品質分析のテスト
            quality_result = self.ai_service.analyze_content_quality(notion_data[0]["text"])
            
            return {
                "success": True,
                "message": "AI services test completed",
                "summary": summary_result,
                "insights": insights_result,
                "quality": quality_result
            }
            
        except Exception as e:
            logger.error(f"AI services test failed: {e}")
            return {
                "success": False,
                "message": f"Test failed: {str(e)}",
                "error": str(e)
            }
    
    async def test_dashboard_data(self) -> Dict[str, Any]:
        """ダッシュボードデータのテスト"""
        try:
            logger.info("Testing dashboard data generation with mock data")
            
            # モックデータを取得
            notion_data = self.get_mock_notion_data()
            obsidian_data = self.get_mock_obsidian_data()
            all_data = notion_data + obsidian_data
            
            # 基本統計
            basic_stats = {
                "notion_pages": len(notion_data),
                "obsidian_files": len(obsidian_data),
                "total_content": len(all_data),
                "last_analysis": datetime.now().isoformat(),
                "analysis_count": 1
            }
            
            # 重複検出
            texts = [item["text"] for item in all_data]
            duplicates = self.content_analyzer.detect_duplicates(texts)
            
            # 推奨事項（簡易版）
            recommendations = []
            if duplicates:
                recommendations.append({
                    "title": "重複コンテンツの統合",
                    "description": f"{len(duplicates)}個の重複が検出されました",
                    "priority": "high",
                    "action_type": "merge_content"
                })
            
            return {
                "success": True,
                "message": "Dashboard data test completed",
                "basic_stats": basic_stats,
                "duplicates": {
                    "count": len(duplicates),
                    "items": duplicates
                },
                "recommendations": {
                    "count": len(recommendations),
                    "items": recommendations
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Dashboard data test failed: {e}")
            return {
                "success": False,
                "message": f"Test failed: {str(e)}",
                "error": str(e)
            }
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """すべてのテストを実行"""
        try:
            logger.info("Running all mock data tests")
            
            results = {
                "timestamp": datetime.now().isoformat(),
                "tests": {}
            }
            
            # 包括的分析のテスト
            results["tests"]["comprehensive_analysis"] = await self.test_comprehensive_analysis()
            
            # 重複検出のテスト
            results["tests"]["duplicate_detection"] = await self.test_duplicate_detection()
            
            # AIサービスのテスト
            results["tests"]["ai_services"] = await self.test_ai_services()
            
            # ダッシュボードデータのテスト
            results["tests"]["dashboard_data"] = await self.test_dashboard_data()
            
            # 全体の成功/失敗を判定
            all_success = all(test.get("success", False) for test in results["tests"].values())
            results["overall_success"] = all_success
            
            logger.info(f"All tests completed. Overall success: {all_success}")
            return results
            
        except Exception as e:
            logger.error(f"Test suite failed: {e}")
            return {
                "success": False,
                "message": f"Test suite failed: {str(e)}",
                "error": str(e)
            }
