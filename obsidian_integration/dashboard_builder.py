"""
Obsidian ダッシュボードビルダー
Obsidianダッシュボードの構築と管理を行う
"""
import logging
import os
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

class ObsidianDashboardBuilder:
    """Obsidianダッシュボードビルダークラス"""
    
    def __init__(self, vault_path: str):
        self.vault_path = vault_path
        self.templates_dir = Path(vault_path) / "Templates"
        self.dashboard_dir = Path(vault_path) / "Dashboard"
        self.insights_dir = Path(vault_path) / "Insights"
        self.analysis_dir = Path(vault_path) / "Analysis"
    
    async def initialize(self):
        """ダッシュボードビルダーの初期化"""
        try:
            logger.info("Initializing Obsidian dashboard builder...")
            
            # ディレクトリの作成
            await self._create_directories()
            
            # テンプレートの作成
            await self._create_templates()
            
            # ダッシュボードの作成
            await self._create_dashboard()
            
            logger.info("Obsidian dashboard builder initialized successfully")
            
        except Exception as e:
            logger.error(f"Dashboard builder initialization failed: {e}")
            raise
    
    async def _create_directories(self):
        """必要なディレクトリの作成"""
        try:
            directories = [
                self.templates_dir,
                self.dashboard_dir,
                self.insights_dir,
                self.analysis_dir
            ]
            
            for directory in directories:
                directory.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created directory: {directory}")
            
        except Exception as e:
            logger.error(f"Directory creation failed: {e}")
            raise
    
    async def _create_templates(self):
        """テンプレートの作成"""
        try:
            # 分析レポートテンプレート
            await self._create_analysis_report_template()
            
            # インサイトテンプレート
            await self._create_insight_template()
            
            # 重複統合テンプレート
            await self._create_duplicate_integration_template()
            
            logger.info("Templates created successfully")
            
        except Exception as e:
            logger.error(f"Template creation failed: {e}")
    
    async def _create_analysis_report_template(self):
        """分析レポートテンプレートの作成"""
        try:
            template_content = """# 📊 分析レポート

## 📋 基本情報
- **分析日時**: {{date:YYYY-MM-DD HH:mm}}
- **分析タイプ**: {{分析タイプ}}
- **対象ノート**: [[{{対象ノート}}]]
- **信頼度**: {{信頼度}}%

## 🔍 分析結果
{{分析結果の詳細}}

## 📈 メトリクス
- **類似度スコア**: {{類似度スコア}}
- **重要度スコア**: {{重要度スコア}}
- **関連ノート数**: {{関連ノート数}}

## 🔗 関連ノート
{{関連ノートのリスト}}

## ⚡ 推奨アクション
{{推奨アクションのリスト}}

## 📝 ユーザーメモ
{{ユーザーのメモ}}

## 🏷️ タグ
#analysis #{{分析タイプ}} #{{信頼度レベル}}"""
            
            template_path = self.templates_dir / "Analysis Report.md"
            await self._write_file(template_path, template_content)
            
        except Exception as e:
            logger.error(f"Analysis report template creation failed: {e}")
    
    async def _create_insight_template(self):
        """インサイトテンプレートの作成"""
        try:
            template_content = """# 💡 インサイト: {{インサイトタイトル}}

## 🎯 発見
{{発見した内容}}

## 🔍 分析
{{分析の詳細}}

## 💭 考察
{{考察と思考}}

## 🔗 関連概念
{{関連概念のリスト}}

## 📚 参考資料
{{参考資料のリスト}}

## 🎯 次のアクション
{{アクションアイテムのリスト}}

## 📝 メモ
{{追加メモ}}

## 🏷️ タグ
#insight #{{カテゴリ}} #{{重要度}}"""
            
            template_path = self.templates_dir / "Insight.md"
            await self._write_file(template_path, template_content)
            
        except Exception as e:
            logger.error(f"Insight template creation failed: {e}")
    
    async def _create_duplicate_integration_template(self):
        """重複統合テンプレートの作成"""
        try:
            template_content = """# 🔄 重複統合: {{統合対象}}

## 📋 統合対象ノート
{{統合対象ノートのリスト}}

## 🔍 重複分析
{{重複分析の詳細}}

## ⚡ 統合計画
{{統合計画の詳細}}

## 📝 統合メモ
{{統合時のメモ}}

## ✅ 統合完了
- [ ] 統合実行
- [ ] リンク更新
- [ ] タグ整理
- [ ] アーカイブ

## 🏷️ タグ
#duplicate #integration #{{ステータス}}"""
            
            template_path = self.templates_dir / "Duplicate Integration.md"
            await self._write_file(template_path, template_content)
            
        except Exception as e:
            logger.error(f"Duplicate integration template creation failed: {e}")
    
    async def _create_dashboard(self):
        """メインダッシュボードの作成"""
        try:
            dashboard_content = """# 🧠 Obsidian Knowledge Dashboard

## 📊 グラフビュー
```dataview
TABLE file.name as "ノート名", file.mtime as "更新日時"
FROM ""
WHERE file.name != "Obsidian Knowledge Dashboard"
SORT file.mtime DESC
LIMIT 10
```

## 🔍 最近の分析結果
```dataview
TABLE title as "タイトル", type as "タイプ", confidence as "信頼度"
FROM "Insights"
SORT file.mtime DESC
LIMIT 5
```

## ⚡ 推奨アクション
```dataview
TABLE title as "アクション", priority as "優先度", estimated_time as "推定時間"
FROM "Analysis"
WHERE status = "pending"
SORT priority DESC
LIMIT 5
```

## 🔗 重複候補
```dataview
TABLE title as "タイトル", similarity as "類似度"
FROM "Analysis"
WHERE type = "duplicate"
SORT similarity DESC
LIMIT 5
```

## 🏷️ 人気タグ
```dataview
TABLE length(rows) as "使用回数"
FROM ""
FLATTEN file.tags as tag
GROUP BY tag
SORT length(rows) DESC
LIMIT 10
```"""
            
            dashboard_path = self.dashboard_dir / "Obsidian Knowledge Dashboard.md"
            await self._write_file(dashboard_path, dashboard_content)
            
        except Exception as e:
            logger.error(f"Dashboard creation failed: {e}")
    
    async def _write_file(self, file_path: Path, content: str) -> bool:
        """ファイルに内容を書き込み"""
        try:
            # ディレクトリが存在しない場合は作成
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"File written: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"File writing failed: {e}")
            return False
    
    async def create_insight_note(self, insight_data: Dict[str, Any]) -> Optional[str]:
        """インサイトノートの作成"""
        try:
            # インサイトノートの内容を生成
            content = self._generate_insight_content(insight_data)
            
            # ファイル名を生成
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"Insight_{insight_data.get('type', 'unknown')}_{timestamp}.md"
            file_path = self.insights_dir / filename
            
            # ファイルを作成
            success = await self._write_file(file_path, content)
            
            if success:
                logger.info(f"Created insight note: {file_path}")
                return str(file_path)
            else:
                return None
                
        except Exception as e:
            logger.error(f"Insight note creation failed: {e}")
            return None
    
    async def create_analysis_note(self, analysis_data: Dict[str, Any]) -> Optional[str]:
        """分析ノートの作成"""
        try:
            # 分析ノートの内容を生成
            content = self._generate_analysis_content(analysis_data)
            
            # ファイル名を生成
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"Analysis_{analysis_data.get('type', 'unknown')}_{timestamp}.md"
            file_path = self.analysis_dir / filename
            
            # ファイルを作成
            success = await self._write_file(file_path, content)
            
            if success:
                logger.info(f"Created analysis note: {file_path}")
                return str(file_path)
            else:
                return None
                
        except Exception as e:
            logger.error(f"Analysis note creation failed: {e}")
            return None
    
    async def create_duplicate_note(self, duplicate_data: Dict[str, Any]) -> Optional[str]:
        """重複ノートの作成"""
        try:
            # 重複ノートの内容を生成
            content = self._generate_duplicate_content(duplicate_data)
            
            # ファイル名を生成
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"Duplicate_{timestamp}.md"
            file_path = self.analysis_dir / filename
            
            # ファイルを作成
            success = await self._write_file(file_path, content)
            
            if success:
                logger.info(f"Created duplicate note: {file_path}")
                return str(file_path)
            else:
                return None
                
        except Exception as e:
            logger.error(f"Duplicate note creation failed: {e}")
            return None
    
    def _generate_insight_content(self, insight_data: Dict[str, Any]) -> str:
        """インサイトノートの内容を生成"""
        try:
            content = f"""# 💡 インサイト: {insight_data.get('title', 'New Insight')}

## 📋 基本情報
- **タイプ**: {insight_data.get('type', 'unknown')}
- **信頼度**: {insight_data.get('confidence', 0.0)}%
- **生成日時**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 🔍 詳細
{insight_data.get('content', 'No content available')}

## ⚡ 推奨アクション
{insight_data.get('action', 'No action specified')}

## 📝 メモ
{{ユーザーのメモをここに記入}}

## 🏷️ タグ
#insight #{insight_data.get('type', 'unknown')} #{'high' if insight_data.get('confidence', 0) > 0.8 else 'medium' if insight_data.get('confidence', 0) > 0.5 else 'low'}"""
            
            return content
            
        except Exception as e:
            logger.error(f"Insight content generation failed: {e}")
            return ""
    
    def _generate_analysis_content(self, analysis_data: Dict[str, Any]) -> str:
        """分析ノートの内容を生成"""
        try:
            content = f"""# 📊 分析結果: {analysis_data.get('title', 'New Analysis')}

## 📋 基本情報
- **分析タイプ**: {analysis_data.get('type', 'unknown')}
- **対象ノート**: [[{analysis_data.get('target_note', 'Unknown')}]]
- **信頼度**: {analysis_data.get('confidence', 0.0)}%

## 🔍 分析結果
{analysis_data.get('result', 'No result available')}

## 📈 メトリクス
- **類似度スコア**: {analysis_data.get('similarity_score', 0.0)}
- **重要度スコア**: {analysis_data.get('importance_score', 0.0)}
- **関連ノート数**: {analysis_data.get('related_notes_count', 0)}

## 🔗 関連ノート
{analysis_data.get('related_notes', 'No related notes')}

## ⚡ 推奨アクション
{analysis_data.get('recommendations', 'No recommendations')}

## 📝 ユーザーメモ
{{ユーザーのメモをここに記入}}

## 🏷️ タグ
#analysis #{analysis_data.get('type', 'unknown')} #{'high' if analysis_data.get('confidence', 0) > 0.8 else 'medium' if analysis_data.get('confidence', 0) > 0.5 else 'low'}"""
            
            return content
            
        except Exception as e:
            logger.error(f"Analysis content generation failed: {e}")
            return ""
    
    def _generate_duplicate_content(self, duplicate_data: Dict[str, Any]) -> str:
        """重複ノートの内容を生成"""
        try:
            content = f"""# 🔄 重複検出: {duplicate_data.get('title', 'Duplicate Content')}

## 📋 重複ノート一覧
{duplicate_data.get('duplicate_notes', 'No duplicate notes found')}

## 📊 類似度分析
{duplicate_data.get('similarity_analysis', 'No similarity analysis available')}

## 🔍 重複内容の比較
{duplicate_data.get('content_comparison', 'No content comparison available')}

## ⚡ 統合推奨
{duplicate_data.get('integration_recommendation', 'No integration recommendation')}

## 📝 統合メモ
{{統合時のメモをここに記入}}

## ✅ 統合完了
- [ ] 統合実行
- [ ] リンク更新
- [ ] タグ整理
- [ ] アーカイブ

## 🏷️ タグ
#duplicate #integration #pending"""
            
            return content
            
        except Exception as e:
            logger.error(f"Duplicate content generation failed: {e}")
            return ""
    
    async def update_dashboard(self, dashboard_data: Dict[str, Any]) -> bool:
        """ダッシュボードの更新"""
        try:
            # ダッシュボードの内容を生成
            content = self._generate_dashboard_content(dashboard_data)
            
            # ダッシュボードファイルを更新
            dashboard_path = self.dashboard_dir / "Obsidian Knowledge Dashboard.md"
            success = await self._write_file(dashboard_path, content)
            
            if success:
                logger.info("Dashboard updated successfully")
                return True
            else:
                return False
                
        except Exception as e:
            logger.error(f"Dashboard update failed: {e}")
            return False
    
    def _generate_dashboard_content(self, dashboard_data: Dict[str, Any]) -> str:
        """ダッシュボードの内容を生成"""
        try:
            content = f"""# 🧠 Obsidian Knowledge Dashboard

## 📊 同期状況
- **成功**: {dashboard_data.get('sync_success', 0)}件
- **待機中**: {dashboard_data.get('sync_pending', 0)}件
- **エラー**: {dashboard_data.get('sync_error', 0)}件

## 🔍 最近の分析結果
{dashboard_data.get('recent_analysis', 'No recent analysis available')}

## ⚡ 推奨アクション
{dashboard_data.get('recommended_actions', 'No recommended actions available')}

## 🔗 重複候補
{dashboard_data.get('duplicate_candidates', 'No duplicate candidates found')}

## 🏷️ 人気タグ
{dashboard_data.get('popular_tags', 'No popular tags available')}

## 📈 統計情報
- **総ノート数**: {dashboard_data.get('total_notes', 0)}
- **総リンク数**: {dashboard_data.get('total_links', 0)}
- **総タグ数**: {dashboard_data.get('total_tags', 0)}
- **最終更新**: {datetime.now().strftime('%Y-%m-%d %H:%M')}"""
            
            return content
            
        except Exception as e:
            logger.error(f"Dashboard content generation failed: {e}")
            return ""
    
    async def get_dashboard_stats(self) -> Dict[str, Any]:
        """ダッシュボードの統計情報を取得"""
        try:
            stats = {
                'total_notes': 0,
                'total_links': 0,
                'total_tags': 0,
                'recent_notes': [],
                'popular_tags': []
            }
            
            # ノート数のカウント
            vault_path = Path(self.vault_path)
            md_files = list(vault_path.rglob("*.md"))
            stats['total_notes'] = len(md_files)
            
            # 最近のノート
            recent_files = sorted(md_files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]
            stats['recent_notes'] = [str(f.relative_to(vault_path)) for f in recent_files]
            
            return stats
            
        except Exception as e:
            logger.error(f"Dashboard stats retrieval failed: {e}")
            return {}
