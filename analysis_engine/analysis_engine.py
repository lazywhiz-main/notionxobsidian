from typing import List, Dict, Any
from analysis_engine.content_analyzer import ContentAnalyzer
from analysis_engine.insight_generator import InsightGenerator
from analysis_engine.recommendation_system import RecommendationSystem
import logging

logger = logging.getLogger(__name__)

class AnalysisEngine:
    def __init__(self):
        self.content_analyzer = ContentAnalyzer()
        self.insight_generator = InsightGenerator()
        self.recommendation_system = RecommendationSystem()

    async def analyze_and_generate_insights(self, contents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyzes a list of content items and generates insights and recommendations.
        Each content item in the list should be a dictionary with at least 'id' and 'text' keys.
        """
        if not contents:
            logger.info("No content provided for analysis.")
            return {"insights": [], "recommendations": []}

        content_texts = [item['text'] for item in contents]
        content_ids = [item['id'] for item in contents]

        logger.info(f"Starting analysis for {len(contents)} content items.")

        # 1. Content Analysis
        similarities = self.content_analyzer.calculate_similarity(content_texts)
        duplicates = self.content_analyzer.detect_duplicates(content_texts)
        keywords_list = [self.content_analyzer.extract_keywords(text) for text in content_texts]
        sentiments = [self.content_analyzer.analyze_sentiment(text) for text in content_texts]

        analysis_results = {
            "content_ids": content_ids,
            "texts": content_texts,
            "similarities": similarities,
            "duplicates": duplicates,
            "keywords": keywords_list,
            "sentiments": sentiments
        }
        logger.info("Content analysis completed.")

        # 2. Insight Generation
        insights = []
        insights.extend(self.insight_generator.generate_related_content_insights(analysis_results))
        insights.extend(self.insight_generator.generate_duplicate_insights(analysis_results))
        # Add summary insights for each content (placeholder for actual summarization)
        for i, content_id in enumerate(content_ids):
            insights.append(self.insight_generator.generate_summary_insight(content_id, f"Summary of {content_id} content."))
        logger.info(f"Generated {len(insights)} insights.")

        # 3. Recommendation Generation
        for insight in insights:
            recommendation = self.insight_generator.generate_action_recommendation(insight)
            self.recommendation_system.add_recommendation(recommendation)
        logger.info(f"Generated {len(self.recommendation_system.get_recommendations())} recommendations.")

        return {
            "analysis_results": analysis_results,
            "insights": insights,
            "recommendations": self.recommendation_system.get_recommendations()
        }