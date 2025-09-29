"""
ObsidianFileMonitorのテスト
"""
import unittest
import sys
import os
import tempfile
import shutil
import asyncio
from unittest.mock import Mock, patch

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from obsidian_integration.file_monitor import ObsidianFileMonitor, ObsidianFileHandler

class TestObsidianFileMonitor(unittest.TestCase):
    """ObsidianFileMonitorのテストクラス"""
    
    def setUp(self):
        """テストの前処理"""
        # 一時ディレクトリを作成
        self.temp_dir = tempfile.mkdtemp()
        self.monitor = ObsidianFileMonitor(self.temp_dir)
        self.handler_called = False
        self.handler_data = None
    
    def tearDown(self):
        """テストの後処理"""
        # 一時ディレクトリを削除
        shutil.rmtree(self.temp_dir)
    
    def test_monitor_initialization(self):
        """モニターの初期化テスト"""
        self.assertEqual(self.monitor.vault_path, self.temp_dir)
        self.assertIsNone(self.monitor.observer)
        self.assertIsNone(self.monitor.event_handler)
        self.assertFalse(self.monitor.running)
        self.assertIsNone(self.monitor.change_callback)
        self.assertIsInstance(self.monitor.file_cache, dict)
    
    def test_handler_initialization(self):
        """ハンドラーの初期化テスト"""
        handler = ObsidianFileHandler(self.temp_dir)
        
        self.assertEqual(handler.vault_path, self.temp_dir)
        self.assertIsNone(handler.change_callback)
        self.assertIsInstance(handler.last_modified, dict)
    
    def test_set_change_callback(self):
        """変更コールバックの設定テスト"""
        def test_callback(event):
            self.handler_called = True
            self.handler_data = event
        
        self.monitor.set_change_callback(test_callback)
        self.assertEqual(self.monitor.change_callback, test_callback)
    
    def test_get_file_info(self):
        """ファイル情報の取得テスト"""
        # テストファイルを作成
        test_file = os.path.join(self.temp_dir, 'test.md')
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('# Test File\n\nThis is a test file.')
        
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            file_info = loop.run_until_complete(
                self.monitor._get_file_info(test_file)
            )
            
            self.assertIsNotNone(file_info)
            self.assertIn('path', file_info)
            self.assertIn('name', file_info)
            self.assertIn('size', file_info)
            self.assertIn('created_time', file_info)
            self.assertIn('modified_time', file_info)
            self.assertIn('relative_path', file_info)
            
            self.assertEqual(file_info['path'], test_file)
            self.assertEqual(file_info['name'], 'test.md')
            self.assertGreater(file_info['size'], 0)
            
        finally:
            loop.close()
    
    def test_get_file_info_nonexistent(self):
        """存在しないファイルの情報取得テスト"""
        nonexistent_file = os.path.join(self.temp_dir, 'nonexistent.md')
        
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            file_info = loop.run_until_complete(
                self.monitor._get_file_info(nonexistent_file)
            )
            
            self.assertIsNone(file_info)
            
        finally:
            loop.close()
    
    def test_get_file_content(self):
        """ファイルコンテンツの取得テスト"""
        # テストファイルを作成
        test_file = os.path.join(self.temp_dir, 'test.md')
        test_content = '# Test File\n\nThis is a test file.'
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            content = loop.run_until_complete(
                self.monitor.get_file_content(test_file)
            )
            
            self.assertEqual(content, test_content)
            
        finally:
            loop.close()
    
    def test_get_file_content_nonexistent(self):
        """存在しないファイルのコンテンツ取得テスト"""
        nonexistent_file = os.path.join(self.temp_dir, 'nonexistent.md')
        
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            content = loop.run_until_complete(
                self.monitor.get_file_content(nonexistent_file)
            )
            
            self.assertIsNone(content)
            
        finally:
            loop.close()
    
    def test_write_file_content(self):
        """ファイルコンテンツの書き込みテスト"""
        test_file = os.path.join(self.temp_dir, 'test.md')
        test_content = '# Test File\n\nThis is a test file.'
        
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                self.monitor.write_file_content(test_file, test_content)
            )
            
            self.assertTrue(result)
            
            # ファイルが作成されたことを確認
            self.assertTrue(os.path.exists(test_file))
            
            # コンテンツが正しく書き込まれたことを確認
            with open(test_file, 'r', encoding='utf-8') as f:
                written_content = f.read()
            self.assertEqual(written_content, test_content)
            
        finally:
            loop.close()
    
    def test_write_file_content_nested_directory(self):
        """ネストしたディレクトリへのファイル書き込みテスト"""
        nested_dir = os.path.join(self.temp_dir, 'subdir')
        test_file = os.path.join(nested_dir, 'test.md')
        test_content = '# Test File\n\nThis is a test file.'
        
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                self.monitor.write_file_content(test_file, test_content)
            )
            
            self.assertTrue(result)
            
            # ディレクトリが作成されたことを確認
            self.assertTrue(os.path.exists(nested_dir))
            
            # ファイルが作成されたことを確認
            self.assertTrue(os.path.exists(test_file))
            
        finally:
            loop.close()
    
    def test_get_all_markdown_files(self):
        """すべてのMarkdownファイルの取得テスト"""
        # テストファイルを作成
        test_files = [
            'test1.md',
            'test2.md',
            'subdir/test3.md',
            'subdir/test4.md'
        ]
        
        for file_path in test_files:
            full_path = os.path.join(self.temp_dir, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(f'# {file_path}\n\nTest content.')
        
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            files = loop.run_until_complete(
                self.monitor.get_all_markdown_files()
            )
            
            self.assertEqual(len(files), 4)
            
            # ファイル名の確認
            file_names = [f['name'] for f in files]
            for test_file in test_files:
                self.assertIn(os.path.basename(test_file), file_names)
            
        finally:
            loop.close()
    
    def test_search_files(self):
        """ファイルの検索テスト"""
        # テストファイルを作成
        test_files = [
            'test_note.md',
            'another_test.md',
            'different_file.md'
        ]
        
        for file_name in test_files:
            file_path = os.path.join(self.temp_dir, file_name)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f'# {file_name}\n\nTest content.')
        
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # "test"で検索
            results = loop.run_until_complete(
                self.monitor.search_files('test')
            )
            
            self.assertEqual(len(results), 2)
            
            # ファイル名の確認
            file_names = [f['name'] for f in results]
            self.assertIn('test_note.md', file_names)
            self.assertIn('another_test.md', file_names)
            
        finally:
            loop.close()
    
    def test_get_file_cache(self):
        """ファイルキャッシュの取得テスト"""
        # テストファイルを作成
        test_file = os.path.join(self.temp_dir, 'test.md')
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('# Test File\n\nThis is a test file.')
        
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # ファイルキャッシュを初期化
            loop.run_until_complete(self.monitor._initialize_file_cache())
            
            cache = self.monitor.get_file_cache()
            
            self.assertIsInstance(cache, dict)
            self.assertGreater(len(cache), 0)
            
            # テストファイルがキャッシュに含まれていることを確認
            self.assertIn(test_file, cache)
            
        finally:
            loop.close()
    
    def test_get_cache_stats(self):
        """キャッシュ統計の取得テスト"""
        # テストファイルを作成
        test_files = [
            'test1.md',
            'test2.md',
            'test3.md'
        ]
        
        for file_name in test_files:
            file_path = os.path.join(self.temp_dir, file_name)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f'# {file_name}\n\nTest content.')
        
        # 非同期テストの実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # ファイルキャッシュを初期化
            loop.run_until_complete(self.monitor._initialize_file_cache())
            
            stats = self.monitor.get_cache_stats()
            
            self.assertIsNotNone(stats)
            self.assertIn('total_files', stats)
            self.assertIn('total_size', stats)
            self.assertIn('average_size', stats)
            
            self.assertEqual(stats['total_files'], 3)
            self.assertGreater(stats['total_size'], 0)
            self.assertGreater(stats['average_size'], 0)
            
        finally:
            loop.close()
    
    def test_handle_file_change(self):
        """ファイル変更の処理テスト"""
        def test_callback(event):
            self.handler_called = True
            self.handler_data = event
        
        self.monitor.set_change_callback(test_callback)
        
        # テストファイルを作成
        test_file = os.path.join(self.temp_dir, 'test.md')
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('# Test File\n\nThis is a test file.')
        
        # ファイル変更を処理
        self.monitor._handle_file_change(test_file, 'modified')
        
        # コールバックが呼ばれたことを確認
        self.assertTrue(self.handler_called)
        self.assertIsNotNone(self.handler_data)
        self.assertEqual(self.handler_data['file_path'], test_file)
        self.assertEqual(self.handler_data['action'], 'modified')
    
    def test_handle_file_change_no_callback(self):
        """コールバックがない場合のファイル変更処理テスト"""
        # テストファイルを作成
        test_file = os.path.join(self.temp_dir, 'test.md')
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('# Test File\n\nThis is a test file.')
        
        # コールバックを設定せずにファイル変更を処理
        self.monitor._handle_file_change(test_file, 'modified')
        
        # エラーが発生しないことを確認
        self.assertFalse(self.handler_called)
        self.assertIsNone(self.handler_data)

if __name__ == '__main__':
    unittest.main()
