"""
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
