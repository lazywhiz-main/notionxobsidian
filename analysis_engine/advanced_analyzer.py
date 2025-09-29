"""
高度な分析機能
トピックモデリング、感情分析、重要度スコアリング、トレンド分析を実装
"""
import re
import math
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import logging

logger = logging.getLogger(__name__)

class AdvancedAnalyzer:
    """高度な分析機能を提供するクラス"""
    
    def __init__(self):
        # 感情分析用の辞書
        self.sentiment_words = {
            'positive': {
                'excellent', 'amazing', 'wonderful', 'fantastic', 'great', 'good', 'awesome',
                'brilliant', 'outstanding', 'superb', 'magnificent', 'perfect', 'ideal',
                'love', 'like', 'enjoy', 'appreciate', 'admire', 'cherish', 'treasure',
                'success', 'achievement', 'victory', 'triumph', 'accomplishment',
                'happy', 'joyful', 'delighted', 'pleased', 'satisfied', 'content'
            },
            'negative': {
                'terrible', 'awful', 'horrible', 'disgusting', 'hate', 'dislike', 'despise',
                'failure', 'disaster', 'catastrophe', 'crisis', 'problem', 'issue',
                'sad', 'depressed', 'miserable', 'unhappy', 'disappointed', 'frustrated',
                'angry', 'furious', 'rage', 'annoyed', 'irritated', 'upset',
                'bad', 'poor', 'worst', 'terrible', 'awful', 'horrible'
            }
        }
        
        # 重要度スコアリング用の重み
        self.importance_weights = {
            'title_keywords': 3.0,
            'heading_keywords': 2.0,
            'frequent_words': 1.5,
            'rare_words': 2.0,
            'sentiment_words': 1.2,
            'length_factor': 0.8
        }
        
        # トレンド分析用の時間窓
        self.trend_windows = {
            'short': 7,    # 7日
            'medium': 30,  # 30日
            'long': 90     # 90日
        }
    
    def analyze_topics(self, texts: List[str], num_topics: int = 5) -> Dict[str, Any]:
        """
        トピックモデリング（簡易版）
        実際のLDAの代わりに、キーワードの共起分析を使用
        """
        try:
            # テキストの前処理
            processed_texts = [self._preprocess_text(text) for text in texts]
            
            # キーワード抽出
            all_keywords = []
            for text in processed_texts:
                keywords = self._extract_keywords(text)
                all_keywords.extend(keywords)
            
            # キーワードの頻度計算
            keyword_freq = Counter(all_keywords)
            
            # 共起分析
            cooccurrence = self._calculate_cooccurrence(processed_texts)
            
            # トピック生成
            topics = self._generate_topics(keyword_freq, cooccurrence, num_topics)
            
            return {
                'topics': topics,
                'keyword_frequency': dict(keyword_freq.most_common(20)),
                'cooccurrence_matrix': cooccurrence,
                'analysis_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Topic analysis failed: {e}")
            return {}
    
    def analyze_sentiment_advanced(self, text: str) -> Dict[str, Any]:
        """
        高度な感情分析
        単純なキーワードマッチングから、文脈を考慮した分析
        """
        try:
            # テキストの前処理
            processed_text = self._preprocess_text(text)
            words = processed_text.split()
            
            # 感情スコア計算
            positive_score = 0
            negative_score = 0
            neutral_score = 0
            
            # 感情語の検出
            for word in words:
                if word in self.sentiment_words['positive']:
                    positive_score += 1
                elif word in self.sentiment_words['negative']:
                    negative_score += 1
                else:
                    neutral_score += 1
            
            # 文脈分析（否定語の検出）
            negation_words = {'not', 'no', 'never', 'none', 'nothing', 'neither', 'nor'}
            negation_score = sum(1 for word in words if word in negation_words)
            
            # 感情の強度計算
            total_words = len(words)
            if total_words > 0:
                positive_ratio = positive_score / total_words
                negative_ratio = negative_score / total_words
                neutral_ratio = neutral_score / total_words
                
                # 否定語による調整
                if negation_score > 0:
                    positive_ratio *= 0.5
                    negative_ratio *= 1.5
                
                # 最終的な感情判定
                if positive_ratio > negative_ratio and positive_ratio > 0.1:
                    sentiment = 'positive'
                    confidence = positive_ratio
                elif negative_ratio > positive_ratio and negative_ratio > 0.1:
                    sentiment = 'negative'
                    confidence = negative_ratio
                else:
                    sentiment = 'neutral'
                    confidence = neutral_ratio
            else:
                sentiment = 'neutral'
                confidence = 0.0
            
            return {
                'sentiment': sentiment,
                'confidence': confidence,
                'positive_score': positive_score,
                'negative_score': negative_score,
                'neutral_score': neutral_score,
                'negation_count': negation_score,
                'analysis_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Advanced sentiment analysis failed: {e}")
            return {'sentiment': 'neutral', 'confidence': 0.0}
    
    def calculate_importance_score(self, text: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        重要度スコアリング
        テキストの内容、構造、メタデータを考慮した重要度計算
        """
        try:
            # 基本情報の取得
            title = metadata.get('title', '') if metadata else ''
            word_count = len(text.split())
            char_count = len(text)
            
            # タイトルキーワードの重み
            title_keywords = self._extract_keywords(title)
            title_score = len(title_keywords) * self.importance_weights['title_keywords']
            
            # 見出しキーワードの重み
            headings = self._extract_headings(text)
            heading_score = len(headings) * self.importance_weights['heading_keywords']
            
            # 頻出語の重み
            frequent_words = self._get_frequent_words(text)
            frequent_score = len(frequent_words) * self.importance_weights['frequent_words']
            
            # 希少語の重み
            rare_words = self._get_rare_words(text)
            rare_score = len(rare_words) * self.importance_weights['rare_words']
            
            # 感情語の重み
            sentiment_words = self._get_sentiment_words(text)
            sentiment_score = len(sentiment_words) * self.importance_weights['sentiment_words']
            
            # 長さの重み
            length_score = min(word_count / 100, 1.0) * self.importance_weights['length_factor']
            
            # 総合スコア計算
            total_score = (
                title_score + heading_score + frequent_score + 
                rare_score + sentiment_score + length_score
            )
            
            # 正規化（0-100スケール）
            normalized_score = min(total_score * 10, 100)
            
            return {
                'importance_score': normalized_score,
                'components': {
                    'title_keywords': title_score,
                    'heading_keywords': heading_score,
                    'frequent_words': frequent_score,
                    'rare_words': rare_score,
                    'sentiment_words': sentiment_score,
                    'length_factor': length_score
                },
                'metadata': {
                    'word_count': word_count,
                    'char_count': char_count,
                    'title': title,
                    'headings_count': len(headings)
                },
                'analysis_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Importance scoring failed: {e}")
            return {'importance_score': 0.0}
    
    def analyze_trends(self, content_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        トレンド分析
        時系列データからトレンドを分析
        """
        try:
            if not content_history:
                return {}
            
            # データの整理
            trends = {}
            current_date = datetime.now()
            
            for window_name, days in self.trend_windows.items():
                cutoff_date = current_date - timedelta(days=days)
                
                # 期間内のデータをフィルタ
                recent_content = [
                    item for item in content_history
                    if datetime.fromisoformat(item.get('date', '')) >= cutoff_date
                ]
                
                # トレンド指標の計算
                trends[window_name] = {
                    'content_count': len(recent_content),
                    'avg_word_count': self._calculate_avg_word_count(recent_content),
                    'top_keywords': self._get_trending_keywords(recent_content),
                    'sentiment_trend': self._calculate_sentiment_trend(recent_content),
                    'growth_rate': self._calculate_growth_rate(recent_content, days)
                }
            
            return {
                'trends': trends,
                'analysis_date': current_date.isoformat(),
                'total_content': len(content_history)
            }
            
        except Exception as e:
            logger.error(f"Trend analysis failed: {e}")
            return {}
    
    def _preprocess_text(self, text: str) -> str:
        """テキストの前処理"""
        # 小文字に変換
        text = text.lower()
        # 特殊文字を除去
        text = re.sub(r'[^\w\s]', ' ', text)
        # 複数の空白を単一の空白に
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _extract_keywords(self, text: str, min_length: int = 3) -> List[str]:
        """キーワード抽出"""
        words = text.split()
        # ストップワードを除去
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'
        }
        keywords = [word for word in words if word not in stop_words and len(word) >= min_length]
        return keywords
    
    def _calculate_cooccurrence(self, texts: List[str]) -> Dict[str, Dict[str, int]]:
        """共起分析"""
        cooccurrence = defaultdict(lambda: defaultdict(int))
        
        for text in texts:
            words = text.split()
            for i, word1 in enumerate(words):
                for j, word2 in enumerate(words):
                    if i != j and word1 != word2:
                        cooccurrence[word1][word2] += 1
        
        return dict(cooccurrence)
    
    def _generate_topics(self, keyword_freq: Counter, cooccurrence: Dict, num_topics: int) -> List[Dict[str, Any]]:
        """トピック生成"""
        topics = []
        used_keywords = set()
        
        # 頻度の高いキーワードからトピックを生成
        for keyword, freq in keyword_freq.most_common():
            if keyword in used_keywords:
                continue
            
            # 関連キーワードを収集
            related_keywords = []
            if keyword in cooccurrence:
                related = sorted(cooccurrence[keyword].items(), key=lambda x: x[1], reverse=True)
                related_keywords = [kw for kw, count in related[:5] if kw not in used_keywords]
            
            # トピックを作成
            topic_keywords = [keyword] + related_keywords
            topics.append({
                'topic_id': len(topics) + 1,
                'keywords': topic_keywords,
                'main_keyword': keyword,
                'frequency': freq,
                'related_count': len(related_keywords)
            })
            
            # 使用済みキーワードをマーク
            used_keywords.update(topic_keywords)
            
            if len(topics) >= num_topics:
                break
        
        return topics
    
    def _extract_headings(self, text: str) -> List[str]:
        """見出しの抽出"""
        headings = re.findall(r'^#+\s+(.+)$', text, re.MULTILINE)
        return headings
    
    def _get_frequent_words(self, text: str) -> List[str]:
        """頻出語の取得"""
        words = self._extract_keywords(text)
        word_freq = Counter(words)
        # 頻度が2回以上の単語
        frequent_words = [word for word, freq in word_freq.items() if freq >= 2]
        return frequent_words
    
    def _get_rare_words(self, text: str) -> List[str]:
        """希少語の取得"""
        words = self._extract_keywords(text)
        word_freq = Counter(words)
        # 頻度が1回の単語
        rare_words = [word for word, freq in word_freq.items() if freq == 1]
        return rare_words
    
    def _get_sentiment_words(self, text: str) -> List[str]:
        """感情語の取得"""
        words = text.lower().split()
        sentiment_words = []
        for word in words:
            if word in self.sentiment_words['positive'] or word in self.sentiment_words['negative']:
                sentiment_words.append(word)
        return sentiment_words
    
    def _calculate_avg_word_count(self, content_list: List[Dict[str, Any]]) -> float:
        """平均単語数の計算"""
        if not content_list:
            return 0.0
        word_counts = [len(item.get('text', '').split()) for item in content_list]
        return sum(word_counts) / len(word_counts)
    
    def _get_trending_keywords(self, content_list: List[Dict[str, Any]]) -> List[str]:
        """トレンドキーワードの取得"""
        all_keywords = []
        for item in content_list:
            keywords = self._extract_keywords(item.get('text', ''))
            all_keywords.extend(keywords)
        
        keyword_freq = Counter(all_keywords)
        return [word for word, freq in keyword_freq.most_common(10)]
    
    def _calculate_sentiment_trend(self, content_list: List[Dict[str, Any]]) -> Dict[str, float]:
        """感情トレンドの計算"""
        sentiments = []
        for item in content_list:
            sentiment_result = self.analyze_sentiment_advanced(item.get('text', ''))
            sentiments.append(sentiment_result.get('sentiment', 'neutral'))
        
        sentiment_counts = Counter(sentiments)
        total = len(sentiments)
        
        return {
            'positive_ratio': sentiment_counts.get('positive', 0) / total,
            'negative_ratio': sentiment_counts.get('negative', 0) / total,
            'neutral_ratio': sentiment_counts.get('neutral', 0) / total
        }
    
    def _calculate_growth_rate(self, content_list: List[Dict[str, Any]], days: int) -> float:
        """成長率の計算"""
        if len(content_list) < 2:
            return 0.0
        
        # 期間を2つに分割
        mid_point = len(content_list) // 2
        first_half = content_list[:mid_point]
        second_half = content_list[mid_point:]
        
        first_count = len(first_half)
        second_count = len(second_half)
        
        if first_count == 0:
            return 0.0
        
        growth_rate = (second_count - first_count) / first_count
        return growth_rate
