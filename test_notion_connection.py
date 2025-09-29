#!/usr/bin/env python3
"""
Notion API接続テスト
Database ID と Data Source ID の確認
"""
import os
import asyncio
from config.settings import settings
from notion_integration.notion_client import NotionClient

async def test_notion_connection():
    """Notion API接続をテスト"""
    print("🔍 Notion API接続テスト")
    print("=" * 50)
    
    # 設定の確認
    print("\n📋 現在の設定:")
    print(f"NOTION_API_KEY: {'設定済み' if settings.NOTION_API_KEY else '❌ 未設定'}")
    print(f"NOTION_DATABASE_ID: {'設定済み' if settings.NOTION_DATABASE_ID else '❌ 未設定'}")
    print(f"NOTION_DATA_SOURCE_ID: {'設定済み' if settings.NOTION_DATA_SOURCE_ID else '❌ 未設定'}")
    
    if not settings.NOTION_API_KEY:
        print("\n❌ NOTION_API_KEYが設定されていません")
        print("   .envファイルにAPIキーを設定してください")
        return False
    
    if not settings.NOTION_DATABASE_ID:
        print("\n❌ NOTION_DATABASE_IDが設定されていません")
        print("   .envファイルにデータベースIDを設定してください")
        return False
    
    if not settings.NOTION_DATA_SOURCE_ID:
        print("\n❌ NOTION_DATA_SOURCE_IDが設定されていません")
        print("   .envファイルにデータソースIDを設定してください")
        return False
    
    # Notionクライアントの初期化
    try:
        client = NotionClient()
        print("\n✅ Notionクライアントの初期化成功")
    except Exception as e:
        print(f"\n❌ Notionクライアントの初期化失敗: {e}")
        return False
    
    # データベース情報の取得
    try:
        print("\n🔍 データベース情報を取得中...")
        database_info = await client.get_database_info(settings.NOTION_DATABASE_ID)
        
        if database_info:
            print("✅ データベース情報の取得成功")
            print(f"   データベース名: {database_info.get('title', [{}])[0].get('plain_text', 'N/A')}")
            print(f"   データベースID: {settings.NOTION_DATABASE_ID}")
            print(f"   作成日時: {database_info.get('created_time', 'N/A')}")
            print(f"   最終更新: {database_info.get('last_edited_time', 'N/A')}")
        else:
            print("❌ データベース情報の取得失敗")
            return False
            
    except Exception as e:
        print(f"❌ データベース情報の取得エラー: {e}")
        return False
    
    # データソース情報の取得
    try:
        print("\n🔍 データソース情報を取得中...")
        data_sources = await client.get_data_sources(settings.NOTION_DATABASE_ID)
        
        if data_sources:
            print("✅ データソース情報の取得成功")
            print(f"   データソース数: {len(data_sources)}")
            for i, ds in enumerate(data_sources):
                print(f"   データソース {i+1}: {ds.get('id', 'N/A')}")
        else:
            print("⚠️ データソース情報が見つかりません")
            print("   これは正常な場合もあります（APIバージョンによる）")
            
    except Exception as e:
        print(f"⚠️ データソース情報の取得エラー: {e}")
        print("   これは正常な場合もあります（APIバージョンによる）")
    
    # ページの取得テスト
    try:
        print("\n🔍 データベースページの取得テスト...")
        pages = await client.get_database_pages(settings.NOTION_DATABASE_ID)
        
        if pages is not None:
            print(f"✅ ページ取得成功: {len(pages)}件のページ")
            if pages:
                print("   最初のページ:")
                first_page = pages[0]
                print(f"   - ページID: {first_page.get('id', 'N/A')}")
                print(f"   - 作成日時: {first_page.get('created_time', 'N/A')}")
                print(f"   - 最終更新: {first_page.get('last_edited_time', 'N/A')}")
        else:
            print("❌ ページ取得失敗")
            return False
            
    except Exception as e:
        print(f"❌ ページ取得エラー: {e}")
        return False
    
    # ページ作成テスト（オプション）
    try:
        print("\n🔍 ページ作成テスト...")
        test_properties = {
            "Name": {
                "title": [{"type": "text", "text": {"content": "API接続テスト"}}]
            }
        }
        
        # テストページを作成
        new_page = await client.create_page(
            parent_id=settings.NOTION_DATABASE_ID,
            properties=test_properties
        )
        
        if new_page and new_page.get('id'):
            print("✅ ページ作成成功")
            print(f"   作成されたページID: {new_page['id']}")
            
            # テストページを削除（オプション）
            # await client.delete_page(new_page['id'])
            # print("   テストページを削除しました")
        else:
            print("❌ ページ作成失敗")
            return False
            
    except Exception as e:
        print(f"❌ ページ作成エラー: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Notion API接続テスト完了！")
    print("✅ すべてのテストが成功しました")
    return True

async def main():
    """メイン関数"""
    success = await test_notion_connection()
    
    if success:
        print("\n📋 次のステップ:")
        print("1. GitHub Secretsに設定を追加")
        print("2. Obsidianプラグインの設定")
        print("3. GitHub Actionsのテスト実行")
    else:
        print("\n❌ 設定を確認してください")
        print("1. .envファイルの設定を確認")
        print("2. Notion APIキーの有効性を確認")
        print("3. データベースIDの正確性を確認")

if __name__ == "__main__":
    asyncio.run(main())
