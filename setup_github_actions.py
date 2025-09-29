#!/usr/bin/env python3
"""
GitHub Actions設定の自動化スクリプト
既存のリポジトリにGitHub Actionsを設定
"""

import os
import shutil
from pathlib import Path

def create_github_actions_workflow():
    """GitHub Actionsワークフローファイルを作成"""
    print("🔧 GitHub Actionsワークフローファイルを作成中...")
    
    # .github/workflowsディレクトリを作成
    workflows_dir = Path(".github/workflows")
    workflows_dir.mkdir(parents=True, exist_ok=True)
    
    # ワークフローファイルの内容
    workflow_content = """name: Notion-Obsidian Sync

on:
  # スケジュール実行（10分間隔）
  schedule:
    - cron: '*/10 * * * *'
  
  # ファイル変更時の実行
  push:
    branches: [ main ]
    paths: [ 'obsidian-vault/**/*.md' ]
  
  # 手動実行
  workflow_dispatch:

jobs:
  sync-and-analyze:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run analysis
      env:
        NOTION_API_KEY: ${{ secrets.NOTION_API_KEY }}
        NOTION_DATABASE_ID: ${{ secrets.NOTION_DATABASE_ID }}
        NOTION_DATA_SOURCE_ID: ${{ secrets.NOTION_DATA_SOURCE_ID }}
        OBSIDIAN_VAULT_PATH: ./obsidian-vault
      run: |
        python -m sync_system.github_actions_runner
    
    - name: Commit results
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add .
        git commit -m "Update analysis results" || exit 0
        git push
"""
    
    # ワークフローファイルを保存
    workflow_file = workflows_dir / "notion-obsidian-sync.yml"
    with open(workflow_file, 'w', encoding='utf-8') as f:
        f.write(workflow_content)
    
    print(f"✅ ワークフローファイルを作成: {workflow_file}")

def create_github_actions_runner():
    """GitHub Actions用のランナーを作成"""
    print("🔧 GitHub Actionsランナーを作成中...")
    
    # sync_systemディレクトリにgithub_actions_runner.pyを作成
    runner_content = '''"""
GitHub Actions用のランナー
Obsidianファイルの分析とNotion同期を実行
"""
import asyncio
import os
import sys
import logging
from pathlib import Path
from datetime import datetime

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from analysis_engine.enhanced_analysis_engine import EnhancedAnalysisEngine
from notion_integration.notion_client import NotionClient
from obsidian_integration.markdown_parser import ObsidianMarkdownParser
from sync_system.basic_dashboard_service import BasicDashboardService
from config import settings

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GitHubActionsRunner:
    """GitHub Actions用のランナークラス"""
    
    def __init__(self):
        self.analysis_engine = EnhancedAnalysisEngine()
        self.notion_client = NotionClient()
        self.markdown_parser = ObsidianMarkdownParser()
        self.dashboard_service = BasicDashboardService()
        
        # Obsidian保管庫のパス
        self.vault_path = os.getenv('OBSIDIAN_VAULT_PATH', './obsidian-vault')
        
        logger.info("GitHub Actions Runner initialized")
    
    async def run_analysis(self):
        """分析を実行"""
        try:
            logger.info("Starting analysis...")
            
            # 1. Obsidianファイルをスキャン
            obsidian_files = self._scan_obsidian_files()
            logger.info(f"Found {len(obsidian_files)} Obsidian files")
            
            if not obsidian_files:
                logger.warning("No Obsidian files found")
                return
            
            # 2. ファイルを解析
            contents = []
            for file_path in obsidian_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    parsed_data = self.markdown_parser.parse_file(file_path, content)
                    if parsed_data and parsed_data.get('content', {}).get('raw_content'):
                        contents.append({
                            "id": file_path,
                            "text": parsed_data['content']['raw_content'],
                            "metadata": {
                                "title": parsed_data.get('file_info', {}).get('name', ''),
                                "source": "obsidian",
                                "file_path": file_path,
                                "last_modified": parsed_data.get('file_info', {}).get('modified_time', ''),
                                "word_count": parsed_data.get('metadata', {}).get('word_count', 0)
                            }
                        })
                except Exception as e:
                    logger.warning(f"Failed to parse file {file_path}: {e}")
                    continue
            
            if not contents:
                logger.warning("No valid content found")
                return
            
            # 3. 分析を実行
            logger.info(f"Analyzing {len(contents)} contents...")
            analysis_results = await self.analysis_engine.analyze_content_comprehensive(contents)
            
            # 4. 結果をログに出力
            logger.info("Analysis completed:")
            logger.info(f"- Insights: {len(analysis_results.get('insights', []))}")
            logger.info(f"- Recommendations: {len(analysis_results.get('recommendations', []))}")
            logger.info(f"- Duplicates: {len(analysis_results.get('analysis_results', {}).get('basic_analysis', {}).get('duplicates', []))}")
            
            # 5. 結果をファイルに保存
            await self._save_results(analysis_results)
            
            logger.info("Analysis completed successfully")
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            raise
    
    def _scan_obsidian_files(self):
        """Obsidianファイルをスキャン"""
        try:
            vault_path = Path(self.vault_path)
            if not vault_path.exists():
                logger.warning(f"Vault path does not exist: {vault_path}")
                return []
            
            markdown_files = []
            for md_file in vault_path.rglob("*.md"):
                markdown_files.append(str(md_file))
            
            return markdown_files
            
        except Exception as e:
            logger.error(f"File scanning failed: {e}")
            return []
    
    async def _save_results(self, analysis_results):
        """分析結果をファイルに保存"""
        try:
            results_dir = Path("analysis-results")
            results_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 結果をJSONファイルに保存
            import json
            results_file = results_dir / f"analysis_results_{timestamp}.json"
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(analysis_results, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Results saved to: {results_file}")
            
        except Exception as e:
            logger.error(f"Failed to save results: {e}")

async def main():
    """メイン関数"""
    try:
        runner = GitHubActionsRunner()
        await runner.run_analysis()
    except Exception as e:
        logger.error(f"Runner failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
'''
    
    # ランナーファイルを保存
    runner_file = Path("sync_system/github_actions_runner.py")
    with open(runner_file, 'w', encoding='utf-8') as f:
        f.write(runner_content)
    
    print(f"✅ ランナーファイルを作成: {runner_file}")

