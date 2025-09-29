# GitHub Actions クイックスタートガイド

## 🚀 5分で始めるGitHub Actions連携

### 前提条件
- [x] GitHubリポジトリが準備済み
- [x] Obsidian Sync有料版を使用
- [x] Notion APIキーを取得済み

## 📋 セットアップ手順

### 1. リポジトリのクローン（1分）
```bash
git clone https://github.com/lazywhiz-main/notionxobsidian.git
cd notionxobsidian
```

### 2. ObsidianでVaultを開く（30秒）
1. Obsidianを起動
2. 「Open folder as vault」
3. クローンしたフォルダを選択

### 3. Obsidian Git プラグインの設定（2分）
1. **プラグインをインストール**
   - Settings → Community plugins → Browse
   - **"Obsidian Git"** を検索してインストール（`github-sync` ではない）
   - **作者**: Vincent

2. **自動同期を有効化**
   - Settings → Community plugins → Obsidian Git
   - "Auto pull" ✅
   - "Auto push" ✅
   - "Auto commit" ✅
   - 同期間隔: 5分

### 4. GitHub Secretsの設定（1分）
1. GitHubリポジトリのSettings → Secrets and variables → Actions
2. 以下のSecretsを追加：
   - `NOTION_API_KEY`: あなたのNotion APIキー
   - `NOTION_DATABASE_ID`: NotionデータベースID
   - `NOTION_DATA_SOURCE_ID`: NotionデータソースID

### 5. テスト実行（30秒）
1. `01_Content/test-sync.md` を作成
2. 簡単な内容を記述
3. 保存（自動的にGitHubにプッシュ）
4. GitHub Actionsが自動実行される

## ✅ 動作確認

### 正常に動作している場合
- [x] Obsidian Gitが自動的にコミット・プッシュ
- [x] GitHub Actionsが10分以内に実行
- [x] 分析結果が生成される
- [x] エラーログがない

### 問題がある場合
1. **Obsidian Gitが動作しない**
   - プラグインが有効化されているか確認
   - 設定を再確認

2. **GitHub Actionsが実行されない**
   - Secretsが正しく設定されているか確認
   - ワークフローファイルを確認

3. **エラーが発生する**
   - GitHub Actionsのログを確認
   - 設定を再確認

## 🔧 カスタマイズ

### 実行間隔の変更
`.github/workflows/notion-obsidian-sync.yml` を編集：
```yaml
schedule:
  - cron: '*/5 * * * *'  # 5分間隔
  # - cron: '*/10 * * * *'  # 10分間隔
  # - cron: '0 */1 * * *'   # 1時間間隔
```

### 分析対象の変更
`sync_system/github_actions_runner.py` を編集：
```python
# 特定のフォルダのみを分析
vault_path = Path('./obsidian-vault/01_Content')
```

## 📊 監視・メンテナンス

### 日常的な確認
1. **GitHub Actionsの実行状況**
   - https://github.com/lazywhiz-main/notionxobsidian/actions
   - 緑色のチェックマークが表示されているか

2. **分析結果の確認**
   - `analysis-results/` フォルダ
   - 最新の分析結果を確認

3. **エラーログの確認**
   - GitHub Actionsのログ
   - エラーがないか確認

### 月次のメンテナンス
1. **Secretsの更新**
   - Notion APIキーの更新
   - 期限切れの確認

2. **プラグインの更新**
   - Obsidian Gitプラグインの更新
   - その他のプラグインの更新

3. **ログのクリーンアップ**
   - 古い分析結果の削除
   - ログファイルの整理

## 🆘 サポート

### よくある質問
**Q: 同期が遅いのですが？**
A: 実行間隔を調整してください。10分間隔が推奨です。

**Q: 分析結果が表示されません**
A: GitHub Actionsのログを確認し、エラーがないかチェックしてください。

**Q: Obsidian Gitが動作しません**
A: プラグインが正しくインストールされ、有効化されているか確認してください。

### トラブルシューティング
詳細なトラブルシューティングは [Obsidian設定ガイド](obsidian-setup-guide.md) を参照してください。

## 🎉 完了！

これでGitHub Actions連携の設定が完了しました！

- ✅ Macを常時起動する必要がない
- ✅ 完全にクラウドベース
- ✅ 自動的な分析・同期
- ✅ バージョン管理機能

**次のステップ**: Notion側の設定に進んでください。
