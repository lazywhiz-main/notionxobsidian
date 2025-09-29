# Notion設定ガイド

## 1. Notion API の設定

### 1.1 Integration の作成
1. [Notion Developers](https://www.notion.so/my-integrations) にアクセス
2. 「New integration」をクリック
3. 以下の情報を入力：
   - **Name**: `Notion x Obsidian Integration`
   - **Logo**: 任意（推奨：NotionとObsidianのアイコンを組み合わせたもの）
   - **Associated workspace**: 使用するワークスペースを選択

### 1.2 API Key の取得
1. 作成したIntegrationのページで「Internal Integration Token」をコピー
2. このトークンを `.env` ファイルの `NOTION_API_KEY` に設定

### 1.3 データベースの作成

#### メインダッシュボードデータベース
以下のプロパティを持つデータベースを作成：

**データベース名**: `Notion x Obsidian Dashboard`

**プロパティ**:
- `Title` (Title) - 必須
- `Status` (Select) - オプション: Active, Inactive, Archived
- `Source` (Select) - オプション: Notion, Obsidian, Both
- `Last Sync` (Date) - 最終同期日時
- `Tags` (Multi-select) - タグ
- `Priority` (Select) - オプション: High, Medium, Low
- `Content Type` (Select) - オプション: Note, Task, Project, Reference
- `Word Count` (Number) - 単語数
- `Created` (Created time) - 作成日時
- `Modified` (Last edited time) - 最終更新日時

#### 分析結果データベース
**データベース名**: `AI Analysis Results`

**プロパティ**:
- `Title` (Title) - 必須
- `Analysis Type` (Select) - オプション: Content Analysis, Similarity, Duplicate Detection, Sentiment
- `Source Content` (Relation) - メインダッシュボードデータベースとの関連
- `Score` (Number) - 分析スコア
- `Keywords` (Multi-select) - 抽出されたキーワード
- `Summary` (Rich text) - 分析結果の要約
- `Recommendations` (Rich text) - 推奨事項
- `Generated At` (Date) - 分析実行日時
- `Status` (Select) - オプション: New, Reviewed, Applied, Dismissed

#### 推奨事項データベース
**データベース名**: `Recommendations`

**プロパティ**:
- `Title` (Title) - 必須
- `Type` (Select) - オプション: Merge Content, Link Content, Update Tags, Archive Content
- `Priority` (Select) - オプション: High, Medium, Low
- `Target Content` (Relation) - 対象コンテンツ
- `Description` (Rich text) - 推奨事項の詳細
- `Action Required` (Rich text) - 必要なアクション
- `Status` (Select) - オプション: Pending, In Progress, Completed, Rejected
- `Created At` (Date) - 作成日時
- `Due Date` (Date) - 期限（任意）

#### 同期ログデータベース
**データベース名**: `Sync Log`

**プロパティ**:
- `Title` (Title) - 必須
- `Sync Type` (Select) - オプション: Notion to Obsidian, Obsidian to Notion, Analysis Update
- `Status` (Select) - オプション: Success, Failed, Partial
- `Items Processed` (Number) - 処理されたアイテム数
- `Errors` (Number) - エラー数
- `Duration` (Number) - 実行時間（秒）
- `Details` (Rich text) - 詳細ログ
- `Timestamp` (Date) - 実行日時

### 1.4 データベースの共有
1. 各データベースのページで「Share」をクリック
2. 作成したIntegrationを追加
3. 「Can edit」権限を付与

### 1.5 データベースID とデータソースID の取得

#### ⚠️ 重要: Notion API 2025-09-03 の変更
Notion APIの新しいバージョンでは、**データソース（Data Source）**の概念が導入されました。データベースが複数のデータソースを持つことができるようになり、ページ作成時には`data_source_id`が必要です。

#### 🔑 データベースID vs データソースID の違い

**データベースID (Database ID)**:
- **役割**: データベース全体を識別
- **用途**: データベースの情報取得、検索、管理
- **取得方法**: データベースのURLから取得
- **例**: `6c4240a9-a3ce-413e-9fd0-8a51a4d0a49b`

**データソースID (Data Source ID)**:
- **役割**: データベース内の特定のデータソースを識別
- **用途**: ページ作成、データ操作
- **取得方法**: データベース設定メニューから取得
- **例**: `a42a62ed-9b51-4b98-9dea-ea6d091bc508`

#### 📊 関係性
```
データベース (Database ID)
├── データソース1 (Data Source ID 1)
│   ├── ページ1
│   └── ページ2
└── データソース2 (Data Source ID 2)
    ├── ページ3
    └── ページ4
```

#### データベースID の取得
1. データベースのURLからIDを取得
   - URL例: `https://www.notion.so/workspace/DATABASE_ID?v=...`
   - `DATABASE_ID` の部分をコピー
2. `.env` ファイルの `NOTION_DATABASE_ID` に設定

#### データソースID の取得（新規）
1. データベースの設定メニューを開く
2. 「Manage data sources」セクションを探す
3. 「Copy data source ID」ボタンをクリック
4. `.env` ファイルの `NOTION_DATA_SOURCE_ID` に設定

**重要**: データベースID ≠ データソースID です。両方とも必要です！

## 2. 環境変数の設定

`.env` ファイルに以下を設定：

```env
# Notion設定
NOTION_API_KEY="your_notion_integration_token_here"
NOTION_DATABASE_ID="your_main_dashboard_database_id_here"
NOTION_DATA_SOURCE_ID="your_data_source_id_here"  # 新規: 2025-09-03 API対応

# その他の設定
OBSIDIAN_VAULT_PATH="/path/to/your/obsidian/vault"
OPENAI_API_KEY="your_openai_api_key_here"  # オプション
ANTHROPIC_API_KEY="your_anthropic_api_key_here"  # オプション
```

## 3. 初期データの準備

### 3.1 サンプルコンテンツの作成
メインダッシュボードデータベースに以下のようなサンプルエントリを作成：

1. **テスト用ノート**
   - Title: "AI and Machine Learning Overview"
   - Content: "This is a comprehensive overview of artificial intelligence and machine learning technologies..."
   - Tags: AI, ML, Technology
   - Status: Active

2. **プロジェクトノート**
   - Title: "Project Planning Template"
   - Content: "A template for project planning and management..."
   - Tags: Project, Template, Management
   - Status: Active

3. **リファレンスノート**
   - Title: "Useful Resources and Links"
   - Content: "A collection of useful resources and links..."
   - Tags: Reference, Resources, Links
   - Status: Active

## 4. ダッシュボードの構築

### 4.1 メインダッシュボードページ
1. 新しいページを作成: `Notion x Obsidian Integration Dashboard`
2. 以下のセクションを追加：
   - **システムステータス**: 同期状況、エラー状況
   - **最近の分析結果**: 最新の分析結果を表示
   - **推奨事項**: 優先度の高い推奨事項
   - **同期ログ**: 最近の同期履歴
   - **統計情報**: コンテンツ数、分析回数など

### 4.2 ビューの設定
各データベースに以下のビューを作成：

**メインダッシュボード**:
- All Items (デフォルト)
- By Status (Status でグループ化)
- By Source (Source でグループ化)
- Recent (Modified でソート)

**分析結果**:
- All Results (デフォルト)
- By Type (Analysis Type でグループ化)
- High Score (Score でソート)
- Recent (Generated At でソート)

**推奨事項**:
- All Recommendations (デフォルト)
- By Priority (Priority でグループ化)
- Pending (Status でフィルタ)
- Due Soon (Due Date でソート)

## 5. 自動化の設定

### 5.1 テンプレートの作成
各データベースにテンプレートを作成：

**メインダッシュボードテンプレート**:
- デフォルトのプロパティ値を設定
- 基本的な構造を定義

**分析結果テンプレート**:
- 分析タイプ別のテンプレート
- 標準的な分析項目を定義

**推奨事項テンプレート**:
- 推奨タイプ別のテンプレート
- アクション項目を定義

## 6. 権限とセキュリティ

### 6.1 アクセス権限
- Integrationには必要最小限の権限のみ付与
- データベースの編集権限のみ設定
- ワークスペース全体へのアクセスは避ける

### 6.2 API制限
- Notion APIのレート制限に注意
- 大量のデータ処理時は適切な間隔を設定
- エラーハンドリングを実装

## 7. テストと検証

### 7.1 接続テスト
```bash
# 環境変数の確認
python -c "from config.settings import settings; print('Notion API Key:', 'SET' if settings.NOTION_API_KEY else 'NOT SET'); print('Data Source ID:', 'SET' if settings.NOTION_DATA_SOURCE_ID else 'NOT SET')"

# データベース接続テスト
python -c "from notion_integration.notion_client import NotionClient; client = NotionClient(); print('Connection successful')"
```

### 7.2 データ取得テスト
```bash
# データベースページの取得テスト
python -c "
from notion_integration.notion_client import NotionClient
client = NotionClient()
pages = client.get_database_pages()
print(f'Found {len(pages)} pages')
"
```

## 8. トラブルシューティング

### 8.1 よくある問題
1. **API Key エラー**: トークンが正しく設定されているか確認
2. **データベースID エラー**: データベースIDが正しいか確認
3. **データソースID エラー**: データソースIDが正しく設定されているか確認（2025-09-03 API対応）
4. **権限エラー**: Integrationに適切な権限が付与されているか確認
5. **レート制限**: API呼び出し頻度を調整
6. **API バージョンエラー**: Notion-Versionヘッダーが2025-09-03に設定されているか確認

### 8.2 ログの確認
```bash
# アプリケーションログの確認
tail -f logs/app.log

# エラーログの確認
tail -f logs/error.log
```

## 9. 次のステップ

Notion側の設定が完了したら：
1. Obsidian側の設定に進む
2. 初期同期の実行
3. 分析機能のテスト
4. ダッシュボードのカスタマイズ
