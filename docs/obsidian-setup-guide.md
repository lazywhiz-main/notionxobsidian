# Obsidian設定ガイド（GitHub Actions対応版）

## 1. Obsidian Vault の準備

### 1.1 Vault の作成
1. Obsidianを起動
2. 「Open folder as vault」をクリック
3. **GitHubリポジトリをクローンしたフォルダを選択**
4. Vault名を設定: `Notion x Obsidian Integration`

### 1.2 既存のObsidian Sync保管庫を使用（推奨）
**Obsidian Sync有料版を使用している場合：**

1. **既存のObsidian保管庫を開く**
   - 通常通りObsidianを起動
   - 既存の同期済み保管庫を開く

2. **GitHubリポジトリをクローン**
   ```bash
   # 別の場所にGitHubリポジトリをクローン
   git clone https://github.com/lazywhiz-main/notionxobsidian.git
   cd notionxobsidian
   ```

3. **設定ファイルをコピー**
   - GitHubリポジトリの設定ファイルを既存の保管庫にコピー
   - `.github/workflows/` フォルダを既存の保管庫にコピー

### 1.3 Obsidian Sync有料版の設定（推奨）
**Obsidian Sync有料版を使用している場合、以下の利点があります：**

#### 💎 Obsidian Sync有料版の利点
- ✅ **リアルタイム同期**: 複数デバイス間で即座に同期
- ✅ **エンドツーエンド暗号化**: セキュリティが高い
- ✅ **バージョン履歴**: 過去のバージョンに戻れる
- ✅ **自動的な競合解決**: 重複を自動で回避
- ✅ **高速な同期処理**: バックグラウンドで処理

#### 🔧 推奨設定の変更
1. **ファイルシステム監視を有効化**（高速処理）
2. **Obsidian Syncをバックアップとして活用**（セキュリティ）
3. **ハイブリッド同期の実装**（最適化）
4. **競合解決機能の強化**（信頼性）

#### 📋 同期戦略
- 🚀 **プライマリ**: ファイルシステム監視（高速）
- ☁️ **セカンダリ**: Obsidian Sync（バックアップ・他デバイス）
- 🔄 **フォールバック**: 手動同期

### 1.4 フォルダ構造の作成
以下のフォルダ構造を作成：

```
Notion-Obsidian-Integration/
├── 00_Dashboard/           # メインダッシュボード
├── 01_Content/             # メインコンテンツ
├── 02_Analysis/            # 分析結果
│   ├── Results/            # 分析結果
│   ├── Insights/           # インサイト
│   └── Duplicates/         # 重複検出
├── 03_Recommendations/     # 推奨事項
├── 04_Sync/                # 同期関連
│   ├── Logs/               # 同期ログ
│   └── Conflicts/          # 競合解決
├── 05_Templates/           # テンプレート
└── 06_Archive/             # アーカイブ
```

### 1.5 環境変数の設定
`.env` ファイルに以下を設定：

```env
# Obsidian設定
OBSIDIAN_VAULT_PATH="/path/to/your/obsidian/vault"

# 例（macOS）:
# OBSIDIAN_VAULT_PATH="/Users/username/Documents/Obsidian/Notion-Obsidian-Integration"

# 例（Windows）:
# OBSIDIAN_VAULT_PATH="C:\\Users\\username\\Documents\\Obsidian\\Notion-Obsidian-Integration"

# 例（Linux）:
# OBSIDIAN_VAULT_PATH="/home/username/Documents/Obsidian/Notion-Obsidian-Integration"
```

## 2. GitHub Actions連携の設定

### 2.1 Obsidian Git プラグインのインストール
**GitHub Actionsと連携するために必須のプラグインです：**

1. **Yet Another Obsidian Synchronizer** プラグインをインストール
   - Settings → Community plugins → Browse
   - **"Yet Another Obsidian Synchronizer"** を検索してインストール
   - プラグインを有効化
   - **作者**: Mahyar Mirrashed
   - **機能**: "Use Git to synchronize your vault contents across devices"
   - **ダウンロード数**: 12,538

2. **自動同期の設定**
   - Settings → Community plugins → Yet Another Obsidian Synchronizer
   - "Auto pull" を有効化
   - "Auto push" を有効化
   - "Auto commit" を有効化
   - 同期間隔を設定（推奨：5分）

### 2.2 GitHubリポジトリの設定
1. **リモートリポジトリの確認**
   ```bash
   git remote -v
   # origin  https://github.com/lazywhiz-main/notionxobsidian.git (fetch)
   # origin  https://github.com/lazywhiz-main/notionxobsidian.git (push)
   ```

