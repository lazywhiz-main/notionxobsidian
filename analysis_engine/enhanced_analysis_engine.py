"""
統合された分析エンジン
基本的な分析、高度な分析、AIサービス連携を統合した分析エンジン
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from .content_analyzer import ContentAnalyzer
from .insight_generator import InsightGenerator
from .recommendation_system import RecommendationSystem
from .advanced_analyzer import AdvancedAnalyzer
from .ai_service_integration import AIServiceIntegration

logger = logging.getLogger(__name__)

class EnhancedAnalysisEngine:
    """統合された分析エンジンクラス"""
    
    def __init__(self):
        self.content_analyzer = ContentAnalyzer()
        self.insight_generator = InsightGenerator()
        self.recommendation_system = RecommendationSystem()
        self.advanced_analyzer = AdvancedAnalyzer()
        self.ai_service = AIServiceIntegration()
        
        logger.info("Enhanced Analysis Engine initialized")
    
    async def analyze_content_comprehensive(self, contents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        包括的なコンテンツ分析
        基本的な分析から高度な分析、AIサービス連携まで統合
        """
        try:
            if not contents:
                logger.warning("No content provided for analysis")
                return {"error": "No content provided"}
            
            logger.info(f"Starting comprehensive analysis for {len(contents)} content items")
            
            # 1. 基本的な分析
            basic_analysis = await self._perform_basic_analysis(contents)
            
            # 2. 高度な分析
            advanced_analysis = await self._perform_advanced_analysis(contents)
            
            # 3. AIサービス連携分析
            ai_analysis = await self._perform_ai_analysis(contents)
            
            # 4. 統合結果の生成
            integrated_results = await self._integrate_analysis_results(
                basic_analysis, advanced_analysis, ai_analysis
            )
            
            # 5. インサイトと推奨事項の生成
            insights = await self._generate_comprehensive_insights(integrated_results)
            recommendations = await self._generate_comprehensive_recommendations(integrated_results)
            
            # 6. 最終結果の構築
            final_results = {
                'analysis_metadata': {
                    'total_content': len(contents),
                    'analysis_date': datetime.now().isoformat(),
                    'analysis_type': 'comprehensive',
                    'processing_time': integrated_results.get('processing_time', 0)
                },
                'basic_analysis': basic_analysis,
                'advanced_analysis': advanced_analysis,
                'ai_analysis': ai_analysis,
                'integrated_results': integrated_results,
                'insights': insights,
                'recommendations': recommendations,
                'summary': await self._generate_executive_summary(integrated_results, insights, recommendations)
            }
            
            logger.info("Comprehensive analysis completed successfully")
            return final_results
            
        except Exception as e:
            logger.error(f"Comprehensive analysis failed: {e}")
            return {"error": str(e)}
    
    async def analyze_single_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        単一コンテンツの詳細分析
        """
        try:
            logger.info(f"Analyzing single content: {content.get('id', 'unknown')}")
            
            text = content.get('text', '')
            metadata = content.get('metadata', {})
            
            # 基本的な分析
            keywords = self.content_analyzer.extract_keywords(text)
            sentiment = self.content_analyzer.analyze_sentiment(text)
            
            # 高度な分析
            advanced_sentiment = self.advanced_analyzer.analyze_sentiment_advanced(text)
            importance = self.advanced_analyzer.calculate_importance_score(text, metadata)
            
            # AIサービス分析
            summary = self.ai_service.generate_summary(text, max_length=200)
            quality = self.ai_service.analyze_content_quality(text)
            
            return {
                'content_id': content.get('id', 'unknown'),
                'basic_analysis': {
                    'keywords': keywords,
                    'sentiment': sentiment
                },
                'advanced_analysis': {
                    'sentiment_advanced': advanced_sentiment,
                    'importance_score': importance
                },
                'ai_analysis': {
                    'summary': summary,
                    'quality': quality
                },
                'analysis_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Single content analysis failed: {e}")
            return {"error": str(e)}
    
    async def _perform_basic_analysis(self, contents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """基本的な分析の実行"""
        try:
            content_texts = [item['text'] for item in contents]
            content_ids = [item['id'] for item in contents]
            
            # 類似度計算
            similarities = self.content_analyzer.calculate_similarity(content_texts)
            
            # 重複検出
            duplicates = self.content_analyzer.detect_duplicates(content_texts)
            
            # キーワード抽出
            keywords_list = [self.content_analyzer.extract_keywords(text) for text in content_texts]
            
            # 感情分析
            sentiments = [self.content_analyzer.analyze_sentiment(text) for text in content_texts]
            
            return {
                'content_ids': content_ids,
                'similarities': similarities,
                'duplicates': duplicates,
                'keywords': keywords_list,
                'sentiments': sentiments,
                'analysis_type': 'basic'
            }
            
        except Exception as e:
            logger.error(f"Basic analysis failed: {e}")
            return {"error": str(e)}
    
    async def _perform_advanced_analysis(self, contents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """高度な分析の実行"""
        try:
            content_texts = [item['text'] for item in contents]
            content_metadata = [item.get('metadata', {}) for item in contents]
            
            # トピック分析
            topics = self.advanced_analyzer.analyze_topics(content_texts, num_topics=5)
            
            # 高度な感情分析
            advanced_sentiments = [
                self.advanced_analyzer.analyze_sentiment_advanced(text) 
                for text in content_texts
            ]
            
            # 重要度スコアリング
            importance_scores = [
                self.advanced_analyzer.calculate_importance_score(text, metadata)
                for text, metadata in zip(content_texts, content_metadata)
            ]
            
            # トレンド分析（履歴データがある場合）
            trend_analysis = self.advanced_analyzer.analyze_trends(contents)
            
            return {
                'topics': topics,
                'advanced_sentiments': advanced_sentiments,
                'importance_scores': importance_scores,
                'trend_analysis': trend_analysis,
                'analysis_type': 'advanced'
            }
            
        except Exception as e:
            logger.error(f"Advanced analysis failed: {e}")
            return {"error": str(e)}
    
    async def _perform_ai_analysis(self, contents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """AIサービス連携分析の実行"""
        try:
            # インサイト生成
            insights = self.ai_service.generate_insights(contents)
            
            # 各コンテンツの要約と品質分析
            summaries = []
            quality_analyses = []
            
            for content in contents[:5]:  # 最大5件まで
                text = content.get('text', '')
                summary = self.ai_service.generate_summary(text, max_length=150)
                quality = self.ai_service.analyze_content_quality(text)
                
                summaries.append({
                    'content_id': content.get('id', 'unknown'),
                    'summary': summary
                })
                quality_analyses.append({
                    'content_id': content.get('id', 'unknown'),
                    'quality': quality
                })
            
            return {
                'insights': insights,
                'summaries': summaries,
                'quality_analyses': quality_analyses,
                'analysis_type': 'ai_service'
            }
            
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return {"error": str(e)}
    
    async def _integrate_analysis_results(self, basic_analysis: Dict, advanced_analysis: Dict, ai_analysis: Dict) -> Dict[str, Any]:
        """分析結果の統合"""
        try:
            start_time = datetime.now()
            
            # 統合結果の構築
            integrated_results = {
                'content_count': basic_analysis.get('content_ids', []),
                'similarity_matrix': basic_analysis.get('similarities', []),
                'duplicate_pairs': basic_analysis.get('duplicates', []),
                'topics': advanced_analysis.get('topics', {}),
                'sentiment_distribution': self._calculate_sentiment_distribution(
                    basic_analysis.get('sentiments', []),
                    advanced_analysis.get('advanced_sentiments', [])
                ),
                'importance_ranking': self._calculate_importance_ranking(
                    advanced_analysis.get('importance_scores', [])
                ),
                'quality_metrics': self._calculate_quality_metrics(
                    ai_analysis.get('quality_analyses', [])
                ),
                'trend_indicators': advanced_analysis.get('trend_analysis', {}),
                'ai_insights': ai_analysis.get('insights', {}),
                'processing_time': (datetime.now() - start_time).total_seconds()
            }
            
            return integrated_results
            
        except Exception as e:
            logger.error(f"Analysis integration failed: {e}")
            return {"error": str(e)}
    
    async def _generate_comprehensive_insights(self, integrated_results: Dict) -> List[Dict[str, Any]]:
        """包括的なインサイトの生成"""
        try:
            insights = []
            
            # 重複コンテンツのインサイト
            duplicates = integrated_results.get('duplicate_pairs', [])
            for dup in duplicates:
                insights.append({
                    'type': 'duplicate_content',
                    'priority': 'high',
                    'title': '重複コンテンツの検出',
                    'description': f"コンテンツ {dup['index_a']} と {dup['index_b']} が {dup['similarity']:.2f} の類似度で重複しています",
                    'action': 'コンテンツの統合または整理を検討してください',
                    'confidence': dup['similarity']
                })
            
            # トピックのインサイト
            topics = integrated_results.get('topics', {}).get('topics', [])
            for topic in topics:
                insights.append({
                    'type': 'topic_cluster',
                    'priority': 'medium',
                    'title': f'トピック: {topic["main_keyword"]}',
                    'description': f"関連キーワード: {', '.join(topic['keywords'])}",
                    'action': '関連コンテンツをグループ化して整理してください',
                    'confidence': topic['frequency'] / 10  # 正規化
                })
            
            # 重要度のインサイト
            importance_ranking = integrated_results.get('importance_ranking', [])
            if importance_ranking:
                top_important = importance_ranking[0]
                insights.append({
                    'type': 'importance_highlight',
                    'priority': 'high',
                    'title': '重要度の高いコンテンツ',
                    'description': f"コンテンツ {top_important['content_id']} が最高の重要度スコア ({top_important['score']:.1f}) を持っています",
                    'action': 'このコンテンツを優先的に管理してください',
                    'confidence': top_important['score'] / 100
                })
            
            # AIインサイトの追加
            ai_insights = integrated_results.get('ai_insights', {})
            if ai_insights.get('insights'):
                insights.append({
                    'type': 'ai_insight',
                    'priority': 'medium',
                    'title': 'AI生成インサイト',
                    'description': ai_insights['insights'],
                    'action': 'AIの提案を参考にコンテンツを改善してください',
                    'confidence': 0.8
                })
            
            return insights
            
        except Exception as e:
            logger.error(f"Comprehensive insights generation failed: {e}")
            return []
    
    async def _generate_comprehensive_recommendations(self, integrated_results: Dict) -> List[Dict[str, Any]]:
        """包括的な推奨事項の生成"""
        try:
            recommendations = []
            
            # 重複コンテンツの推奨事項
            duplicates = integrated_results.get('duplicate_pairs', [])
            for dup in duplicates:
                recommendations.append({
                    'type': 'merge_content',
                    'priority': 'high',
                    'title': '重複コンテンツの統合',
                    'description': f"コンテンツ {dup['index_a']} と {dup['index_b']} を統合することを推奨します",
                    'action_items': [
                        '重複コンテンツの内容を比較',
                        'より完全なコンテンツを選択',
                        '不要なコンテンツを削除またはアーカイブ',
                        '統合後のコンテンツを更新'
                    ],
                    'expected_benefit': 'コンテンツの重複を解消し、管理を効率化',
                    'difficulty': 'medium',
                    'estimated_time': '30分'
                })
            
            # トピック整理の推奨事項
            topics = integrated_results.get('topics', {}).get('topics', [])
            if len(topics) > 3:
                recommendations.append({
                    'type': 'organize_topics',
                    'priority': 'medium',
                    'title': 'トピックの整理',
                    'description': f"{len(topics)}個のトピックが検出されました。トピック別にコンテンツを整理することを推奨します",
                    'action_items': [
                        'トピック別のフォルダまたはタグを作成',
                        '関連コンテンツをグループ化',
                        'トピック間の関連性を明確化',
                        'ナビゲーションの改善'
                    ],
                    'expected_benefit': 'コンテンツの発見性と管理性の向上',
                    'difficulty': 'medium',
                    'estimated_time': '1時間'
                })
            
            # 品質改善の推奨事項
            quality_metrics = integrated_results.get('quality_metrics', {})
            if quality_metrics.get('avg_quality_score', 0) < 6.0:
                recommendations.append({
                    'type': 'improve_quality',
                    'priority': 'medium',
                    'title': 'コンテンツ品質の改善',
                    'description': f"平均品質スコアが {quality_metrics.get('avg_quality_score', 0):.1f} です。品質の向上を推奨します",
                    'action_items': [
                        '低品質コンテンツの特定',
                        'コンテンツの構造化',
                        '情報の完全性の向上',
                        '読みやすさの改善'
                    ],
                    'expected_benefit': 'コンテンツの価値と有用性の向上',
                    'difficulty': 'high',
                    'estimated_time': '2時間'
                })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Comprehensive recommendations generation failed: {e}")
            return []
    
    async def _generate_executive_summary(self, integrated_results: Dict, insights: List[Dict], recommendations: List[Dict]) -> Dict[str, Any]:
        """エグゼクティブサマリーの生成"""
        try:
            total_content = len(integrated_results.get('content_count', []))
            duplicate_count = len(integrated_results.get('duplicate_pairs', []))
            topic_count = len(integrated_results.get('topics', {}).get('topics', []))
            
            high_priority_insights = [i for i in insights if i.get('priority') == 'high']
            high_priority_recommendations = [r for r in recommendations if r.get('priority') == 'high']
            
            summary = f"""
            分析サマリー:
            - 総コンテンツ数: {total_content}
            - 重複ペア: {duplicate_count}
            - 検出トピック: {topic_count}
            - 高優先度インサイト: {len(high_priority_insights)}
            - 高優先度推奨事項: {len(high_priority_recommendations)}
            
            主要な発見:
            {chr(10).join([f"- {insight['title']}" for insight in high_priority_insights[:3]])}
            
            推奨アクション:
            {chr(10).join([f"- {rec['title']}" for rec in high_priority_recommendations[:3]])}
            """
            
            return {
                'summary': summary.strip(),
                'key_metrics': {
                    'total_content': total_content,
                    'duplicate_count': duplicate_count,
                    'topic_count': topic_count,
                    'high_priority_items': len(high_priority_insights) + len(high_priority_recommendations)
                },
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Executive summary generation failed: {e}")
            return {"summary": "サマリーの生成に失敗しました", "error": str(e)}
    
    def _calculate_sentiment_distribution(self, basic_sentiments: List[str], advanced_sentiments: List[Dict]) -> Dict[str, Any]:
        """感情分布の計算"""
        try:
            sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
            
            # 基本的な感情分析結果
            for sentiment in basic_sentiments:
                sentiment_counts[sentiment.lower()] += 1
            
            # 高度な感情分析結果
            for sentiment_data in advanced_sentiments:
                sentiment = sentiment_data.get('sentiment', 'neutral')
                sentiment_counts[sentiment.lower()] += 1
            
            total = sum(sentiment_counts.values())
            if total > 0:
                return {
                    'positive_ratio': sentiment_counts['positive'] / total,
                    'negative_ratio': sentiment_counts['negative'] / total,
                    'neutral_ratio': sentiment_counts['neutral'] / total,
                    'total_count': total
                }
            else:
                return {'positive_ratio': 0, 'negative_ratio': 0, 'neutral_ratio': 0, 'total_count': 0}
                
        except Exception as e:
            logger.error(f"Sentiment distribution calculation failed: {e}")
            return {'positive_ratio': 0, 'negative_ratio': 0, 'neutral_ratio': 0, 'total_count': 0}
    
    def _calculate_importance_ranking(self, importance_scores: List[Dict]) -> List[Dict[str, Any]]:
        """重要度ランキングの計算"""
        try:
            ranking = []
            for i, score_data in enumerate(importance_scores):
                ranking.append({
                    'content_id': f'content_{i}',
                    'score': score_data.get('importance_score', 0),
                    'rank': 0  # 後で設定
                })
            
            # スコアでソート
            ranking.sort(key=lambda x: x['score'], reverse=True)
            
            # ランクを設定
            for i, item in enumerate(ranking):
                item['rank'] = i + 1
            
            return ranking
            
        except Exception as e:
            logger.error(f"Importance ranking calculation failed: {e}")
            return []
    
    def _calculate_quality_metrics(self, quality_analyses: List[Dict]) -> Dict[str, Any]:
        """品質メトリクスの計算"""
        try:
            if not quality_analyses:
                return {'avg_quality_score': 0, 'total_analyzed': 0}
            
            # 品質スコアの抽出（フォールバック分析の場合）
            scores = []
            for analysis in quality_analyses:
                quality_data = analysis.get('quality', {})
                quality_analysis = quality_data.get('quality_analysis', '')
                
                # 簡単なスコア抽出（実際の実装ではより複雑になる）
                if '読みやすさ:' in quality_analysis:
                    try:
                        score_line = [line for line in quality_analysis.split('\n') if '読みやすさ:' in line][0]
                        score = float(score_line.split(':')[1].split('/')[0])
                        scores.append(score)
                    except:
                        scores.append(5.0)  # デフォルトスコア
                else:
                    scores.append(5.0)  # デフォルトスコア
            
            return {
                'avg_quality_score': sum(scores) / len(scores) if scores else 0,
                'total_analyzed': len(quality_analyses),
                'scores': scores
            }
            
        except Exception as e:
            logger.error(f"Quality metrics calculation failed: {e}")
            return {'avg_quality_score': 0, 'total_analyzed': 0}