def create_obsidian_vault_structure():
    """Obsidian保管庫の構造を作成"""
    print("🔧 Obsidian保管庫の構造を作成中...")
    
    vault_dir = Path("obsidian-vault")
    vault_dir.mkdir(exist_ok=True)
    
    # フォルダ構造を作成
    folders = [
        "00_Dashboard",
        "01_Content", 
        "02_Analysis",
        "03_Recommendations",
        "04_Sync",
        "05_Templates",
        "06_Archive"
    ]
    
    for folder in folders:
        folder_path = vault_dir / folder
        folder_path.mkdir(exist_ok=True)
        
        # READMEファイルを作成
        readme_file = folder_path / "README.md"
        if not readme_file.exists():
            with open(readme_file, 'w', encoding='utf-8') as f:
                f.write(f"# {folder}\n\nこのフォルダは{folder}用です。\n")
    
    print(f"✅ Obsidian保管庫の構造を作成: {vault_dir}")

def create_gitignore():
    """Gitignoreファイルを作成"""
    print("🔧 Gitignoreファイルを作成中...")
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
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

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log

# Analysis results
analysis-results/

# Obsidian
.obsidian/
"""
    
    with open(".gitignore", 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    
    print("✅ Gitignoreファイルを作成")

def create_readme():
    """READMEファイルを作成"""
    print("🔧 READMEファイルを作成中...")
    
    readme_content = """# Notion x Obsidian Integration

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
"""
    
    with open("README.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ READMEファイルを作成")

def main():
    """メイン関数"""
    print("🚀 GitHub Actions設定を開始...")
    print("=" * 60)
    
    # 1. GitHub Actionsワークフローを作成
    create_github_actions_workflow()
    
    # 2. GitHub Actionsランナーを作成
    create_github_actions_runner()
    
    # 3. Obsidian保管庫の構造を作成
    create_obsidian_vault_structure()
    
    # 4. Gitignoreファイルを作成
    create_gitignore()
    
    # 5. READMEファイルを作成
    create_readme()
    
    print("\n" + "=" * 60)
    print("✅ GitHub Actions設定が完了しました！")
    print("\n📋 次のステップ:")
    print("1. 変更をコミット・プッシュ")
    print("2. GitHubリポジトリのSecretsを設定")
    print("3. Obsidian Git プラグインを設定")
    print("4. テスト実行")

if __name__ == "__main__":
    main()