2. **ブランチの設定**
   ```bash
   git checkout -b main
   git push -u origin main
   ```

3. **自動コミットの設定**
   - Obsidian Git プラグインの設定で自動コミットを有効化
   - コミットメッセージのテンプレートを設定

### 2.3 同期フローの確認
**GitHub Actionsとの連携フロー：**

```
📱 iPhoneでメモ作成
    ↓
☁️ Obsidian Syncでクラウド同期
    ↓
💻 MacでObsidian Gitが自動プッシュ
    ↓
🐙 GitHubリポジトリに変更が反映
    ↓
⚙️ GitHub Actionsが自動実行（10分間隔）
    ↓
🔍 分析エンジンが実行
    ↓
📊 結果がNotionに同期
```

## 3. メインダッシュボードの作成

### 3.1 メインダッシュボードファイル
`00_Dashboard/00_Main_Dashboard.md` を作成：

```markdown
---
title: "Notion x Obsidian Integration Dashboard"
type: dashboard
created: 2024-01-01
modified: 2024-01-01
tags: [dashboard, integration, main]
status: active
---

# Notion x Obsidian Integration Dashboard

## 📊 システムステータス

### 同期状況
- **最終同期**: {{last_sync_time}}
- **同期ステータス**: {{sync_status}}
- **処理済みアイテム**: {{processed_items}}
- **エラー数**: {{error_count}}

### 統計情報
- **総コンテンツ数**: {{total_content}}
- **Notionコンテンツ**: {{notion_content}}
- **Obsidianコンテンツ**: {{obsidian_content}}
- **分析実行回数**: {{analysis_count}}

## 🔍 最近の分析結果

### 最新のインサイト
- [[02_Analysis/Insights/{{latest_insight}}]]

### 重複検出
- [[02_Analysis/Duplicates/{{duplicate_detection}}]]

### 類似度分析
- [[02_Analysis/Results/{{similarity_analysis}}]]

## 💡 推奨事項

### 優先度: 高
- [[03_Recommendations/{{high_priority_rec}}]]

### 優先度: 中
- [[03_Recommendations/{{medium_priority_rec}}]]

## 📝 最近更新されたノート

- [[01_Content/{{recent_note_1}}]]
- [[01_Content/{{recent_note_2}}]]
- [[01_Content/{{recent_note_3}}]]

## 🔗 クイックリンク

- [[02_Analysis/Results/]] - 分析結果
- [[02_Analysis/Insights/]] - インサイト
- [[03_Recommendations/]] - 推奨事項
- [[04_Sync/Logs/]] - 同期ログ
- [[05_Templates/]] - テンプレート

## 📈 パフォーマンス

### 分析実行時間
- **平均実行時間**: {{avg_analysis_time}}秒
- **最長実行時間**: {{max_analysis_time}}秒
- **最短実行時間**: {{min_analysis_time}}秒

### 同期パフォーマンス
- **平均同期時間**: {{avg_sync_time}}秒
- **成功率**: {{sync_success_rate}}%
```

## 4. プラグインのインストール

### 4.1 必須プラグイン
1. **Obsidian Git** - GitHub連携（必須）
2. **Templater** - テンプレート機能
3. **Dataview** - データベース機能
4. **Calendar** - カレンダー表示
5. **Daily Notes** - 日次ノート
6. **File Explorer** - ファイル管理

### 4.2 推奨プラグイン
1. **Advanced Tables** - 表の編集
2. **Kanban** - カンバンボード
3. **Mind Map** - マインドマップ
4. **Sliding Panes** - パネル表示
5. **Style Settings** - スタイル設定

## 5. テンプレートの作成

### 5.1 コンテンツテンプレート
`05_Templates/Content_Template.md` を作成：

```markdown
---
title: "{{title}}"
type: content
created: {{date}}
modified: {{date}}
tags: [{{tags}}]
status: active
source: {{source}}
priority: {{priority}}
word_count: {{word_count}}
---

# {{title}}

## 概要
{{summary}}

## 詳細
{{content}}

## 関連リンク
- [[{{related_note_1}}]]
- [[{{related_note_2}}]]

## メタデータ
- **作成日**: {{created_date}}
- **更新日**: {{modified_date}}
- **ソース**: {{source}}
- **優先度**: {{priority}}
- **単語数**: {{word_count}}
```

