# Obsidian保管庫パスの確認方法

## 🔍 Obsidian保管庫パスの確認方法

### 📋 方法1: Obsidianアプリ内で確認
1. Obsidianを開く
2. 設定（歯車アイコン）をクリック
3. **'About'** または **'一般'** を選択
4. **'Vault location'** または **'保管庫の場所'** を確認

### 📋 方法2: ファイルエクスプローラーで確認
1. Obsidianで任意のファイルを開く
2. ファイルを右クリック
3. **'Show in Finder'** または **'エクスプローラーで表示'** を選択
4. フォルダのパスを確認

### 📋 方法3: ターミナルで確認
1. Obsidianでファイルを開く
2. ファイルを右クリック
3. **'Copy path'** または **'パスをコピー'** を選択
4. ターミナルで `pwd` を実行

### 📋 方法4: 一般的な保管庫の場所
- **macOS**: `~/Documents/Obsidian/`
- **Windows**: `C:\Users\[ユーザー名]\Documents\Obsidian\`
- **Linux**: `~/Documents/Obsidian/`

## 🔍 一般的なObsidian保管庫の場所

### macOS
- `~/Documents/Obsidian/`
- `~/Obsidian/`
- `~/Desktop/Obsidian/`
- `~/Dropbox/Obsidian/`
- `~/OneDrive/Obsidian/`
- `~/Google Drive/Obsidian/`

### Windows
- `C:\Users\[ユーザー名]\Documents\Obsidian\`
- `C:\Users\[ユーザー名]\Obsidian\`
- `C:\Users\[ユーザー名]\Desktop\Obsidian\`

### Linux
- `~/Documents/Obsidian/`
- `~/Obsidian/`
- `~/Desktop/Obsidian/`

## 🔍 Obsidian設定ファイルの場所

### macOS
- `~/Library/Application Support/obsidian`
- `~/Library/Preferences/obsidian`

### Windows
- `%APPDATA%\Obsidian`
- `%LOCALAPPDATA%\Obsidian`

### Linux
- `~/.config/obsidian`
- `~/.local/share/obsidian`

## 📋 手動確認の手順

### 1️⃣ Obsidianアプリ内で確認
- Obsidianを開く
- 設定（歯車アイコン）をクリック
- **'About'** または **'一般'** を選択
- **'Vault location'** または **'保管庫の場所'** を確認

### 2️⃣ ファイルエクスプローラーで確認
- Obsidianで任意のファイルを開く
- ファイルを右クリック
- **'Show in Finder'** または **'エクスプローラーで表示'** を選択
- フォルダのパスを確認

### 3️⃣ 一般的な場所を確認
- `~/Documents/Obsidian/`
- `~/Obsidian/`
- `~/Desktop/Obsidian/`
- `~/Dropbox/Obsidian/`
- `~/OneDrive/Obsidian/`
- `~/Google Drive/Obsidian/`

## 🎯 次のステップ

### 保管庫のパスが分かったら:
1. そのパスをコピー
2. Git設定スクリプトを実行
3. パスを入力して設定を完了

### 現在のプロジェクトディレクトリを使用する場合:
- 現在のディレクトリ（`/Users/lazywhiz/notionxobsidian`）をObsidian保管庫として使用
- 既存のファイルをObsidianで管理
- Git設定を直接実行

## 💡 推奨アプローチ

1. **既存のObsidian保管庫**がある場合:
   - その保管庫のパスを確認
   - その保管庫でGit設定を実行

2. **新しいObsidian保管庫**を作成する場合:
   - 現在のプロジェクトディレクトリを使用
   - 既存のファイルをObsidianで管理
   - Git設定を直接実行
