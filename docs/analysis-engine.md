# 分析エンジン設計

## 概要

NotionとObsidianのコンテンツを分析し、インサイトを生成する軽量な分析エンジンを設計します。データベースを設けず、既存のプラットフォームの機能を最大限活用する設計です。

## アーキテクチャ

```
┌─────────────────────────────────────────────────────────────┐
│                    Analysis Engine                          │
├─────────────────────────────────────────────────────────────┤
│  Content Analyzer │ Insight Generator │ Recommendation    │
│  • テキスト分析    │  • インサイト生成  │  • 推奨生成        │
│  • 類似度計算      │  • 可視化          │  • アクション提案    │
│  • 重複検出        │  • レポート生成    │  • 優先度付け      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                External Platform Integration                 │
├─────────────────────────────────────────────────────────────┤
│  Notion API │ Obsidian FS │ AI Services │ File Storage      │
│  • コンテンツ取得  │  • ファイル監視  │  • NLP処理    │  • 一時保存    │
│  • 結果反映      │  • メタデータ    │  • 分析処理    │  • キャッシュ  │
│  • 自動化実行    │  • リンク解析    │  • 推奨生成    │  • ログ       │
└─────────────────────────────────────────────────────────────┘
```

## 主要コンポーネント

### 1. コンテンツアナライザー

**役割**: テキスト分析とメトリクス計算
**機能**:
- テキスト前処理
- 特徴量抽出
- 類似度計算
- 重複検出
- トピック分析

**実装例**:
```python
class ContentAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("ja_core_news_sm")
        self.vectorizer = TfidfVectorizer()
        self.similarity_threshold = 0.8
    
    def analyze_text(self, text):
        """テキストの基本分析"""
        doc = self.nlp(text)
        
        return {
            'word_count': len(doc),
            'sentence_count': len(list(doc.sents)),
            'entities': [(ent.text, ent.label_) for ent in doc.ents],
            'keywords': self.extract_keywords(text),
            'sentiment': self.analyze_sentiment(text)
        }
    
    def calculate_similarity(self, text1, text2):
        """テキスト間の類似度計算"""
        vector1 = self.vectorizer.fit_transform([text1])
        vector2 = self.vectorizer.fit_transform([text2])
        
        similarity = cosine_similarity(vector1, vector2)[0][0]
        return similarity
    
    def detect_duplicates(self, texts):
        """重複コンテンツの検出"""
        duplicates = []
        
        for i, text1 in enumerate(texts):
            for j, text2 in enumerate(texts[i+1:], i+1):
                similarity = self.calculate_similarity(text1, text2)
                if similarity > self.similarity_threshold:
                    duplicates.append({
                        'text1_index': i,
                        'text2_index': j,
                        'similarity': similarity
                    })
        
        return duplicates
```

### 2. インサイト生成器

**役割**: 分析結果から洞察を生成
**機能**:
- パターン認識
- トレンド分析
- 異常検出
- インサイト生成
- 可視化データ生成

**実装例**:
```python
class InsightGenerator:
    def __init__(self):
        self.insight_templates = {
            'similarity': "類似度{similarity}%のコンテンツが見つかりました",
            'duplicate': "重複度{duplicate}%のコンテンツが検出されました",
            'topic': "新しいトピック '{topic}' が発見されました",
            'trend': "トレンド '{trend}' が{period}期間で{change}%変化しました"
        }
    
    def generate_insights(self, analysis_results):
        """分析結果からインサイトを生成"""
        insights = []
        
        # 類似度インサイト
        for result in analysis_results.get('similarity', []):
            if result['similarity'] > 0.7:
                insights.append({
                    'type': 'similarity',
                    'content': self.insight_templates['similarity'].format(
                        similarity=round(result['similarity'] * 100)
                    ),
                    'confidence': result['similarity'],
                    'action': 'link_related_content'
                })
        
        # 重複インサイト
        for result in analysis_results.get('duplicates', []):
            insights.append({
                'type': 'duplicate',
                'content': self.insight_templates['duplicate'].format(
                    duplicate=round(result['similarity'] * 100)
                ),
                'confidence': result['similarity'],
                'action': 'merge_duplicate_content'
            })
        
        return insights
    
    def generate_recommendations(self, insights):
        """インサイトから推奨アクションを生成"""
        recommendations = []
        
        for insight in insights:
            if insight['type'] == 'similarity':
                recommendations.append({
                    'action': 'create_link',
                    'description': '関連コンテンツ間のリンクを作成',
                    'priority': 'medium',
                    'estimated_time': '5分'
                })
            elif insight['type'] == 'duplicate':
                recommendations.append({
                    'action': 'merge_content',
                    'description': '重複コンテンツを統合',
                    'priority': 'high',
                    'estimated_time': '15分'
                })
        
        return recommendations
```

