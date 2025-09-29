#!/usr/bin/env python3
"""
Obsidian保管庫でのGit手動設定スクリプト
"""

import os
import subprocess
import shutil
from pathlib import Path

def setup_obsidian_git():
    """Obsidian保管庫でGitを設定"""
    print("🔧 Obsidian保管庫でのGit手動設定")
    print("=" * 60)
    
    # 保管庫のパスを確認
    vault_path = input("既存のObsidian保管庫のパスを入力してください: ").strip()
    
    if not vault_path or not os.path.exists(vault_path):
        print("❌ 有効な保管庫パスを入力してください")
        return False
    
    print(f"📁 保管庫パス: {vault_path}")
    
    # Gitを初期化
    if not init_git_repo(vault_path):
        return False
    
    # リモートリポジトリを追加
    if not add_remote_repo(vault_path):
        return False
    
    # 初回コミットとプッシュ
    if not initial_commit_and_push(vault_path):
        return False
    
    print("\n✅ Git設定が完了しました！")
    return True

def init_git_repo(vault_path):
    """Gitリポジトリを初期化"""
    print("\n🔧 Gitリポジトリを初期化中...")
    
    try:
        # Gitを初期化
        subprocess.run(["git", "init"], cwd=vault_path, check=True)
        print("✅ Gitリポジトリを初期化")
        
        # .gitignoreを作成
        gitignore_content = """# Obsidian
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
"""
        
        gitignore_path = Path(vault_path) / ".gitignore"
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        print("✅ .gitignoreファイルを作成")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git初期化エラー: {e}")
        return False
    
    return True

def add_remote_repo(vault_path):
    """リモートリポジトリを追加"""
    print("\n🔗 リモートリポジトリを追加中...")
    
    try:
        # リモートリポジトリを追加
        subprocess.run(["git", "remote", "add", "origin", "https://github.com/lazywhiz-main/notionxobsidian.git"], cwd=vault_path, check=True)
        print("✅ リモートリポジトリを追加")
        
        # メインブランチを設定
        subprocess.run(["git", "branch", "-M", "main"], cwd=vault_path, check=True)
        print("✅ メインブランチを設定")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ リモートリポジトリ追加エラー: {e}")
        return False
    
    return True

def initial_commit_and_push(vault_path):
    """初回コミットとプッシュを実行"""
    print("\n📝 初回コミットとプッシュを実行中...")
    
    try:
        # 変更をステージング
        subprocess.run(["git", "add", "."], cwd=vault_path, check=True)
        print("✅ 変更をステージング")
        
        # 初回コミット
        subprocess.run(["git", "commit", "-m", "Initial commit: Obsidian vault with GitHub Actions"], cwd=vault_path, check=True)
        print("✅ 初回コミットを実行")
        
        # プッシュ
        subprocess.run(["git", "push", "-u", "origin", "main"], cwd=vault_path, check=True)
        print("✅ 初回プッシュを実行")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ コミット/プッシュエラー: {e}")
        print("💡 認証情報の入力が必要な場合があります")
        return False
    
    return True

def explain_next_steps():
    """次のステップの説明"""
    print("\n" + "=" * 60)
    print("🎯 次のステップ")
    print("=" * 60)
    
    print("\n1️⃣ プラグインの設定:")
    print("   - Obsidian Gitプラグインの設定を開く")
    print("   - 自動同期を有効化")
    print("   - 同期間隔を設定")
    
    print("\n2️⃣ 動作確認:")
    print("   - ファイルを変更して自動同期をテスト")
    print("   - GitHub Actionsの動作を確認")
    print("   - エラーがないか確認")
    
    print("\n3️⃣ GitHub Actions設定:")
    print("   - GitHub Secretsを設定")
    print("   - ワークフローの動作を確認")
    print("   - 分析結果の同期を確認")

def main():
    """メイン関数"""
    print("🚀 Obsidian保管庫でのGit手動設定")
    print("=" * 60)
    print("このスクリプトは既存のObsidian保管庫にGit設定を追加します")
    print("GitHub Actionsとの連携を可能にします")
    print()
    
    success = setup_obsidian_git()
    
    if success:
        explain_next_steps()
        print("\n🎉 設定完了！")
    else:
        print("\n❌ 設定に失敗しました")
        print("エラーメッセージを確認してください")

if __name__ == "__main__":
    main()
