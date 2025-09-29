#!/usr/bin/env python3
"""
複数データベース設定のテストスクリプト
"""

import asyncio
from config.settings import settings
from notion_integration.multi_database_client import MultiDatabaseNotionClient

async def test_multiple_databases():
    """複数データベースの設定テスト"""
    print("🔧 複数データベース設定テスト")
    print("=" * 60)
    
    # 1. 設定の確認
    print("\n1️⃣ データベース設定の確認")
    database_types = ['main', 'analysis', 'recommendations', 'sync_log']
    
    for db_type in database_types:
        db_id_attr = f"NOTION_{db_type.upper()}_DATABASE_ID"
        ds_id_attr = f"NOTION_{db_type.upper()}_DATA_SOURCE_ID"
        
        db_id = getattr(settings, db_id_attr, "")
        ds_id = getattr(settings, ds_id_attr, "")
        
        print(f"   {db_type.upper()}:")
        print(f"     データベースID: {'✅ SET' if db_id else '❌ NOT SET'}")
        print(f"     データソースID: {'✅ SET' if ds_id else '❌ NOT SET'}")
    
    # 2. クライアントの初期化
    print("\n2️⃣ マルチデータベースクライアントの初期化")
    try:
        client = MultiDatabaseNotionClient()
        print("   ✅ クライアントが正常に初期化されました")
    except Exception as e:
        print(f"   ❌ クライアントの初期化に失敗: {e}")
        return False
    
    # 3. 各データベースの状況確認
    print("\n3️⃣ 各データベースの状況確認")
    try:
        status = await client.get_all_database_status()
        
        for db_type, info in status.items():
            print(f"   📊 {info['name']}:")
            print(f"     ステータス: {info['status']}")
            print(f"     ページ数: {info['page_count']}")
            if info['status'] == 'error':
                print(f"     エラー: {info.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"   ❌ データベース状況の確認に失敗: {e}")
        return False
    
    # 4. 設定の推奨事項
    print("\n4️⃣ 設定の推奨事項")
    print("   📋 必要な設定:")
    print("   1. 各データベースのIDを.envファイルに設定")
    print("   2. 各データソースのIDを.envファイルに設定")
    print("   3. データベース間の関連付けを設定")
    
    print("\n   💡 設定例:")
    print("   # メインダッシュボード")
    print("   NOTION_MAIN_DATABASE_ID=\"your_main_db_id\"")
    print("   NOTION_MAIN_DATA_SOURCE_ID=\"your_main_ds_id\"")
    print("   ")
    print("   # 分析結果")
    print("   NOTION_ANALYSIS_DATABASE_ID=\"your_analysis_db_id\"")
    print("   NOTION_ANALYSIS_DATA_SOURCE_ID=\"your_analysis_ds_id\"")
    
    return True

async def main():
    """メイン関数"""
    success = await test_multiple_databases()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ 複数データベース設定テスト完了!")
        print("\n📋 次のステップ:")
        print("1. 不足している設定を.envファイルに追加")
        print("2. 各データベースのデータソースIDを取得")
        print("3. 実際のデータベース操作をテスト")
    else:
        print("❌ テストが失敗しました。設定を確認してください。")
        exit(1)

if __name__ == "__main__":
    asyncio.run(main())
