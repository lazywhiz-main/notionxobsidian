from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from config import settings
from analysis_engine.enhanced_analysis_engine import EnhancedAnalysisEngine
from analysis_engine.content_analyzer import ContentAnalyzer
from analysis_engine.ai_service_integration import AIServiceIntegration
from sync_system.manual_sync_service import ManualSyncService
from sync_system.basic_dashboard_service import BasicDashboardService
from tests.mock_data_service import MockDataService
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Notion x Obsidian Integration API",
    description="API for integrating Notion and Obsidian with AI analysis capabilities.",
    version="0.2.0",
)

# Initialize services
enhanced_engine = EnhancedAnalysisEngine()
content_analyzer = ContentAnalyzer()
ai_service = AIServiceIntegration()
manual_sync = ManualSyncService()
dashboard_service = BasicDashboardService()
mock_data_service = MockDataService()

# Pydantic models
class ContentItem(BaseModel):
    id: str
    text: str
    metadata: Optional[Dict[str, Any]] = {}

class AnalysisRequest(BaseModel):
    contents: List[ContentItem]
    analysis_type: Optional[str] = "comprehensive"

class SingleAnalysisRequest(BaseModel):
    content: ContentItem

@app.get("/")
async def read_root():
    return {
        "message": "Notion x Obsidian Integration API is running!",
        "version": "0.2.0",
        "features": [
            "Enhanced Analysis Engine",
            "AI Service Integration", 
            "Content Analysis",
            "Insight Generation",
            "Recommendation System",
            "Manual Sync Service",
            "Basic Dashboard",
            "Mock Data Testing"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": "2024-01-01T00:00:00Z"}

# ===== 手動同期機能 =====

@app.post("/sync/manual/notion-to-obsidian")
async def sync_notion_to_obsidian():
    """NotionからObsidianへの手動同期"""
    try:
        result = await manual_sync.sync_notion_to_obsidian()
        return result
    except Exception as e:
        logger.error(f"Manual sync failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sync/manual/obsidian-to-notion")
async def sync_obsidian_to_notion():
    """ObsidianからNotionへの手動同期"""
    try:
        result = await manual_sync.sync_obsidian_to_notion()
        return result
    except Exception as e:
        logger.error(f"Manual sync failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sync/manual/full")
async def full_manual_sync():
    """双方向の完全手動同期"""
    try:
        result = await manual_sync.full_sync()
        return result
    except Exception as e:
        logger.error(f"Full manual sync failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===== ダッシュボード機能 =====

@app.get("/dashboard")
async def get_dashboard():
    """基本的なダッシュボードデータを取得"""
    try:
        dashboard_data = await dashboard_service.get_dashboard_data()
        return dashboard_data
    except Exception as e:
        logger.error(f"Dashboard data generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dashboard/duplicates")
async def get_dashboard_duplicates():
    """重複コンテンツの詳細表示"""
    try:
        dashboard_data = await dashboard_service.get_dashboard_data()
        return {
            "duplicates": dashboard_data.get("duplicates", {}),
            "timestamp": dashboard_data.get("timestamp")
        }
    except Exception as e:
        logger.error(f"Duplicate data generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dashboard/recommendations")
async def get_dashboard_recommendations():
    """推奨事項の詳細表示"""
    try:
        dashboard_data = await dashboard_service.get_dashboard_data()
        return {
            "recommendations": dashboard_data.get("recommendations", {}),
            "timestamp": dashboard_data.get("timestamp")
        }
    except Exception as e:
        logger.error(f"Recommendation data generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dashboard/status")
async def get_dashboard_status():
    """システムステータスの表示"""
    try:
        dashboard_data = await dashboard_service.get_dashboard_data()
        return {
            "system_status": dashboard_data.get("system_status", {}),
            "basic_stats": dashboard_data.get("basic_stats", {}),
            "timestamp": dashboard_data.get("timestamp")
        }
    except Exception as e:
        logger.error(f"Status data generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===== 分析機能 =====

@app.post("/analyze/comprehensive")
async def analyze_comprehensive(request: AnalysisRequest):
    """包括的なコンテンツ分析"""
    try:
        contents = [item.dict() for item in request.contents]
        results = await enhanced_engine.analyze_content_comprehensive(contents)
        return {"success": True, "results": results}
    except Exception as e:
        logger.error(f"Comprehensive analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/single")
async def analyze_single(request: SingleAnalysisRequest):
    """単一コンテンツの詳細分析"""
    try:
        content = request.content.dict()
        results = await enhanced_engine.analyze_single_content(content)
        return {"success": True, "results": results}
    except Exception as e:
        logger.error(f"Single analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/keywords")
async def extract_keywords(request: SingleAnalysisRequest):
    """キーワード抽出"""
    try:
        text = request.content.text
        keywords = content_analyzer.extract_keywords(text)
        return {"success": True, "keywords": keywords}
    except Exception as e:
        logger.error(f"Keyword extraction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/sentiment")
async def analyze_sentiment(request: SingleAnalysisRequest):
    """感情分析"""
    try:
        text = request.content.text
        sentiment = content_analyzer.analyze_sentiment(text)
        return {"success": True, "sentiment": sentiment}
    except Exception as e:
        logger.error(f"Sentiment analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/similarity")
async def calculate_similarity(request: AnalysisRequest):
    """類似度計算"""
    try:
        texts = [item.text for item in request.contents]
        similarity_matrix = content_analyzer.calculate_similarity(texts)
        return {"success": True, "similarity_matrix": similarity_matrix}
    except Exception as e:
        logger.error(f"Similarity calculation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/duplicates")
async def detect_duplicates(request: AnalysisRequest):
    """重複検出"""
    try:
        texts = [item.text for item in request.contents]
        duplicates = content_analyzer.detect_duplicates(texts)
        return {"success": True, "duplicates": duplicates}
    except Exception as e:
        logger.error(f"Duplicate detection failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===== AI機能 =====

@app.post("/ai/summary")
async def generate_summary(request: SingleAnalysisRequest):
    """AI要約生成"""
    try:
        text = request.content.text
        summary = ai_service.generate_summary(text, max_length=200)
        return {"success": True, "summary": summary}
    except Exception as e:
        logger.error(f"Summary generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai/insights")
async def generate_insights(request: AnalysisRequest):
    """AIインサイト生成"""
    try:
        contents = [item.dict() for item in request.contents]
        insights = ai_service.generate_insights(contents)
        return {"success": True, "insights": insights}
    except Exception as e:
        logger.error(f"Insights generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai/quality")
async def analyze_quality(request: SingleAnalysisRequest):
    """AI品質分析"""
    try:
        text = request.content.text
        quality = ai_service.analyze_content_quality(text)
        return {"success": True, "quality": quality}
    except Exception as e:
        logger.error(f"Quality analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===== モックデータテスト機能 =====

@app.get("/test/mock-data")
async def test_mock_data():
    """モックデータでのテスト実行"""
    try:
        results = await mock_data_service.run_all_tests()
        return results
    except Exception as e:
        logger.error(f"Mock data test failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test/comprehensive-analysis")
async def test_comprehensive_analysis():
    """包括的分析のテスト"""
    try:
        results = await mock_data_service.test_comprehensive_analysis()
        return results
    except Exception as e:
        logger.error(f"Comprehensive analysis test failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test/duplicate-detection")
async def test_duplicate_detection():
    """重複検出のテスト"""
    try:
        results = await mock_data_service.test_duplicate_detection()
        return results
    except Exception as e:
        logger.error(f"Duplicate detection test failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test/ai-services")
async def test_ai_services():
    """AIサービスのテスト"""
    try:
        results = await mock_data_service.test_ai_services()
        return results
    except Exception as e:
        logger.error(f"AI services test failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test/dashboard-data")
async def test_dashboard_data():
    """ダッシュボードデータのテスト"""
    try:
        results = await mock_data_service.test_dashboard_data()
        return results
    except Exception as e:
        logger.error(f"Dashboard data test failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ===== システム情報 =====

@app.get("/status")
async def get_status():
    """システムステータス"""
    return {
        "status": "running",
        "version": "0.2.0",
        "features": {
            "enhanced_analysis": True,
            "ai_service_integration": True,
            "content_analysis": True,
            "manual_sync": True,
            "basic_dashboard": True,
            "notion_integration": "ready",
            "obsidian_integration": "ready",
            "sync_system": "ready"
        },
        "ai_services": {
            "openai": "configured" if settings.OPENAI_API_KEY else "not_configured",
            "anthropic": "configured" if settings.ANTHROPIC_API_KEY else "not_configured"
        },
        "endpoints": {
            "sync": [
                "POST /sync/manual/notion-to-obsidian",
                "POST /sync/manual/obsidian-to-notion", 
                "POST /sync/manual/full"
            ],
            "dashboard": [
                "GET /dashboard",
                "GET /dashboard/duplicates",
                "GET /dashboard/recommendations",
                "GET /dashboard/status"
            ],
            "analysis": [
                "POST /analyze/comprehensive",
                "POST /analyze/single",
                "POST /analyze/keywords",
                "POST /analyze/sentiment",
                "POST /analyze/similarity",
                "POST /analyze/duplicates"
            ],
            "ai": [
                "POST /ai/summary",
                "POST /ai/insights",
                "POST /ai/quality"
            ],
            "testing": [
                "GET /test/mock-data",
                "GET /test/comprehensive-analysis",
                "GET /test/duplicate-detection",
                "GET /test/ai-services",
                "GET /test/dashboard-data"
            ]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)