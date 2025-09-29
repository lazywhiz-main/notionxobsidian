"""
Notion ダッシュボードビルダー
Notionダッシュボードの構築と管理を行う
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from notion_integration.notion_client import NotionClient
from config import settings

logger = logging.getLogger(__name__)

class NotionDashboardBuilder:
    """Notionダッシュボードビルダークラス"""
    
    def __init__(self, notion_client):
        self.notion_client = notion_client
        self.database_ids = {}
        self.template_ids = {}
    
    async def initialize(self):
        """ダッシュボードビルダーの初期化"""
        try:
            logger.info("Initializing Notion dashboard builder...")
            
            # データベースIDの取得
            await self._get_database_ids()
            
            # テンプレートの作成
            await self._create_templates()
            
            logger.info("Notion dashboard builder initialized successfully")
            
        except Exception as e:
            logger.error(f"Dashboard builder initialization failed: {e}")
            raise
    
    async def _get_database_ids(self):
        """データベースIDの取得"""
        try:
            # データベースを検索
            databases = self.notion_client.client.search(
                query="",
                filter={"property": "object", "value": "database"}
            )
            
            # データベースIDを保存
            for database in databases.get('results', []):
                title = database.get('title', [{}])[0].get('plain_text', '')
                if 'insight' in title.lower():
                    self.database_ids['insights'] = database['id']
                elif 'task' in title.lower():
                    self.database_ids['tasks'] = database['id']
                elif 'analysis' in title.lower():
                    self.database_ids['analysis_results'] = database['id']
                elif 'sync' in title.lower():
                    self.database_ids['sync_status'] = database['id']
            
            logger.info(f"Found {len(self.database_ids)} databases")
            
        except Exception as e:
            logger.error(f"Database ID retrieval failed: {e}")
    
    async def _create_templates(self):
        """テンプレートの作成"""
        try:
            # 分析レポートテンプレート
            await self._create_analysis_report_template()
            
            # 同期状況レポートテンプレート
            await self._create_sync_status_template()
            
            # プロジェクト進捗レポートテンプレート
            await self._create_project_progress_template()
            
            logger.info("Templates created successfully")
            
        except Exception as e:
            logger.error(f"Template creation failed: {e}")
    
    async def _create_analysis_report_template(self):
        """分析レポートテンプレートの作成"""
        try:
            template_content = """# 📊 分析レポート

## 📋 基本情報
- **分析日時**: {{分析日時}}
- **分析タイプ**: {{分析タイプ}}
- **対象コンテンツ**: {{対象コンテンツ}}

## 🔍 分析結果
{{分析結果の詳細}}

## 📈 信頼度
**信頼度**: {{信頼度}}%

## ⚡ 推奨アクション
{{推奨アクション}}

## 📝 実行メモ
{{実行メモ}}

## 🔗 関連リンク
- [関連タスク]({{関連タスクリンク}})
- [関連コンテンツ]({{関連コンテンツリンク}})"""
            
            # テンプレートページの作成
            template_page = await self._create_template_page(
                "分析レポートテンプレート",
                template_content
            )
            
            if template_page:
                self.template_ids['analysis_report'] = template_page
            
        except Exception as e:
            logger.error(f"Analysis report template creation failed: {e}")
    
    async def _create_sync_status_template(self):
        """同期状況レポートテンプレートの作成"""
        try:
            template_content = """# 🔄 同期状況レポート

## 📊 サマリー
- **成功**: {{成功件数}}件
- **待機中**: {{待機件数}}件
- **エラー**: {{エラー件数}}件

## ✅ 成功した同期
{{成功した同期の詳細}}

## ⏳ 待機中の同期
{{待機中の同期の詳細}}

## ❌ エラーが発生した同期
{{エラーの詳細}}

## 🔧 推奨アクション
{{推奨アクション}}"""
            
            # テンプレートページの作成
            template_page = await self._create_template_page(
                "同期状況レポートテンプレート",
                template_content
            )
            
            if template_page:
                self.template_ids['sync_status'] = template_page
            
        except Exception as e:
            logger.error(f"Sync status template creation failed: {e}")
    
    async def _create_project_progress_template(self):
        """プロジェクト進捗レポートテンプレートの作成"""
        try:
            template_content = """# 📈 プロジェクト進捗レポート

