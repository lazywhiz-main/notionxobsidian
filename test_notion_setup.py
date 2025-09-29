#!/usr/bin/env python3
"""
Notion API 2025-09-03 対応の設定テストスクリプト
"""

import asyncio
import os
from config.settings import settings
from notion_integration.notion_client import NotionClient

async def test_notion_setup():
    """Notion設定のテスト"""
    print("🔧 Notion API 2025-09-03 設定テスト")
    print("=" * 50)
    
    # 1. 環境変数の確認
    print("\n1️⃣ 環境変数の確認")
    print(f"   NOTION_API_KEY: {'✅ SET' if settings.NOTION_API_KEY else '❌ NOT SET'}")
    print(f"   NOTION_DATABASE_ID: {'✅ SET' if settings.NOTION_DATABASE_ID else '❌ NOT SET'}")
    print(f"   NOTION_DATA_SOURCE_ID: {'✅ SET' if settings.NOTION_DATA_SOURCE_ID else '❌ NOT SET'}")
    
    if not settings.NOTION_API_KEY:
        print("\n❌ NOTION_API_KEYが設定されていません。")
        print("   .envファイルにNOTION_API_KEYを設定してください。")
        return False
    
    if not settings.NOTION_DATABASE_ID:
        print("\n❌ NOTION_DATABASE_IDが設定されていません。")
        print("   .envファイルにNOTION_DATABASE_IDを設定してください。")
        return False
    
    # 2. Notionクライアントの初期化テスト
    print("\n2️⃣ Notionクライアントの初期化")
    try:
        client = NotionClient()
        print("   ✅ Notionクライアントが正常に初期化されました")
    except Exception as e:
        print(f"   ❌ Notionクライアントの初期化に失敗: {e}")
        return False
    
    # 3. データベース情報の取得テスト
    print("\n3️⃣ データベース情報の取得")
    try:
        database_info = await client.get_database_info()
        if database_info:
            print("   ✅ データベース情報の取得に成功")
            print(f"   📊 データベースタイトル: {database_info.get('title', [{}])[0].get('plain_text', 'N/A')}")
        else:
            print("   ❌ データベース情報の取得に失敗")
            return False
    except Exception as e:
        print(f"   ❌ データベース情報の取得に失敗: {e}")
        return False
    
    # 4. データソースの取得テスト
    print("\n4️⃣ データソースの取得")
    try:
        data_sources = await client.get_data_sources()
        if data_sources:
            print(f"   ✅ {len(data_sources)}個のデータソースを発見")
            for i, ds in enumerate(data_sources):
                print(f"   📋 データソース {i+1}: {ds.get('name', 'N/A')} (ID: {ds.get('id', 'N/A')[:8]}...)")
            
            # データソースIDが設定されていない場合の推奨
            if not settings.NOTION_DATA_SOURCE_ID and data_sources:
                print(f"\n💡 推奨: .envファイルに以下を追加してください:")
                print(f"   NOTION_DATA_SOURCE_ID=\"{data_sources[0]['id']}\"")
        else:
            print("   ❌ データソースの取得に失敗")
            return False
    except Exception as e:
        print(f"   ❌ データソースの取得に失敗: {e}")
        return False
    
    # 5. ページの取得テスト
    print("\n5️⃣ ページの取得テスト")
    try:
        pages = await client.get_database_pages()
        print(f"   ✅ {len(pages)}個のページを取得")
        if pages:
            print("   📄 最初のページ:")
            first_page = pages[0]
            title = first_page.get('properties', {}).get('Title', {}).get('title', [{}])[0].get('plain_text', 'N/A')
            print(f"      - タイトル: {title}")
            print(f"      - ID: {first_page.get('id', 'N/A')[:8]}...")
    except Exception as e:
        print(f"   ❌ ページの取得に失敗: {e}")
        return False
    
    # 6. 総合結果
    print("\n" + "=" * 50)
    print("🎉 Notion設定テスト完了!")
    print("\n📋 次のステップ:")
    print("1. 必要に応じてNOTION_DATA_SOURCE_IDを.envファイルに設定")
    print("2. Obsidian側の設定に進む")
    print("3. 初期同期の実行")
    
    return True

async def main():
    """メイン関数"""
    success = await test_notion_setup()
    if not success:
        print("\n❌ テストが失敗しました。設定を確認してください。")
        exit(1)
    else:
        print("\n✅ すべてのテストが成功しました！")

if __name__ == "__main__":
    asyncio.run(main())
