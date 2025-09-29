#!/usr/bin/env python3
"""
複数データベースのデータソースID管理スクリプト
"""

import asyncio
import os
from config.settings import settings
from notion_integration.notion_client import NotionClient

async def discover_all_data_sources():
    """すべてのデータベースのデータソースIDを発見"""
    print("🔍 複数データベースのデータソースID発見")
    print("=" * 60)
    
    # 設定されたデータベースIDのリスト
    database_ids = [
        settings.NOTION_DATABASE_ID,  # メインダッシュボード
        # 他のデータベースIDをここに追加
        # "your_analysis_results_database_id",
        # "your_recommendations_database_id",
        # "your_sync_log_database_id",
    ]
    
    client = NotionClient()
    all_data_sources = {}
    
    for db_id in database_ids:
        if not db_id or db_id == "your_main_dashboard_database_id_here":
            continue
            
        print(f"\n📊 データベース: {db_id[:8]}...")
        try:
            # データベース情報を取得
            database_info = await client.get_database_info(db_id)
            if database_info:
                title = database_info.get('title', [{}])[0].get('plain_text', 'N/A')
                print(f"   📋 タイトル: {title}")
                
                # データソースを取得
                data_sources = await client.get_data_sources(db_id)
                if data_sources:
                    print(f"   🔗 データソース数: {len(data_sources)}")
                    for i, ds in enumerate(data_sources):
                        print(f"      {i+1}. {ds.get('name', 'N/A')} (ID: {ds.get('id', 'N/A')})")
                        all_data_sources[db_id] = {
                            'title': title,
                            'data_sources': data_sources
                        }
                else:
                    print("   ❌ データソースが見つかりません")
            else:
                print("   ❌ データベース情報の取得に失敗")
        except Exception as e:
            print(f"   ❌ エラー: {e}")
    
    return all_data_sources

async def generate_env_config(data_sources_info):
    """環境変数設定を生成"""
    print("\n" + "=" * 60)
    print("📝 .envファイル設定の推奨")
    print("=" * 60)
    
    print("\n# Notion API設定（2025-09-03 API対応）")
    print(f"NOTION_API_KEY=\"{settings.NOTION_API_KEY}\"")
    
    if data_sources_info:
        print("\n# データベースID設定")
        for db_id, info in data_sources_info.items():
            title = info['title']
            print(f"# {title}")
            print(f"NOTION_{title.upper().replace(' ', '_').replace('-', '_')}_DATABASE_ID=\"{db_id}\"")
            
            # 最初のデータソースIDを推奨
            if info['data_sources']:
                first_ds = info['data_sources'][0]
                print(f"NOTION_{title.upper().replace(' ', '_').replace('-', '_')}_DATA_SOURCE_ID=\"{first_ds['id']}\"")
    
    print("\n# Obsidian設定")
    print("OBSIDIAN_VAULT_PATH=\"/path/to/your/obsidian/vault\"")
    
    print("\n# AIサービス設定（オプション）")
    print("OPENAI_API_KEY=\"your_openai_api_key_here\"")
    print("ANTHROPIC_API_KEY=\"your_anthropic_api_key_here\"")

async def test_multiple_databases():
    """複数データベースのテスト"""
    print("\n" + "=" * 60)
    print("🧪 複数データベースのテスト")
    print("=" * 60)
    
    client = NotionClient()
    
    # 設定ファイルを更新して複数データベースに対応
    print("\n💡 推奨アプローチ:")
    print("1. 各データベースごとに専用のクライアントメソッドを作成")
    print("2. データベースタイプごとに異なる処理を実装")
    print("3. 設定ファイルでデータベースIDを管理")
    
    print("\n📋 実装例:")
    print("""
# config/settings.py に追加
class Settings:
    # メインダッシュボード
    NOTION_MAIN_DATABASE_ID: str = os.getenv("NOTION_MAIN_DATABASE_ID", "")
    NOTION_MAIN_DATA_SOURCE_ID: str = os.getenv("NOTION_MAIN_DATA_SOURCE_ID", "")
    
    # 分析結果データベース
    NOTION_ANALYSIS_DATABASE_ID: str = os.getenv("NOTION_ANALYSIS_DATABASE_ID", "")
    NOTION_ANALYSIS_DATA_SOURCE_ID: str = os.getenv("NOTION_ANALYSIS_DATA_SOURCE_ID", "")
    
    # 推奨事項データベース
    NOTION_RECOMMENDATIONS_DATABASE_ID: str = os.getenv("NOTION_RECOMMENDATIONS_DATABASE_ID", "")
    NOTION_RECOMMENDATIONS_DATA_SOURCE_ID: str = os.getenv("NOTION_RECOMMENDATIONS_DATA_SOURCE_ID", "")
    """)

async def main():
    """メイン関数"""
    print("🚀 Notion API 2025-09-03 複数データベース対応")
    
    # 1. データソースの発見
    data_sources_info = await discover_all_data_sources()
    
    # 2. 環境変数設定の生成
    await generate_env_config(data_sources_info)
    
    # 3. 複数データベースのテスト
    await test_multiple_databases()
    
    print("\n" + "=" * 60)
    print("✅ 複数データベース対応完了!")
    print("\n📋 次のステップ:")
    print("1. 上記の設定を.envファイルに追加")
    print("2. 各データベースごとの処理を実装")
    print("3. データベース間の関連付けを設定")

if __name__ == "__main__":
    asyncio.run(main())