### 3. 推奨システム

**役割**: アクションアイテムの提案と優先度付け
**機能**:
- 推奨アルゴリズム
- 優先度計算
- アクション生成
- 実行可能性評価

**実装例**:
```python
class RecommendationSystem:
    def __init__(self):
        self.action_templates = {
            'create_link': {
                'title': '関連コンテンツのリンク作成',
                'description': '類似度の高いコンテンツ間のリンクを作成',
                'steps': [
                    '関連コンテンツを特定',
                    'リンクを追加',
                    'タグを統一'
                ]
            },
            'merge_duplicate': {
                'title': '重複コンテンツの統合',
                'description': '重複度の高いコンテンツを統合',
                'steps': [
                    '重複コンテンツを比較',
                    '統合計画を策定',
                    '統合を実行',
                    '古いコンテンツをアーカイブ'
                ]
            }
        }
    
    def generate_action_items(self, insights):
        """インサイトからアクションアイテムを生成"""
        action_items = []
        
        for insight in insights:
            action_type = insight.get('action')
            if action_type in self.action_templates:
                template = self.action_templates[action_type]
                
                action_items.append({
                    'title': template['title'],
                    'description': template['description'],
                    'type': action_type,
                    'priority': self.calculate_priority(insight),
                    'estimated_time': self.estimate_time(action_type),
                    'steps': template['steps'],
                    'insight_id': insight.get('id')
                })
        
        return action_items
    
    def calculate_priority(self, insight):
        """インサイトの優先度を計算"""
        confidence = insight.get('confidence', 0)
        impact = self.estimate_impact(insight)
        
        priority_score = confidence * impact
        
        if priority_score > 0.8:
            return 'high'
        elif priority_score > 0.5:
            return 'medium'
        else:
            return 'low'
    
    def estimate_time(self, action_type):
        """アクションの実行時間を推定"""
        time_estimates = {
            'create_link': '5分',
            'merge_duplicate': '15分',
            'add_tag': '2分',
            'create_summary': '10分'
        }
        return time_estimates.get(action_type, '10分')
```

## 分析パイプライン

### 1. データ収集

**目的**: NotionとObsidianからコンテンツを収集
**実装**:

```python
class DataCollector:
    def __init__(self, notion_client, obsidian_path):
        self.notion_client = notion_client
        self.obsidian_path = obsidian_path
    
    def collect_notion_content(self):
        """Notionからコンテンツを収集"""
        content = []
        
        # ページの取得
        pages = self.notion_client.search(query="", filter={"property": "object", "value": "page"})
        
        for page in pages:
            content.append({
                'source': 'notion',
                'id': page['id'],
                'title': page['properties']['title']['title'][0]['text']['content'],
                'content': self.extract_page_content(page),
                'created_time': page['created_time'],
                'last_edited_time': page['last_edited_time']
            })
        
        return content
    
    def collect_obsidian_content(self):
        """Obsidianからコンテンツを収集"""
        content = []
        
        for root, dirs, files in os.walk(self.obsidian_path):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content_text = f.read()
                    
                    content.append({
                        'source': 'obsidian',
                        'id': file_path,
                        'title': file,
                        'content': content_text,
                        'created_time': os.path.getctime(file_path),
                        'last_edited_time': os.path.getmtime(file_path)
                    })
        
        return content
```

### 2. 分析実行

**目的**: 収集したコンテンツを分析
**実装**:

```python
class AnalysisPipeline:
    def __init__(self):
        self.analyzer = ContentAnalyzer()
        self.insight_generator = InsightGenerator()
        self.recommendation_system = RecommendationSystem()
    
    def run_analysis(self, content_list):
        """分析パイプラインの実行"""
        results = {
            'similarity': [],
            'duplicates': [],
            'topics': [],
            'insights': [],
            'recommendations': []
        }
        
        # 類似度分析
        results['similarity'] = self.analyze_similarity(content_list)
        
        # 重複検出
        results['duplicates'] = self.detect_duplicates(content_list)
        
        # トピック分析
        results['topics'] = self.analyze_topics(content_list)
        
        # インサイト生成
        results['insights'] = self.insight_generator.generate_insights(results)
        
        # 推奨生成
        results['recommendations'] = self.recommendation_system.generate_action_items(results['insights'])
        
        return results
    
    def analyze_similarity(self, content_list):
        """類似度分析"""
        similarities = []
        
        for i, content1 in enumerate(content_list):
            for j, content2 in enumerate(content_list[i+1:], i+1):
                similarity = self.analyzer.calculate_similarity(
                    content1['content'], 
                    content2['content']
                )
                
                if similarity > 0.5:  # 閾値以上の場合のみ記録
                    similarities.append({
                        'content1': content1,
                        'content2': content2,
                        'similarity': similarity
                    })
        
        return similarities
    
    def detect_duplicates(self, content_list):
        """重複検出"""
        texts = [content['content'] for content in content_list]
        duplicates = self.analyzer.detect_duplicates(texts)
        
        # 結果を元のコンテンツ情報と結合
        for duplicate in duplicates:
            duplicate['content1'] = content_list[duplicate['text1_index']]
            duplicate['content2'] = content_list[duplicate['text2_index']]
            del duplicate['text1_index']
            del duplicate['text2_index']
        
        return duplicates
```

