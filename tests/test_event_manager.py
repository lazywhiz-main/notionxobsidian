"""
EventManagerのテスト
"""
import unittest
import sys
import os
import time
import threading

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sync_system.event_manager import EventManager, Event

class TestEventManager(unittest.TestCase):
    """EventManagerのテストクラス"""
    
    def setUp(self):
        """テストの前処理"""
        self.event_manager = EventManager()
        self.handler_called = False
        self.handler_data = None
    
    def test_event_creation(self):
        """イベントの作成テスト"""
        event = Event(
            id="test_event_1",
            type="test_event",
            data={"message": "test"},
            timestamp=time.time(),
            source="test",
            priority=1
        )
        
        self.assertEqual(event.id, "test_event_1")
        self.assertEqual(event.type, "test_event")
        self.assertEqual(event.data["message"], "test")
        self.assertEqual(event.source, "test")
        self.assertEqual(event.priority, 1)
    
    def test_event_emission(self):
        """イベントの発生テスト"""
        def test_handler(event):
            self.handler_called = True
            self.handler_data = event.data
        
        self.event_manager.register_handler("test_event", test_handler)
        
        # イベントを発生
        self.event_manager.emit_event("test_event", {"message": "test"}, "test_source", 1)
        
        # 少し待ってからハンドラーが呼ばれたかチェック
        time.sleep(0.1)
        
        self.assertTrue(self.handler_called)
        self.assertEqual(self.handler_data["message"], "test")
    
    def test_event_handler_registration(self):
        """イベントハンドラーの登録テスト"""
        def test_handler(event):
            pass
        
        self.event_manager.register_handler("test_event", test_handler)
        
        self.assertIn("test_event", self.event_manager.event_handlers)
        self.assertIn(test_handler, self.event_manager.event_handlers["test_event"])
    
    def test_event_handler_unregistration(self):
        """イベントハンドラーの登録解除テスト"""
        def test_handler(event):
            pass
        
        self.event_manager.register_handler("test_event", test_handler)
        self.event_manager.unregister_handler("test_event", test_handler)
        
        self.assertNotIn(test_handler, self.event_manager.event_handlers["test_event"])
    
    def test_event_history(self):
        """イベント履歴のテスト"""
        # イベントを発生
        self.event_manager.emit_event("test_event", {"message": "test1"}, "test_source", 1)
        self.event_manager.emit_event("test_event", {"message": "test2"}, "test_source", 1)
        
        # 少し待ってから履歴をチェック
        time.sleep(0.1)
        
        history = self.event_manager.get_event_history()
        self.assertGreaterEqual(len(history), 2)
    
    def test_event_stats(self):
        """イベント統計のテスト"""
        # イベントを発生
        self.event_manager.emit_event("test_event", {"message": "test1"}, "test_source", 1)
        self.event_manager.emit_event("other_event", {"message": "test2"}, "other_source", 2)
        
        # 少し待ってから統計をチェック
        time.sleep(0.1)
        
        stats = self.event_manager.get_event_stats()
        self.assertIsNotNone(stats)
        self.assertIn("total_events", stats)
        self.assertIn("events_by_type", stats)
        self.assertIn("events_by_source", stats)
        self.assertIn("events_by_priority", stats)
    
    def test_event_filtering(self):
        """イベントフィルタリングのテスト"""
        # 異なるタイプのイベントを発生
        self.event_manager.emit_event("test_event", {"message": "test1"}, "test_source", 1)
        self.event_manager.emit_event("other_event", {"message": "test2"}, "other_source", 1)
        
        # 少し待ってからフィルタリングをチェック
        time.sleep(0.1)
        
        test_events = self.event_manager.get_event_history("test_event")
        other_events = self.event_manager.get_event_history("other_event")
        
        self.assertGreaterEqual(len(test_events), 1)
        self.assertGreaterEqual(len(other_events), 1)
        
        for event in test_events:
            self.assertEqual(event.type, "test_event")
        
        for event in other_events:
            self.assertEqual(event.type, "other_event")
    
    def test_queue_size(self):
        """キューサイズのテスト"""
        initial_size = self.event_manager.get_queue_size()
        
        # イベントを発生
        self.event_manager.emit_event("test_event", {"message": "test"}, "test_source", 1)
        
        # キューサイズが増加することを確認
        new_size = self.event_manager.get_queue_size()
        self.assertGreaterEqual(new_size, initial_size)

if __name__ == '__main__':
    unittest.main()
