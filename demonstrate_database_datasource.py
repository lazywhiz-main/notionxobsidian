#!/usr/bin/env python3
"""
データベースIDとデータソースIDの違いを確認するスクリプト
"""

import asyncio
from config.settings import settings
from notion_integration.notion_client import NotionClient

async def demonstrate_database_vs_datasource():
    """データベースIDとデータソースIDの違いを実演"""
    print("🔍 データベースID vs データソースID の違い")
    print("=" * 60)
    
    if not settings.NOTION_API_KEY:
        print("❌ NOTION_API_KEYが設定されていません")
        print("   .envファイルにAPIキーを設定してください")
        return
    
    client = NotionClient()
    
    # データベースIDが設定されている場合のテスト
    if settings.NOTION_DATABASE_ID:
        print(f"\n📊 データベースID: {settings.NOTION_DATABASE_ID}")
        
        try:
            # 1. データベース情報を取得（database_idを使用）
            print("\n1️⃣ データベース情報の取得（database_id使用）")
            database_info = await client.get_database_info()
            
            if database_info:
                print("   ✅ データベース情報取得成功")
                print(f"   📋 タイトル: {database_info.get('title', [{}])[0].get('plain_text', 'N/A')}")
                print(f"   🆔 データベースID: {database_info.get('id', 'N/A')}")
                
                # 2. データソース情報を取得
                print("\n2️⃣ データソース情報の取得")
                data_sources = await client.get_data_sources()
                
                if data_sources:
                    print(f"   ✅ {len(data_sources)}個のデータソースを発見")
                    for i, ds in enumerate(data_sources):
                        print(f"   📋 データソース {i+1}:")
                        print(f"      - 名前: {ds.get('name', 'N/A')}")
                        print(f"      - ID: {ds.get('id', 'N/A')}")
                        print(f"      - データベースID: {settings.NOTION_DATABASE_ID}")
                        print(f"      - データソースID: {ds.get('id', 'N/A')}")
                        print(f"      - 違い: データベースID ≠ データソースID")
                else:
                    print("   ❌ データソースが見つかりません")
            else:
                print("   ❌ データベース情報の取得に失敗")
                
        except Exception as e:
            print(f"   ❌ エラー: {e}")
    else:
        print("\n❌ NOTION_DATABASE_IDが設定されていません")
        print("   .envファイルにデータベースIDを設定してください")
    
    # 3. 概念の説明
    print("\n" + "=" * 60)
    print("📚 概念の説明")
    print("=" * 60)
    
    print("\n🔑 データベースID (Database ID):")
    print("   - データベース全体を識別するID")
    print("   - データベースの情報取得に使用")
    print("   - 検索や管理操作に使用")
    print("   - 例: 6c4240a9-a3ce-413e-9fd0-8a51a4d0a49b")
    
    print("\n🔑 データソースID (Data Source ID):")
    print("   - データベース内の特定のデータソースを識別")
    print("   - ページ作成時に必要")
    print("   - データ操作時に使用")
    print("   - 例: a42a62ed-9b51-4b98-9dea-ea6d091bc508")
    
    print("\n💡 重要なポイント:")
    print("   1. データベースID ≠ データソースID")
    print("   2. 1つのデータベースに複数のデータソースが存在可能")
    print("   3. ページ作成時は data_source_id が必要")
    print("   4. データベース情報取得時は database_id が必要")
    
    print("\n📋 設定例:")
    print("   # データベースID（データベース全体を識別）")
    print("   NOTION_DATABASE_ID=\"6c4240a9-a3ce-413e-9fd0-8a51a4d0a49b\"")
    print("   ")
    print("   # データソースID（ページ作成時に必要）")
    print("   NOTION_DATA_SOURCE_ID=\"a42a62ed-9b51-4b98-9dea-ea6d091bc508\"")

async def main():
    """メイン関数"""
    await demonstrate_database_vs_datasource()
    
    print("\n" + "=" * 60)
    print("✅ 説明完了!")
    print("\n📋 次のステップ:")
    print("1. データベースIDを.envファイルに設定")
    print("2. データソースIDを取得して.envファイルに設定")
    print("3. 両方のIDを使ってテスト")

if __name__ == "__main__":
    asyncio.run(main())
