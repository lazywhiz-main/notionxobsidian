import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Notion API設定
    NOTION_API_KEY: str = os.getenv("NOTION_API_KEY", "")
    
    # メインダッシュボードデータベース
    NOTION_MAIN_DATABASE_ID: str = os.getenv("NOTION_MAIN_DATABASE_ID", "")
    NOTION_MAIN_DATA_SOURCE_ID: str = os.getenv("NOTION_MAIN_DATA_SOURCE_ID", "")
    
    # 分析結果データベース
    NOTION_ANALYSIS_DATABASE_ID: str = os.getenv("NOTION_ANALYSIS_DATABASE_ID", "")
    NOTION_ANALYSIS_DATA_SOURCE_ID: str = os.getenv("NOTION_ANALYSIS_DATA_SOURCE_ID", "")
    
    # 推奨事項データベース
    NOTION_RECOMMENDATIONS_DATABASE_ID: str = os.getenv("NOTION_RECOMMENDATIONS_DATABASE_ID", "")
    NOTION_RECOMMENDATIONS_DATA_SOURCE_ID: str = os.getenv("NOTION_RECOMMENDATIONS_DATA_SOURCE_ID", "")
    
    # 同期ログデータベース
    NOTION_SYNC_LOG_DATABASE_ID: str = os.getenv("NOTION_SYNC_LOG_DATABASE_ID", "")
    NOTION_SYNC_LOG_DATA_SOURCE_ID: str = os.getenv("NOTION_SYNC_LOG_DATA_SOURCE_ID", "")
    
    # 後方互換性のため（既存コード用）
    NOTION_DATABASE_ID: str = os.getenv("NOTION_DATABASE_ID", "") or os.getenv("NOTION_MAIN_DATABASE_ID", "")
    NOTION_DATA_SOURCE_ID: str = os.getenv("NOTION_DATA_SOURCE_ID", "") or os.getenv("NOTION_MAIN_DATA_SOURCE_ID", "")
    
    # Obsidian設定
    OBSIDIAN_VAULT_PATH: str = os.getenv("OBSIDIAN_VAULT_PATH", "")
    
    # AIサービス設定
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")

settings = Settings()