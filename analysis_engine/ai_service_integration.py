"""
外部AIサービスとの連携
OpenAI、Anthropicなどの外部AIサービスを活用した高度な分析機能
"""
import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import requests

logger = logging.getLogger(__name__)

class AIServiceIntegration:
    """外部AIサービスとの連携クラス"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.openai_base_url = "https://api.openai.com/v1"
        self.anthropic_base_url = "https://api.anthropic.com/v1"
        
        # デフォルトの設定
        self.default_model = "gpt-3.5-turbo"
        self.max_tokens = 1000
        self.temperature = 0.7
    
    def generate_summary(self, text: str, max_length: int = 200) -> Dict[str, Any]:
        """
        テキストの要約生成
        """
        try:
            if self.openai_api_key:
                return self._generate_summary_openai(text, max_length)
            elif self.anthropic_api_key:
                return self._generate_summary_anthropic(text, max_length)
            else:
                return self._generate_summary_fallback(text, max_length)
                
        except Exception as e:
            logger.error(f"Summary generation failed: {e}")
            return self._generate_summary_fallback(text, max_length)
    
    def generate_insights(self, content_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        コンテンツからインサイトを生成
        """
        try:
            if self.openai_api_key:
                return self._generate_insights_openai(content_list)
            elif self.anthropic_api_key:
                return self._generate_insights_anthropic(content_list)
            else:
                return self._generate_insights_fallback(content_list)
                
        except Exception as e:
            logger.error(f"Insights generation failed: {e}")
            return self._generate_insights_fallback(content_list)
    
    def generate_recommendations(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析結果から推奨事項を生成
        """
        try:
            if self.openai_api_key:
                return self._generate_recommendations_openai(analysis_results)
            elif self.anthropic_api_key:
                return self._generate_recommendations_anthropic(analysis_results)
            else:
                return self._generate_recommendations_fallback(analysis_results)
                
        except Exception as e:
            logger.error(f"Recommendations generation failed: {e}")
            return self._generate_recommendations_fallback(analysis_results)
    
    def analyze_content_quality(self, text: str) -> Dict[str, Any]:
        """
        コンテンツの品質分析
        """
        try:
            if self.openai_api_key:
                return self._analyze_quality_openai(text)
            elif self.anthropic_api_key:
                return self._analyze_quality_anthropic(text)
            else:
                return self._analyze_quality_fallback(text)
                
        except Exception as e:
            logger.error(f"Quality analysis failed: {e}")
            return self._analyze_quality_fallback(text)
    
    def _generate_summary_openai(self, text: str, max_length: int) -> Dict[str, Any]:
        """OpenAIを使用した要約生成"""
        try:
            prompt = f"""
            以下のテキストを{max_length}文字以内で要約してください：
            
            {text}
            
            要約は以下の点に注意してください：
            - 主要なポイントを簡潔にまとめる
            - 重要なキーワードを含める
            - 読みやすく整理する
            """
            
            response = self._call_openai_api(prompt)
            
            return {
                'summary': response,
                'method': 'openai',
                'max_length': max_length,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"OpenAI summary generation failed: {e}")
            return self._generate_summary_fallback(text, max_length)
    
    def _generate_summary_anthropic(self, text: str, max_length: int) -> Dict[str, Any]:
        """Anthropicを使用した要約生成"""
        try:
            prompt = f"""
            以下のテキストを{max_length}文字以内で要約してください：
            
            {text}
            
            要約は以下の点に注意してください：
            - 主要なポイントを簡潔にまとめる
            - 重要なキーワードを含める
            - 読みやすく整理する
            """
            
            response = self._call_anthropic_api(prompt)
            
            return {
                'summary': response,
                'method': 'anthropic',
                'max_length': max_length,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Anthropic summary generation failed: {e}")
            return self._generate_summary_fallback(text, max_length)
    
    def _generate_summary_fallback(self, text: str, max_length: int) -> Dict[str, Any]:
        """フォールバック要約生成（AIサービスなし）"""
        try:
            # 簡単な要約生成
            sentences = text.split('. ')
            if len(sentences) <= 2:
                summary = text
            else:
                # 最初の2文を要約として使用
                summary = '. '.join(sentences[:2]) + '.'
            
            # 長さ制限
            if len(summary) > max_length:
                summary = summary[:max_length-3] + '...'
            
            return {
                'summary': summary,
                'method': 'fallback',
                'max_length': max_length,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Fallback summary generation failed: {e}")
            return {
                'summary': text[:max_length] if len(text) > max_length else text,
                'method': 'fallback',
                'max_length': max_length,
                'generated_at': datetime.now().isoformat()
            }
    
    def _generate_insights_openai(self, content_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """OpenAIを使用したインサイト生成"""
        try:
            # コンテンツの準備
            content_text = ""
            for i, content in enumerate(content_list[:5]):  # 最大5件
                content_text += f"コンテンツ{i+1}: {content.get('text', '')}\n\n"
            
            prompt = f"""
            以下のコンテンツを分析して、インサイトを生成してください：
            
            {content_text}
            
            以下の観点から分析してください：
            1. 共通のテーマやパターン
            2. 重要なキーワードや概念
            3. 潜在的な関連性
            4. 改善の提案
            5. 今後の方向性
            
            インサイトは簡潔で実用的なものにしてください。
            """
            
            response = self._call_openai_api(prompt)
            
            return {
                'insights': response,
                'method': 'openai',
                'content_count': len(content_list),
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"OpenAI insights generation failed: {e}")
            return self._generate_insights_fallback(content_list)
    
    def _generate_insights_anthropic(self, content_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Anthropicを使用したインサイト生成"""
        try:
            # コンテンツの準備
            content_text = ""
            for i, content in enumerate(content_list[:5]):  # 最大5件
                content_text += f"コンテンツ{i+1}: {content.get('text', '')}\n\n"
            
            prompt = f"""
            以下のコンテンツを分析して、インサイトを生成してください：
            
            {content_text}
            
            以下の観点から分析してください：
            1. 共通のテーマやパターン
            2. 重要なキーワードや概念
            3. 潜在的な関連性
            4. 改善の提案
            5. 今後の方向性
            
            インサイトは簡潔で実用的なものにしてください。
            """
            
            response = self._call_anthropic_api(prompt)
            
            return {
                'insights': response,
                'method': 'anthropic',
                'content_count': len(content_list),
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Anthropic insights generation failed: {e}")
            return self._generate_insights_fallback(content_list)
    
    def _generate_insights_fallback(self, content_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """フォールバックインサイト生成"""
        try:
            # 簡単なインサイト生成
            all_text = " ".join([content.get('text', '') for content in content_list])
            
            # キーワードの頻度分析
            words = all_text.lower().split()
            word_freq = {}
            for word in words:
                if len(word) > 3:  # 3文字以上の単語のみ
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # 頻度の高いキーワード
            top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
            
            insights = f"""
            分析結果：
            1. 総コンテンツ数: {len(content_list)}
            2. 主要キーワード: {', '.join([kw for kw, freq in top_keywords])}
            3. 平均単語数: {len(all_text.split()) // len(content_list) if content_list else 0}
            4. 推奨事項: コンテンツの整理とタグ付けを検討
            """
            
            return {
                'insights': insights,
                'method': 'fallback',
                'content_count': len(content_list),
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Fallback insights generation failed: {e}")
            return {
                'insights': 'インサイトの生成に失敗しました。',
                'method': 'fallback',
                'content_count': len(content_list),
                'generated_at': datetime.now().isoformat()
            }
    
    def _generate_recommendations_openai(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """OpenAIを使用した推奨事項生成"""
        try:
            prompt = f"""
            以下の分析結果を基に、実用的な推奨事項を生成してください：
            
            分析結果:
            {json.dumps(analysis_results, ensure_ascii=False, indent=2)}
            
            以下の形式で推奨事項を提供してください：
            1. 優先度: 高/中/低
            2. 推奨事項のタイトル
            3. 具体的なアクション
            4. 期待される効果
            5. 実行の難易度
            
            推奨事項は実用的で実行可能なものにしてください。
            """
            
            response = self._call_openai_api(prompt)
            
            return {
                'recommendations': response,
                'method': 'openai',
                'analysis_type': analysis_results.get('type', 'unknown'),
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"OpenAI recommendations generation failed: {e}")
            return self._generate_recommendations_fallback(analysis_results)
    
    def _generate_recommendations_anthropic(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Anthropicを使用した推奨事項生成"""
        try:
            prompt = f"""
            以下の分析結果を基に、実用的な推奨事項を生成してください：
            
            分析結果:
            {json.dumps(analysis_results, ensure_ascii=False, indent=2)}
            
            以下の形式で推奨事項を提供してください：
            1. 優先度: 高/中/低
            2. 推奨事項のタイトル
            3. 具体的なアクション
            4. 期待される効果
            5. 実行の難易度
            
            推奨事項は実用的で実行可能なものにしてください。
            """
            
            response = self._call_anthropic_api(prompt)
            
            return {
                'recommendations': response,
                'method': 'anthropic',
                'analysis_type': analysis_results.get('type', 'unknown'),
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Anthropic recommendations generation failed: {e}")
            return self._generate_recommendations_fallback(analysis_results)
    
    def _generate_recommendations_fallback(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """フォールバック推奨事項生成"""
        try:
            recommendations = """
            推奨事項：
            1. 優先度: 中 - コンテンツの整理とタグ付け
            2. 優先度: 低 - 定期的な分析の実行
            3. 優先度: 高 - 重複コンテンツの統合
            
            具体的なアクション：
            - 関連するコンテンツをグループ化
            - 適切なタグを付与
            - 定期的な分析のスケジュール化
            """
            
            return {
                'recommendations': recommendations,
                'method': 'fallback',
                'analysis_type': analysis_results.get('type', 'unknown'),
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Fallback recommendations generation failed: {e}")
            return {
                'recommendations': '推奨事項の生成に失敗しました。',
                'method': 'fallback',
                'analysis_type': analysis_results.get('type', 'unknown'),
                'generated_at': datetime.now().isoformat()
            }
    
    def _analyze_quality_openai(self, text: str) -> Dict[str, Any]:
        """OpenAIを使用した品質分析"""
        try:
            prompt = f"""
            以下のテキストの品質を分析してください：
            
            {text}
            
            以下の観点から評価してください：
            1. 読みやすさ (1-10点)
            2. 情報の完全性 (1-10点)
            3. 構造の明確さ (1-10点)
            4. 専門性 (1-10点)
            5. 改善点
            
            評価は具体的で建設的なものにしてください。
            """
            
            response = self._call_openai_api(prompt)
            
            return {
                'quality_analysis': response,
                'method': 'openai',
                'text_length': len(text),
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"OpenAI quality analysis failed: {e}")
            return self._analyze_quality_fallback(text)
    
    def _analyze_quality_anthropic(self, text: str) -> Dict[str, Any]:
        """Anthropicを使用した品質分析"""
        try:
            prompt = f"""
            以下のテキストの品質を分析してください：
            
            {text}
            
            以下の観点から評価してください：
            1. 読みやすさ (1-10点)
            2. 情報の完全性 (1-10点)
            3. 構造の明確さ (1-10点)
            4. 専門性 (1-10点)
            5. 改善点
            
            評価は具体的で建設的なものにしてください。
            """
            
            response = self._call_anthropic_api(prompt)
            
            return {
                'quality_analysis': response,
                'method': 'anthropic',
                'text_length': len(text),
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Anthropic quality analysis failed: {e}")
            return self._analyze_quality_fallback(text)
    
    def _analyze_quality_fallback(self, text: str) -> Dict[str, Any]:
        """フォールバック品質分析"""
        try:
            # 簡単な品質分析
            word_count = len(text.split())
            char_count = len(text)
            sentence_count = len(text.split('.'))
            
            # 基本的な品質指標
            readability_score = min(word_count / 10, 10)  # 簡易的な読みやすさ
            completeness_score = min(sentence_count / 5, 10)  # 簡易的な完全性
            structure_score = min(len(text.split('\n')) / 3, 10)  # 簡易的な構造
            
            quality_analysis = f"""
            品質分析結果：
            1. 読みやすさ: {readability_score:.1f}/10
            2. 情報の完全性: {completeness_score:.1f}/10
            3. 構造の明確さ: {structure_score:.1f}/10
            4. 専門性: 5.0/10 (デフォルト)
            
            改善点：
            - より詳細な分析には外部AIサービスの設定が必要です
            - 現在は基本的な統計情報のみを提供しています
            """
            
            return {
                'quality_analysis': quality_analysis,
                'method': 'fallback',
                'text_length': len(text),
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Fallback quality analysis failed: {e}")
            return {
                'quality_analysis': '品質分析に失敗しました。',
                'method': 'fallback',
                'text_length': len(text),
                'generated_at': datetime.now().isoformat()
            }
    
    def _call_openai_api(self, prompt: str) -> str:
        """OpenAI APIの呼び出し"""
        try:
            headers = {
                'Authorization': f'Bearer {self.openai_api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': self.default_model,
                'messages': [
                    {'role': 'user', 'content': prompt}
                ],
                'max_tokens': self.max_tokens,
                'temperature': self.temperature
            }
            
            response = requests.post(
                f'{self.openai_base_url}/chat/completions',
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
                return "OpenAI API呼び出しに失敗しました。"
                
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            return "OpenAI API呼び出しに失敗しました。"
    
    def _call_anthropic_api(self, prompt: str) -> str:
        """Anthropic APIの呼び出し"""
        try:
            headers = {
                'x-api-key': self.anthropic_api_key,
                'Content-Type': 'application/json',
                'anthropic-version': '2023-06-01'
            }
            
            data = {
                'model': 'claude-3-sonnet-20240229',
                'max_tokens': self.max_tokens,
                'messages': [
                    {'role': 'user', 'content': prompt}
                ]
            }
            
            response = requests.post(
                f'{self.anthropic_base_url}/messages',
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['content'][0]['text']
            else:
                logger.error(f"Anthropic API error: {response.status_code} - {response.text}")
                return "Anthropic API呼び出しに失敗しました。"
                
        except Exception as e:
            logger.error(f"Anthropic API call failed: {e}")
            return "Anthropic API呼び出しに失敗しました。"