### 3. 結果反映

**目的**: 分析結果をNotionとObsidianに反映
**実装**:

```python
class ResultReflector:
    def __init__(self, notion_client, obsidian_path):
        self.notion_client = notion_client
        self.obsidian_path = obsidian_path
    
    def reflect_to_notion(self, analysis_results):
        """分析結果をNotionに反映"""
        # 分析結果データベースに追加
        for insight in analysis_results['insights']:
            self.create_notion_insight_page(insight)
        
        # 推奨アクションをタスクデータベースに追加
        for recommendation in analysis_results['recommendations']:
            self.create_notion_task(recommendation)
    
    def reflect_to_obsidian(self, analysis_results):
        """分析結果をObsidianに反映"""
        # 分析結果ノートを作成
        for insight in analysis_results['insights']:
            self.create_obsidian_insight_note(insight)
        
        # 重複検出ノートを作成
        for duplicate in analysis_results['duplicates']:
            self.create_obsidian_duplicate_note(duplicate)
    
    def create_notion_insight_page(self, insight):
        """Notionにインサイトページを作成"""
        page_data = {
            'parent': {'database_id': 'insights_database_id'},
            'properties': {
                'タイトル': {'title': [{'text': {'content': insight['content']}}]},
                'タイプ': {'select': {'name': insight['type']}},
                '信頼度': {'number': insight['confidence']},
                'ステータス': {'select': {'name': '未実行'}}
            }
        }
        
        self.notion_client.pages.create(**page_data)
    
    def create_obsidian_insight_note(self, insight):
        """Obsidianにインサイトノートを作成"""
        note_content = f"""# 💡 インサイト: {insight['content']}

## 📋 基本情報
- **タイプ**: {insight['type']}
- **信頼度**: {insight['confidence']}%
- **生成日時**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 🔍 詳細
{insight['content']}

## ⚡ 推奨アクション
{insight.get('action', 'アクション未設定')}

## 🏷️ タグ
#insight #{insight['type']} #{'high' if insight['confidence'] > 0.8 else 'medium' if insight['confidence'] > 0.5 else 'low'}
"""
        
        filename = f"Insights/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{insight['type']}.md"
        filepath = os.path.join(self.obsidian_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(note_content)
```

## 技術スタック

### 1. 自然言語処理

**ライブラリ**:
- **spaCy**: 高性能なNLPライブラリ
- **NLTK**: 自然言語処理ツールキット
- **scikit-learn**: 機械学習アルゴリズム
- **transformers**: 事前学習モデル

**実装例**:
```python
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline

class NLPAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("ja_core_news_sm")
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.sentiment_analyzer = pipeline("sentiment-analysis")
    
    def analyze_text(self, text):
        doc = self.nlp(text)
        
        return {
            'tokens': [token.text for token in doc],
            'entities': [(ent.text, ent.label_) for ent in doc.ents],
            'sentiment': self.sentiment_analyzer(text)[0],
            'keywords': self.extract_keywords(text)
        }
    
    def extract_keywords(self, text):
        doc = self.nlp(text)
        keywords = []
        
        for token in doc:
            if token.pos_ in ['NOUN', 'ADJ', 'VERB'] and not token.is_stop:
                keywords.append(token.lemma_)
        
        return list(set(keywords))
```

### 2. グラフ分析

**ライブラリ**:
- **NetworkX**: グラフ分析
- **matplotlib**: 可視化
- **plotly**: インタラクティブ可視化

