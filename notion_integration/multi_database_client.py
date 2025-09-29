"""
複数データベース対応のNotionクライアント拡張
"""

from notion_client import Client
from notion_client.helpers import collect_paginated_api
from typing import Dict, Any, List, Optional
from config import settings
import logging

logger = logging.getLogger(__name__)

class MultiDatabaseNotionClient:
    """複数データベースに対応したNotionクライアント"""
    
    def __init__(self, auth_token: str = None):
        self.client = Client(auth=auth_token or settings.NOTION_API_KEY)
        
        # データベース設定のマッピング
        self.database_configs = {
            'main': {
                'database_id': settings.NOTION_MAIN_DATABASE_ID,
                'data_source_id': settings.NOTION_MAIN_DATA_SOURCE_ID,
                'name': 'メインダッシュボード'
            },
            'analysis': {
                'database_id': settings.NOTION_ANALYSIS_DATABASE_ID,
                'data_source_id': settings.NOTION_ANALYSIS_DATA_SOURCE_ID,
                'name': '分析結果'
            },
            'recommendations': {
                'database_id': settings.NOTION_RECOMMENDATIONS_DATABASE_ID,
                'data_source_id': settings.NOTION_RECOMMENDATIONS_DATA_SOURCE_ID,
                'name': '推奨事項'
            },
            'sync_log': {
                'database_id': settings.NOTION_SYNC_LOG_DATABASE_ID,
                'data_source_id': settings.NOTION_SYNC_LOG_DATA_SOURCE_ID,
                'name': '同期ログ'
            }
        }
        
        logger.info("MultiDatabaseNotionClient initialized")
        self._log_database_status()
    
    def _log_database_status(self):
        """データベース設定の状況をログ出力"""
        for db_type, config in self.database_configs.items():
            db_id_status = "✅" if config['database_id'] else "❌"
            ds_id_status = "✅" if config['data_source_id'] else "❌"
            logger.info(f"{config['name']}: DB_ID {db_id_status}, DS_ID {ds_id_status}")
    
    def get_database_config(self, database_type: str) -> Dict[str, Any]:
        """データベースタイプの設定を取得"""
        if database_type not in self.database_configs:
            raise ValueError(f"Unknown database type: {database_type}")
        return self.database_configs[database_type]
    
    async def get_database_pages(self, database_type: str = 'main') -> List[Dict[str, Any]]:
        """指定されたデータベースタイプのページを取得"""
        config = self.get_database_config(database_type)
        db_id = config['database_id']
        
        if not db_id:
            logger.error(f"Database ID not set for {database_type}")
            return []
        
        try:
            pages = collect_paginated_api(self.client.databases.query, database_id=db_id)
            logger.info(f"Fetched {len(pages)} pages from {config['name']}")
            return pages
        except Exception as e:
            logger.error(f"Error fetching pages from {config['name']}: {e}")
            return []
    
    async def create_page(self, database_type: str, properties: Dict[str, Any], children: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """指定されたデータベースタイプにページを作成"""
        config = self.get_database_config(database_type)
        
        if not config['data_source_id']:
            logger.error(f"Data source ID not set for {database_type}")
            return {}
        
        try:
            parent = {"type": "data_source_id", "data_source_id": config['data_source_id']}
            new_page = self.client.pages.create(
                parent=parent,
                properties=properties,
                children=children
            )
            logger.info(f"Created new page in {config['name']}")
            return new_page
        except Exception as e:
            logger.error(f"Error creating page in {config['name']}: {e}")
            return {}
    
    async def create_main_dashboard_page(self, title: str, content: str, tags: List[str] = None) -> Dict[str, Any]:
        """メインダッシュボードにページを作成"""
        properties = {
            "Title": {"title": [{"type": "text", "text": {"content": title}}]},
            "Status": {"select": {"name": "Active"}},
            "Source": {"select": {"name": "Notion"}},
            "Content Type": {"select": {"name": "Note"}},
            "Word Count": {"number": len(content.split())}
        }
        
        if tags:
            properties["Tags"] = {"multi_select": [{"name": tag} for tag in tags]}
        
        children = [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": content}}]
                }
            }
        ]
        
        return await self.create_page('main', properties, children)
    
    async def create_analysis_result(self, analysis_type: str, source_content_id: str, score: float, summary: str) -> Dict[str, Any]:
        """分析結果ページを作成"""
        properties = {
            "Title": {"title": [{"type": "text", "text": {"content": f"{analysis_type} Analysis"}}]},
            "Analysis Type": {"select": {"name": analysis_type}},
            "Score": {"number": score},
            "Summary": {"rich_text": [{"type": "text", "text": {"content": summary}}]},
            "Status": {"select": {"name": "New"}}
        }
        
        children = [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": summary}}]
                }
            }
        ]
        
        return await self.create_page('analysis', properties, children)
    
    async def create_recommendation(self, rec_type: str, priority: str, description: str, target_content_id: str = None) -> Dict[str, Any]:
        """推奨事項ページを作成"""
        properties = {
            "Title": {"title": [{"type": "text", "text": {"content": f"{rec_type} Recommendation"}}]},
            "Type": {"select": {"name": rec_type}},
            "Priority": {"select": {"name": priority}},
            "Description": {"rich_text": [{"type": "text", "text": {"content": description}}]},
            "Status": {"select": {"name": "Pending"}}
        }
        
        children = [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": description}}]
                }
            }
        ]
        
        return await self.create_page('recommendations', properties, children)
    
    async def create_sync_log(self, sync_type: str, status: str, items_processed: int, errors: int = 0, details: str = "") -> Dict[str, Any]:
        """同期ログページを作成"""
        properties = {
            "Title": {"title": [{"type": "text", "text": {"content": f"{sync_type} Sync Log"}}]},
            "Sync Type": {"select": {"name": sync_type}},
            "Status": {"select": {"name": status}},
            "Items Processed": {"number": items_processed},
            "Errors": {"number": errors}
        }
        
        children = []
        if details:
            children.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": details}}]
                }
            })
        
        return await self.create_page('sync_log', properties, children)
    
    async def get_all_database_status(self) -> Dict[str, Any]:
        """すべてのデータベースの状況を取得"""
        status = {}
        
        for db_type, config in self.database_configs.items():
            try:
                pages = await self.get_database_pages(db_type)
                status[db_type] = {
                    'name': config['name'],
                    'database_id_set': bool(config['database_id']),
                    'data_source_id_set': bool(config['data_source_id']),
                    'page_count': len(pages),
                    'status': 'active' if config['database_id'] and config['data_source_id'] else 'inactive'
                }
            except Exception as e:
                status[db_type] = {
                    'name': config['name'],
                    'database_id_set': bool(config['database_id']),
                    'data_source_id_set': bool(config['data_source_id']),
                    'page_count': 0,
                    'status': 'error',
                    'error': str(e)
                }
        
        return status