### 3.2 分析結果テンプレート
`05_Templates/Analysis_Result_Template.md` を作成：

```markdown
---
title: "Analysis Result: {{content_title}}"
type: analysis_result
analysis_type: {{analysis_type}}
created: {{date}}
modified: {{date}}
tags: [analysis, {{analysis_type}}]
status: {{status}}
score: {{score}}
---

# Analysis Result: {{content_title}}

## 分析情報
- **分析タイプ**: {{analysis_type}}
- **分析日時**: {{analysis_date}}
- **スコア**: {{score}}
- **ステータス**: {{status}}

## 分析結果

### キーワード
{{keywords}}

### 要約
{{summary}}

### 詳細分析
{{detailed_analysis}}

## 推奨事項
{{recommendations}}

## 関連コンテンツ
- [[{{source_content}}]]
- [[{{related_content_1}}]]
- [[{{related_content_2}}]]

## メタデータ
- **分析ID**: {{analysis_id}}
- **実行時間**: {{execution_time}}秒
- **信頼度**: {{confidence}}%
```

### 3.3 推奨事項テンプレート
`05_Templates/Recommendation_Template.md` を作成：

```markdown
---
title: "Recommendation: {{recommendation_type}}"
type: recommendation
recommendation_type: {{recommendation_type}}
priority: {{priority}}
created: {{date}}
modified: {{date}}
tags: [recommendation, {{recommendation_type}}]
status: {{status}}
target_content: {{target_content}}
---

# Recommendation: {{recommendation_type}}

## 推奨情報
- **タイプ**: {{recommendation_type}}
- **優先度**: {{priority}}
- **ステータス**: {{status}}
- **対象コンテンツ**: [[{{target_content}}]]

## 推奨内容
{{recommendation_description}}

## 必要なアクション
{{required_actions}}

## 実行手順
1. {{step_1}}
2. {{step_2}}
3. {{step_3}}

## 期待される効果
{{expected_effects}}

## 関連情報
- **作成日**: {{created_date}}
- **期限**: {{due_date}}
- **担当者**: {{assignee}}
- **進捗**: {{progress}}%

## メタデータ
- **推奨ID**: {{recommendation_id}}
- **信頼度**: {{confidence}}%
- **実行可能性**: {{feasibility}}%
```

## 4. プラグインの設定

### 4.1 推奨プラグイン
以下のプラグインをインストール：

1. **Templater**
   - テンプレート機能の強化
   - 動的なコンテンツ生成

2. **Dataview**
   - データベース的な表示
   - 動的なクエリ

3. **Advanced Tables**
   - テーブル機能の強化

4. **Tag Wrangler**
   - タグ管理の強化

5. **File Explorer**
   - ファイル管理の強化

### 4.2 Templater設定
1. Templaterプラグインを有効化
2. 設定でテンプレートフォルダを `05_Templates/` に設定
3. テンプレート変数を設定

### 4.3 Dataview設定
1. Dataviewプラグインを有効化
2. 以下のクエリをメインダッシュボードに追加：

```dataview
TABLE 
  title as "タイトル",
  status as "ステータス",
  priority as "優先度",
  modified as "更新日"
FROM "01_Content"
WHERE status = "active"
SORT modified DESC
LIMIT 10
```

## 5. 自動化の設定

### 5.1 ホットキーの設定
以下のホットキーを設定：

- `Ctrl+Shift+N`: 新しいコンテンツノート
- `Ctrl+Shift+A`: 分析結果ノート
- `Ctrl+Shift+R`: 推奨事項ノート
- `Ctrl+Shift+D`: ダッシュボード更新

### 5.2 自動テンプレート適用
1. Templaterの設定で自動テンプレート適用を有効化
2. フォルダごとにデフォルトテンプレートを設定

## 6. 同期設定

### 6.1 ファイル監視の設定
1. システムがObsidianファイルの変更を監視できるように設定
2. リアルタイム同期のための設定

### 6.2 競合解決の設定
1. 競合が発生した場合の処理方法を設定
2. バックアップの設定

## 7. テストと検証

### 7.1 接続テスト
```bash
# 環境変数の確認
python -c "from config.settings import settings; print('Obsidian Vault Path:', settings.OBSIDIAN_VAULT_PATH)"

# ファイル監視テスト
python -c "
from obsidian_integration.file_monitor import ObsidianFileMonitor
monitor = ObsidianFileMonitor()
print('File monitor initialized successfully')
"
```

