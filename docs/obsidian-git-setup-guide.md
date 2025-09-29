# Obsidian保管庫でのGit設定ガイド

## 🎯 保管庫パス確認完了

**保管庫パス**: `/Users/lazywhiz/Documents/LAZYWHIZ/Notion-Obsidian-Integration`

## ⚠️ アクセス権限の問題

現在、ターミナルから保管庫にアクセスできない状況です。これはmacOSのセキュリティ設定が原因の可能性があります。

## 🔧 解決方法

### 方法1: Finderからターミナルを開く
1. **Finder**で保管庫フォルダを開く
2. フォルダを右クリック
3. **"サービス"** → **"ターミナルで開く"** を選択
4. または、フォルダを**ターミナルアイコンにドラッグ**

### 方法2: ターミナルでアクセス権限を確認
```bash
# アクセス権限を確認
ls -la "/Users/lazywhiz/Documents/LAZYWHIZ/Notion-Obsidian-Integration"

# 権限を変更（必要に応じて）
chmod 755 "/Users/lazywhiz/Documents/LAZYWHIZ/Notion-Obsidian-Integration"
```

### 方法3: Obsidianから直接操作
1. **Obsidian**で保管庫を開く
2. **設定** → **コミュニティプラグイン** → **Obsidian Git**
3. プラグインの設定でGit設定を確認

## 🔧 Git設定手順

### 1️⃣ Gitリポジトリを初期化
```bash
cd "/Users/lazywhiz/Documents/LAZYWHIZ/Notion-Obsidian-Integration"
git init
```

### 2️⃣ .gitignoreファイルを作成
```bash
cat > .gitignore << 'EOF'
# Obsidian
.obsidian/
.DS_Store
Thumbs.db

# Python
__pycache__/
*.py[cod]
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# Environment variables
.env
.env.local
.env.production

# Logs
logs/
*.log

# Analysis results
analysis-results/
EOF
```

### 3️⃣ リモートリポジトリを追加
```bash
git remote add origin https://github.com/lazywhiz-main/notionxobsidian.git
git branch -M main
```

### 4️⃣ 初回コミットとプッシュ
```bash
git add .
git commit -m "Initial commit: Obsidian vault with GitHub Actions"
git push -u origin main
```

## 🔑 GitHub Personal Access Token

### トークン生成手順
1. **GitHub.com** にログイン
2. 右上の**プロフィール画像**をクリック
3. **Settings** を選択
4. 左サイドバー: **Developer settings**
5. **Personal access tokens** → **Tokens (classic)**
6. **Generate new token (classic)**

### トークンの設定
- **Note**: `Obsidian Git Integration`
- **Expiration**: 90 days (推奨)
- **Scopes**: 以下を選択
  - ✅ `repo` (Full control of private repositories)
  - ✅ `workflow` (Update GitHub Action workflows)
  - ✅ `write:packages` (Write packages)

## ⚙️ Obsidian Gitプラグインの設定

### 自動同期設定
- **Auto Pull**: 有効化
- **Auto Push**: 有効化
- **Auto Commit**: 有効化
- **同期間隔**: 5分
- **コミットメッセージ**: `Auto sync: {{date}}`

### 設定手順
1. **Obsidian**で保管庫を開く
2. **設定** → **コミュニティプラグイン** → **Obsidian Git**
3. 設定ボタン（歯車アイコン）をクリック
4. 自動同期設定を有効化

## 🎯 次のステップ

1. **アクセス権限の問題を解決**
2. **Gitリポジトリを初期化**
3. **リモートリポジトリを追加**
4. **初回コミットとプッシュを実行**
5. **プラグインの動作確認**

## 🔧 トラブルシューティング

### アクセス権限エラー
- Finderからターミナルを開く
- 権限を確認・変更
- Obsidianから直接操作

### 認証エラー
- Personal Access Tokenを確認
- トークンの権限を確認
- リポジトリのアクセス権限を確認

### 同期エラー
- リモートリポジトリのURLを確認
- ブランチ名を確認
- 競合を解決