**実装例**:
```python
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go

class GraphAnalyzer:
    def __init__(self):
        self.graph = nx.Graph()
    
    def build_graph(self, content_list):
        """コンテンツからグラフを構築"""
        for content in content_list:
            self.graph.add_node(content['id'], **content)
        
        # 類似度に基づいてエッジを追加
        for i, content1 in enumerate(content_list):
            for j, content2 in enumerate(content_list[i+1:], i+1):
                similarity = self.calculate_similarity(content1, content2)
                if similarity > 0.5:
                    self.graph.add_edge(content1['id'], content2['id'], weight=similarity)
    
    def analyze_graph(self):
        """グラフの分析"""
        return {
            'nodes': self.graph.number_of_nodes(),
            'edges': self.graph.number_of_edges(),
            'density': nx.density(self.graph),
            'clustering': nx.average_clustering(self.graph),
            'centrality': nx.degree_centrality(self.graph)
        }
    
    def visualize_graph(self):
        """グラフの可視化"""
        pos = nx.spring_layout(self.graph)
        
        fig = go.Figure()
        
        # ノードの追加
        for node in self.graph.nodes():
            x, y = pos[node]
            fig.add_trace(go.Scatter(
                x=[x], y=[y],
                mode='markers+text',
                text=[node],
                textposition="middle center",
                marker=dict(size=20, color='blue')
            ))
        
        # エッジの追加
        for edge in self.graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            fig.add_trace(go.Scatter(
                x=[x0, x1], y=[y0, y1],
                mode='lines',
                line=dict(width=2, color='gray')
            ))
        
        fig.update_layout(showlegend=False)
        return fig
```

### 3. 外部API統合

**ライブラリ**:
- **requests**: HTTP クライアント
- **notion-client**: Notion API
- **watchdog**: ファイルシステム監視

**実装例**:
```python
import requests
from notion_client import Client
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ExternalAPIIntegration:
    def __init__(self, notion_token, obsidian_path):
        self.notion_client = Client(auth=notion_token)
        self.obsidian_path = obsidian_path
        self.observer = Observer()
    
    def setup_notion_integration(self):
        """Notion統合の設定"""
        # データベースの作成
        databases = {
            'insights': self.create_insights_database(),
            'tasks': self.create_tasks_database(),
            'analysis_results': self.create_analysis_results_database()
        }
        return databases
    
    def setup_obsidian_integration(self):
        """Obsidian統合の設定"""
        # ファイル監視の設定
        event_handler = ObsidianFileHandler(self.obsidian_path)
        self.observer.schedule(event_handler, self.obsidian_path, recursive=True)
        self.observer.start()
    
    def create_insights_database(self):
        """インサイトデータベースの作成"""
        database = self.notion_client.databases.create(
            parent={'page_id': 'parent_page_id'},
            title='AI分析インサイト',
            properties={
                'タイトル': {'title': {}},
                'タイプ': {'select': {'options': [
                    {'name': 'similarity', 'color': 'blue'},
                    {'name': 'duplicate', 'color': 'red'},
                    {'name': 'topic', 'color': 'green'}
                ]}},
                '信頼度': {'number': {'format': 'percent'}},
                'ステータス': {'select': {'options': [
                    {'name': '未実行', 'color': 'yellow'},
                    {'name': '実行中', 'color': 'blue'},
                    {'name': '完了', 'color': 'green'}
                ]}},
                '作成日時': {'created_time': {}}
            }
        )
        return database

class ObsidianFileHandler(FileSystemEventHandler):
    def __init__(self, obsidian_path):
        self.obsidian_path = obsidian_path
        self.analyzer = ContentAnalyzer()
    
    def on_modified(self, event):
        if event.is_directory:
            return
        
        if event.src_path.endswith('.md'):
            self.analyze_file(event.src_path)
    
    def analyze_file(self, file_path):
        """ファイルの分析"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        analysis = self.analyzer.analyze_text(content)
        self.reflect_analysis(file_path, analysis)
    
    def reflect_analysis(self, file_path, analysis):
        """分析結果の反映"""
        # 分析結果をファイルに追記
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f"\n\n## AI分析結果\n")
            f.write(f"- キーワード: {', '.join(analysis['keywords'])}\n")
            f.write(f"- 感情: {analysis['sentiment']['label']}\n")
            f.write(f"- 信頼度: {analysis['sentiment']['score']}\n")
```

## 運用考慮事項

### 1. パフォーマンス

**最適化項目**:
- 分析処理の並列化
- キャッシュの活用
- メモリ使用量の最適化

**監視項目**:
- 分析処理時間
- メモリ使用量
- CPU使用率

### 2. スケーラビリティ

**考慮事項**:
- 大量データの処理
- 分析処理の分散
- リソースの動的調整

**対策**:
- バッチ処理の実装
- 非同期処理の活用
- クラウドリソースの活用

### 3. メンテナンス

**定期作業**:
- 分析モデルの更新
- パフォーマンスの監視
- エラーログの確認

**監視項目**:
- 分析精度
- 処理時間
- エラー率
