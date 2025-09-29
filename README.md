# Notion x Obsidian Integration

NotionとObsidianを連携し、AI分析機能を提供するシステムです。

## 機能

- 🔄 自動同期（GitHub Actions）
- 🔍 重複検出
- 📊 分析・推奨事項生成
- 📱 マルチデバイス対応
- ☁️ クラウドベース

## セットアップ

### 1. 環境変数の設定

GitHubリポジトリのSecretsに以下を設定：

- `NOTION_API_KEY`: Notion APIキー
- `NOTION_DATABASE_ID`: NotionデータベースID
- `NOTION_DATA_SOURCE_ID`: NotionデータソースID

### 2. Obsidianの設定

1. Obsidian Git プラグインをインストール
2. このリポジトリをクローン
3. 自動同期を有効化

### 3. GitHub Actionsの設定

ワークフローは自動的に実行されます：
- 10分間隔でのスケジュール実行
- ファイル変更時の自動実行
- 手動実行

## 使用方法

1. Obsidianでメモを作成・編集
2. 自動的にGitHubに同期
3. GitHub Actionsが分析を実行
4. 結果がNotionに同期

## フォルダ構造

```
obsidian-vault/
├── 00_Dashboard/     # メインダッシュボード
├── 01_Content/       # メインコンテンツ
├── 02_Analysis/      # 分析結果
├── 03_Recommendations/ # 推奨事項
├── 04_Sync/          # 同期関連
├── 05_Templates/     # テンプレート
└── 06_Archive/       # アーカイブ
```

## ライセンス

MIT License
