from notion_client import Client
from notion_client.helpers import collect_paginated_api
from typing import Dict, Any, List
from config import settings
import logging

logger = logging.getLogger(__name__)

class NotionClient:
    def __init__(self, auth_token: str = None):
        self.client = Client(auth=auth_token or settings.NOTION_API_KEY)
        # Notion API keyの存在確認
        if not settings.NOTION_API_KEY:
            logger.warning("Notion API key is not set. Please set NOTION_API_KEY in your .env file.")
        else:
            logger.info("Notion client initialized successfully")
        
        # データソースIDの確認
        if not settings.NOTION_DATA_SOURCE_ID:
            logger.warning("Notion Data Source ID is not set. Please set NOTION_DATA_SOURCE_ID in your .env file.")

    async def get_database_info(self, database_id: str = None) -> Dict[str, Any]:
        """Gets database information including data sources (2025-09-03 API)."""
        db_id = database_id or settings.NOTION_DATABASE_ID
        if not db_id:
            logger.error("Notion database ID is not set.")
            return {}
        try:
            database_info = self.client.databases.retrieve(database_id=db_id)
            logger.info(f"Retrieved database info for {db_id}")
            return database_info
        except Exception as e:
            logger.error(f"Error retrieving database info for {db_id}: {e}")
            return {}

    async def get_data_sources(self, database_id: str = None) -> List[Dict[str, Any]]:
        """Gets data sources for a database (2025-09-03 API)."""
        db_id = database_id or settings.NOTION_DATABASE_ID
        if not db_id:
            logger.error("Notion database ID is not set.")
            return []
        try:
            database_info = await self.get_database_info(db_id)
            data_sources = database_info.get("data_sources", [])
            logger.info(f"Found {len(data_sources)} data sources for database {db_id}")
            return data_sources
        except Exception as e:
            logger.error(f"Error retrieving data sources for {db_id}: {e}")
            return []

    async def get_database_pages(self, database_id: str = None) -> List[Dict[str, Any]]:
        """Fetches all pages from a specified Notion database."""
        db_id = database_id or settings.NOTION_DATABASE_ID
        if not db_id:
            logger.error("Notion database ID is not set.")
            return []
        try:
            # Using collect_paginated_api to handle pagination
            pages = collect_paginated_api(self.client.databases.query, database_id=db_id)
            logger.info(f"Fetched {len(pages)} pages from database {db_id}.")
            return pages
        except Exception as e:
            logger.error(f"Error fetching database pages from {db_id}: {e}")
            return []

    async def get_page_content(self, page_id: str) -> List[Dict[str, Any]]:
        """Fetches all blocks (content) for a given Notion page."""
        try:
            blocks = collect_paginated_api(self.client.blocks.children.list, block_id=page_id)
            logger.info(f"Fetched {len(blocks)} blocks for page {page_id}.")
            return blocks
        except Exception as e:
            logger.error(f"Error fetching page content for {page_id}: {e}")
            return []

    async def update_page_properties(self, page_id: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        """Updates properties of a Notion page."""
        try:
            updated_page = self.client.pages.update(page_id=page_id, properties=properties)
            logger.info(f"Updated properties for page {page_id}.")
            return updated_page
        except Exception as e:
            logger.error(f"Error updating page properties for {page_id}: {e}")
            return {}

    async def append_block_children(self, block_id: str, children: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Appends new blocks as children to an existing block (e.g., a page)."""
        try:
            response = self.client.blocks.children.append(block_id=block_id, children=children)
            logger.info(f"Appended {len(children)} blocks to {block_id}.")
            return response
        except Exception as e:
            logger.error(f"Error appending blocks to {block_id}: {e}")
            return {}

    async def create_page(self, parent_id: str, properties: Dict[str, Any], children: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Creates a new page in Notion using data source ID (2025-09-03 API)."""
        try:
            # 2025-09-03 API対応: data_source_idを使用
            if settings.NOTION_DATA_SOURCE_ID:
                parent = {"type": "data_source_id", "data_source_id": settings.NOTION_DATA_SOURCE_ID}
            else:
                # フォールバック: 従来のdatabase_idを使用
                parent = {"type": "database_id", "database_id": parent_id}
                logger.warning("Using fallback database_id instead of data_source_id")
            
            new_page = self.client.pages.create(
                parent=parent,
                properties=properties,
                children=children
            )
            logger.info(f"Created new page: {properties.get('title', {}).get('title', [{'plain_text': 'Untitled'}])[0].get('plain_text', 'Untitled')}")
            return new_page
        except Exception as e:
            logger.error(f"Error creating page in database {parent_id}: {e}")
            return {}