### 7.2 ファイル操作テスト
```bash
# ファイル作成テスト
python -c "
from obsidian_integration.markdown_parser import ObsidianMarkdownParser
parser = ObsidianMarkdownParser()
print('Markdown parser initialized successfully')
"
```

## 8. トラブルシューティング

### 8.1 よくある問題
1. **パスエラー**: 絶対パスが正しく設定されているか確認
2. **権限エラー**: ファイルの読み書き権限を確認
3. **エンコーディングエラー**: UTF-8エンコーディングを確認
4. **ファイルロック**: Obsidianがファイルをロックしていないか確認

### 8.2 ログの確認
```bash
# アプリケーションログの確認
tail -f logs/app.log

# ファイル監視ログの確認
tail -f logs/file_monitor.log
```

## 9. セキュリティとバックアップ

### 9.1 バックアップ設定
1. Obsidianの自動バックアップを有効化
2. 外部バックアップサービスとの連携
3. 定期的なバックアップの実行

### 9.2 セキュリティ設定
1. 機密情報のマスキング
2. アクセス権限の設定
3. 監査ログの有効化

## 10. Obsidian Sync有料版での高度な機能

### 10.1 マルチデバイス対応
**Obsidian Sync有料版を使用している場合、以下の高度な機能が利用可能です：**

#### 📱 デバイス別の役割分担
- **デスクトップ**: メイン編集環境（詳細な編集・分析）
- **モバイル**: 外出先での閲覧・軽編集
- **タブレット**: 図表作成・詳細編集
- **同期**: 全デバイス間でリアルタイム同期

#### 🔄 高度な同期の流れ
1. **デスクトップで編集**
2. **ファイルシステム監視が変更を検出**
3. **即座にNotionに同期**
4. **Obsidian Syncがバックグラウンドで同期**
5. **他のデバイスで変更が反映**

### 10.2 高度な監視機能
- **リアルタイムファイル変更検出**
- **マルチデバイス同期状況監視**
- **競合解決の自動化**
- **バージョン履歴の活用**

### 10.3 分析機能の強化
- **クロスデバイスでの分析結果同期**
- **リアルタイム重複検出**
- **マルチデバイスでの推奨事項共有**
- **同期統計の可視化**

### 10.4 自動化機能
- **スケジュール同期**
- **条件付き同期**
- **自動バックアップ**
- **競合解決の自動化**

### 10.5 セキュリティ機能
- **エンドツーエンド暗号化**
- **アクセスログの記録**
- **不正アクセスの検出**
- **データ整合性の確認**

## 11. GitHub Actions設定の確認

### 11.1 ワークフローの確認
1. **GitHubリポジトリのActionsタブを確認**
   - https://github.com/lazywhiz-main/notionxobsidian/actions
   - ワークフローが正常に実行されているか確認

2. **Secretsの設定確認**
   - Settings → Secrets and variables → Actions
   - 以下のSecretsが設定されているか確認：
     - `NOTION_API_KEY`
     - `NOTION_DATABASE_ID`
     - `NOTION_DATA_SOURCE_ID`

### 11.2 同期のテスト
1. **テストファイルの作成**
   - `01_Content/test-sync.md` を作成
   - 簡単な内容を記述

2. **自動同期の確認**
   - Obsidian Gitが自動的にコミット・プッシュ
   - GitHub Actionsが自動実行
   - 分析結果が生成される

3. **ログの確認**
   - GitHub Actionsの実行ログを確認
   - エラーがないかチェック

## 12. トラブルシューティング

### 12.1 よくある問題
1. **Obsidian Gitが動作しない**
   - プラグインが有効化されているか確認
   - 設定が正しいか確認
   - ログを確認

2. **GitHub Actionsが実行されない**
   - Secretsが正しく設定されているか確認
   - ワークフローファイルが正しいか確認
   - リポジトリの権限を確認

3. **同期が遅い**
   - 実行間隔を調整（10分間隔推奨）
   - ファイルサイズを確認
   - ネットワーク接続を確認

### 12.2 ログの確認方法
```bash
# ローカルでのログ確認
git log --oneline

# GitHub Actionsのログ確認
# リポジトリのActionsタブで確認
```

## 13. 次のステップ

Obsidian側の設定が完了したら：
1. Notion側の設定に進む
2. GitHub Actionsの初期実行
3. 分析機能のテスト
4. ダッシュボードのカスタマイズ
5. **Obsidian Sync有料版での高度な機能の活用**
6. **GitHub Actionsでの自動化の活用**
4. 自動化の調整
