"""
テスト設定ファイル
"""
import pytest
import sys
import os
import tempfile
import shutil
from unittest.mock import Mock

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def temp_dir():
    """一時ディレクトリのフィクスチャ"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def mock_notion_client():
    """モックNotionクライアントのフィクスチャ"""
    client = Mock()
    client.token = "test_token"
    client.client = Mock()
    client.running = False
    client.database_ids = {}
    return client

@pytest.fixture
def mock_obsidian_monitor():
    """モックObsidianモニターのフィクスチャ"""
    monitor = Mock()
    monitor.vault_path = "/test/vault"
    monitor.observer = Mock()
    monitor.event_handler = Mock()
    monitor.running = False
    monitor.change_callback = None
    monitor.file_cache = {}
    return monitor

@pytest.fixture
def mock_analysis_engine():
    """モック分析エンジンのフィクスチャ"""
    engine = Mock()
    engine.content_analyzer = Mock()
    engine.insight_generator = Mock()
    engine.recommendation_system = Mock()
    engine.running = False
    engine.analysis_queue = Mock()
    engine.results_cache = {}
    return engine

@pytest.fixture
def mock_sync_coordinator():
    """モック同期コーディネーターのフィクスチャ"""
    coordinator = Mock()
    coordinator.notion_client = Mock()
    coordinator.obsidian_monitor = Mock()
    coordinator.analysis_engine = Mock()
    coordinator.running = False
    coordinator.sync_queue = Mock()
    coordinator.sync_status = {
        'success_count': 0,
        'pending_count': 0,
        'error_count': 0,
        'last_sync': None
    }
    return coordinator

@pytest.fixture
def mock_settings():
    """モック設定のフィクスチャ"""
    settings = Mock()
    settings.notion_token = "test_token"
    settings.obsidian_path = "/test/vault"
    settings.analysis_interval = 300
    settings.sync_interval = 60
    settings.similarity_threshold = 0.8
    settings.confidence_threshold = 0.7
    settings.log_level = "INFO"
    settings.log_file = "logs/app.log"
    settings.host = "0.0.0.0"
    settings.port = 8000
    settings.debug = False
    settings.redis_url = "redis://localhost:6379"
    return settings

@pytest.fixture
def sample_notion_content():
    """サンプルNotionコンテンツのフィクスチャ"""
    return {
        'page': {
            'id': 'test_page_id',
            'created_time': '2024-01-01T00:00:00Z',
            'last_edited_time': '2024-01-01T00:00:00Z',
            'properties': {
                'title': {
                    'title': [{'text': {'content': 'Test Page'}}]
                }
            }
        },
        'blocks': {
            'results': [
                {
                    'type': 'paragraph',
                    'paragraph': {
                        'rich_text': [{'text': {'content': 'This is a test paragraph.'}}]
                    }
                }
            ]
        }
    }

@pytest.fixture
def sample_obsidian_content():
    """サンプルObsidianコンテンツのフィクスチャ"""
    return {
        'title': 'Test Note',
        'content': '# Test Note\n\nThis is a test note.',
        'frontmatter': {
            'tags': ['test', 'note'],
            'obsidian_id': 'test_note_id'
        }
    }

@pytest.fixture
def sample_analysis_results():
    """サンプル分析結果のフィクスチャ"""
    return {
        'similarity': [
            {
                'content1_index': 0,
                'content2_index': 1,
                'similarity': 0.85,
                'content1_preview': 'Test content 1',
                'content2_preview': 'Test content 2'
            }
        ],
        'duplicates': [
            {
                'text1_index': 0,
                'text2_index': 1,
                'similarity': 0.95,
                'text1_preview': 'Duplicate content 1',
                'text2_preview': 'Duplicate content 2'
            }
        ],
        'topics': [
            {
                'topic': 'AI',
                'count': 5,
                'confidence': 0.8
            }
        ],
        'sentiment': [
            {
                'content_id': 'test_content',
                'content_title': 'Test Content',
                'sentiment': 'POSITIVE',
                'confidence': 0.9
            }
        ],
        'readability': [
            {
                'content_id': 'test_content',
                'content_title': 'Test Content',
                'readability_score': 0.7
            }
        ]
    }

@pytest.fixture
def sample_insights():
    """サンプルインサイトのフィクスチャ"""
    from analysis_engine.insight_generator import Insight
    import time
    
    return [
        Insight(
            id='insight_1',
            type='similarity',
            title='Similarity Insight',
            content='Test insight',
            confidence=0.8,
            source_data={},
            created_at=time.time(),
            tags=['similarity']
        ),
        Insight(
            id='insight_2',
            type='duplicate',
            title='Duplicate Insight',
            content='Test insight',
            confidence=0.9,
            source_data={},
            created_at=time.time(),
            tags=['duplicate']
        )
    ]

@pytest.fixture
def sample_action_items():
    """サンプルアクションアイテムのフィクスチャ"""
    from analysis_engine.recommendation_system import ActionItem
    import time
    
    return [
        ActionItem(
            id='action_1',
            title='Test Action 1',
            description='Test description',
            action_type='create_link',
            priority='high',
            estimated_time='5分',
            steps=['Step 1', 'Step 2'],
            status='pending',
            insight_id='insight_1',
            created_at=time.time(),
            updated_at=time.time()
        ),
        ActionItem(
            id='action_2',
            title='Test Action 2',
            description='Test description',
            action_type='merge_duplicate',
            priority='medium',
            estimated_time='15分',
            steps=['Step 1', 'Step 2', 'Step 3'],
            status='pending',
            insight_id='insight_2',
            created_at=time.time(),
            updated_at=time.time()
        )
    ]

@pytest.fixture
def sample_conflict():
    """サンプル競合のフィクスチャ"""
    return {
        'type': 'title_conflict',
        'field': 'title',
        'notion_value': 'Notion Title',
        'obsidian_value': 'Obsidian Title',
        'notion_timestamp': '2024-01-01T00:00:00Z',
        'obsidian_timestamp': '2024-01-01T00:00:00Z',
        'severity': 'medium'
    }

@pytest.fixture
def sample_event():
    """サンプルイベントのフィクスチャ"""
    from sync_system.event_manager import Event
    from datetime import datetime
    
    return Event(
        id='test_event_1',
        type='test_event',
        data={'message': 'test'},
        timestamp=datetime.now(),
        source='test',
        priority=1
    )