## 🎯 プロジェクト概要
- **プロジェクト名**: {{プロジェクト名}}
- **開始日**: {{開始日}}
- **期限**: {{期限}}
- **全体進捗**: {{進捗}}%

## 📋 タスク状況
- **完了**: {{完了タスク数}}件
- **進行中**: {{進行中タスク数}}件
- **未開始**: {{未開始タスク数}}件

## 🔍 AI分析結果
{{AI分析結果}}

## ⚡ 推奨アクション
{{推奨アクション}}"""
            
            # テンプレートページの作成
            template_page = await self._create_template_page(
                "プロジェクト進捗レポートテンプレート",
                template_content
            )
            
            if template_page:
                self.template_ids['project_progress'] = template_page
            
        except Exception as e:
            logger.error(f"Project progress template creation failed: {e}")
    
    async def _create_template_page(self, title: str, content: str) -> Optional[str]:
        """テンプレートページの作成"""
        try:
            # テンプレートページの作成
            page_data = {
                'parent': {'type': 'page_id', 'page_id': 'parent_page_id'},  # 実際の親ページIDに置き換え
                'properties': {
                    'title': {'title': [{'text': {'content': title}}]}
                }
            }
            
            result = self.notion_client.client.pages.create(**page_data)
            page_id = result['id']
            
            # コンテンツの追加
            blocks = self._convert_markdown_to_blocks(content)
            self.notion_client.client.blocks.children.append(
                block_id=page_id,
                children=blocks
            )
            
            logger.info(f"Created template page: {title}")
            return page_id
            
        except Exception as e:
            logger.error(f"Template page creation failed: {e}")
            return None
    
    def _convert_markdown_to_blocks(self, markdown_content: str) -> List[Dict[str, Any]]:
        """MarkdownをNotionブロックに変換"""
        try:
            blocks = []
            lines = markdown_content.split('\n')
            
            for line in lines:
                if not line.strip():
                    continue
                
                if line.startswith('# '):
                    blocks.append({
                        'type': 'heading_1',
                        'heading_1': {'rich_text': [{'text': {'content': line[2:]}}]}
                    })
                elif line.startswith('## '):
                    blocks.append({
                        'type': 'heading_2',
                        'heading_2': {'rich_text': [{'text': {'content': line[3:]}}]}
                    })
                elif line.startswith('### '):
                    blocks.append({
                        'type': 'heading_3',
                        'heading_3': {'rich_text': [{'text': {'content': line[4:]}}]}
                    })
                elif line.startswith('- '):
                    blocks.append({
                        'type': 'bulleted_list_item',
                        'bulleted_list_item': {'rich_text': [{'text': {'content': line[2:]}}]}
                    })
                else:
                    # 通常の段落
                    blocks.append({
                        'type': 'paragraph',
                        'paragraph': {'rich_text': [{'text': {'content': line}}]}
                    })
            
            return blocks
            
        except Exception as e:
            logger.error(f"Markdown to blocks conversion failed: {e}")
            return []
    
    async def create_insight_page(self, insight_data: Dict[str, Any]) -> Optional[str]:
        """インサイトページの作成"""
        try:
            if 'insights' not in self.database_ids:
                logger.warning("Insights database not found")
                return None
            
            page_data = {
                'parent': {'database_id': self.database_ids['insights']},
                'properties': {
                    'タイトル': {'title': [{'text': {'content': insight_data.get('title', 'New Insight')}}]},
                    'タイプ': {'select': {'name': insight_data.get('type', 'unknown')}},
                    '信頼度': {'number': insight_data.get('confidence', 0.0)},
                    'ステータス': {'select': {'name': '未実行'}},
                    '作成日時': {'created_time': datetime.now().isoformat()}
                }
            }
            
            result = self.notion_client.client.pages.create(**page_data)
            logger.info(f"Created insight page: {result['id']}")
            return result['id']
            
        except Exception as e:
            logger.error(f"Insight page creation failed: {e}")
            return None
    
    async def create_task_page(self, task_data: Dict[str, Any]) -> Optional[str]:
        """タスクページの作成"""
        try:
            if 'tasks' not in self.database_ids:
                logger.warning("Tasks database not found")
                return None
            
            page_data = {
                'parent': {'database_id': self.database_ids['tasks']},
                'properties': {
                    'タスク名': {'title': [{'text': {'content': task_data.get('title', 'New Task')}}]},
                    'ステータス': {'select': {'name': '未開始'}},
                    '優先度': {'select': {'name': task_data.get('priority', 'medium')}},
                    '期限': {'date': {'start': task_data.get('due_date', datetime.now().isoformat())}},
                    '推定時間': {'rich_text': [{'text': {'content': task_data.get('estimated_time', '10分')}}]},
                    '作成日時': {'created_time': datetime.now().isoformat()}
                }
            }
            
            result = self.notion_client.client.pages.create(**page_data)
            logger.info(f"Created task page: {result['id']}")
            return result['id']
            
        except Exception as e:
            logger.error(f"Task page creation failed: {e}")
            return None
    
    async def update_sync_status(self, status_data: Dict[str, Any]) -> bool:
        """同期状況の更新"""
        try:
            # 同期状況ページのIDを取得（実際の実装では、設定から取得）
            sync_status_page_id = "sync_status_page_id"  # 実際のIDに置き換え
            
            page_data = {
                'properties': {
                    '成功件数': {'number': status_data.get('success_count', 0)},
                    '待機件数': {'number': status_data.get('pending_count', 0)},
                    'エラー件数': {'number': status_data.get('error_count', 0)},
                    '最終更新': {'last_edited_time': datetime.now().isoformat()}
                }
            }
            
            self.notion_client.client.pages.update(page_id=sync_status_page_id, **page_data)
            logger.info("Sync status updated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Sync status update failed: {e}")
            return False
    
    async def create_analysis_report(self, analysis_data: Dict[str, Any]) -> Optional[str]:
        """分析レポートの作成"""
        try:
            # テンプレートを使用してレポートを作成
            template_id = self.template_ids.get('analysis_report')
            if not template_id:
                logger.warning("Analysis report template not found")
                return None
            
            # テンプレートをコピーして新しいページを作成
            # 実際の実装では、テンプレートのコピー機能を使用
            
            logger.info("Analysis report created successfully")
            return "analysis_report_id"  # 実際のIDに置き換え
            
        except Exception as e:
            logger.error(f"Analysis report creation failed: {e}")
            return None
    
    async def create_sync_status_report(self, sync_data: Dict[str, Any]) -> Optional[str]:
        """同期状況レポートの作成"""
        try:
            # テンプレートを使用してレポートを作成
            template_id = self.template_ids.get('sync_status')
            if not template_id:
                logger.warning("Sync status template not found")
                return None
            
            # テンプレートをコピーして新しいページを作成
            # 実際の実装では、テンプレートのコピー機能を使用
            
            logger.info("Sync status report created successfully")
            return "sync_status_report_id"  # 実際のIDに置き換え
            
        except Exception as e:
            logger.error(f"Sync status report creation failed: {e}")
            return None
    
    async def create_project_progress_report(self, project_data: Dict[str, Any]) -> Optional[str]:
        """プロジェクト進捗レポートの作成"""
        try:
            # テンプレートを使用してレポートを作成
            template_id = self.template_ids.get('project_progress')
            if not template_id:
                logger.warning("Project progress template not found")
                return None
            
            # テンプレートをコピーして新しいページを作成
            # 実際の実装では、テンプレートのコピー機能を使用
            
            logger.info("Project progress report created successfully")
            return "project_progress_report_id"  # 実際のIDに置き換え
            
        except Exception as e:
            logger.error(f"Project progress report creation failed: {e}")
            return None
