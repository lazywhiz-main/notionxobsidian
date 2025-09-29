"""
イベントマネージャー
システム内のイベントを管理する
"""
import logging
import asyncio
import queue
import threading
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class Event:
    """イベントのデータクラス"""
    id: str
    type: str
    data: Dict[str, Any]
    timestamp: datetime
    source: str
    priority: int = 0

class EventManager:
    """イベントマネージャークラス"""
    
    def __init__(self):
        self.event_queue = queue.PriorityQueue()
        self.event_handlers = {}
        self.running = False
        self.event_thread = None
        self.event_history = []
        self.max_history_size = 1000
    
    async def initialize(self):
        """イベントマネージャーの初期化"""
        try:
            logger.info("Initializing event manager...")
            
            # デフォルトのイベントハンドラーを登録
            self._register_default_handlers()
            
            logger.info("Event manager initialized successfully")
            
        except Exception as e:
            logger.error(f"Event manager initialization failed: {e}")
            raise
    
    async def start(self):
        """イベントマネージャーの開始"""
        try:
            logger.info("Starting event manager...")
            self.running = True
            
            # イベント処理スレッドを開始
            self.event_thread = threading.Thread(target=self._event_loop)
            self.event_thread.start()
            
            logger.info("Event manager started successfully")
            
        except Exception as e:
            logger.error(f"Event manager start failed: {e}")
            raise
    
    async def stop(self):
        """イベントマネージャーの停止"""
        logger.info("Stopping event manager...")
        self.running = False
        
        if self.event_thread:
            self.event_thread.join()
    
    def _register_default_handlers(self):
        """デフォルトのイベントハンドラーを登録"""
        try:
            # 同期イベントのハンドラー
            self.register_handler('notion_change', self._handle_notion_change)
            self.register_handler('obsidian_change', self._handle_obsidian_change)
            self.register_handler('sync_complete', self._handle_sync_complete)
            self.register_handler('sync_error', self._handle_sync_error)
            
            # 分析イベントのハンドラー
            self.register_handler('analysis_complete', self._handle_analysis_complete)
            self.register_handler('insight_generated', self._handle_insight_generated)
            self.register_handler('recommendation_generated', self._handle_recommendation_generated)
            
            # システムイベントのハンドラー
            self.register_handler('system_error', self._handle_system_error)
            self.register_handler('system_warning', self._handle_system_warning)
            
            logger.info("Default event handlers registered")
            
        except Exception as e:
            logger.error(f"Default handler registration failed: {e}")
    
    def register_handler(self, event_type: str, handler: Callable):
        """イベントハンドラーの登録"""
        try:
            if event_type not in self.event_handlers:
                self.event_handlers[event_type] = []
            
            self.event_handlers[event_type].append(handler)
            logger.info(f"Registered handler for event type: {event_type}")
            
        except Exception as e:
            logger.error(f"Handler registration failed: {e}")
    
    def unregister_handler(self, event_type: str, handler: Callable):
        """イベントハンドラーの登録解除"""
        try:
            if event_type in self.event_handlers:
                if handler in self.event_handlers[event_type]:
                    self.event_handlers[event_type].remove(handler)
                    logger.info(f"Unregistered handler for event type: {event_type}")
            
        except Exception as e:
            logger.error(f"Handler unregistration failed: {e}")
    
    def emit_event(self, event_type: str, event_data: Dict[str, Any], 
                   source: str = 'system', priority: int = 0):
        """イベントの発生"""
        try:
            event = Event(
                id=self._generate_event_id(),
                type=event_type,
                data=event_data,
                timestamp=datetime.now(),
                source=source,
                priority=priority
            )
            
            # 優先度付きキューに追加（優先度が高いほど先に処理）
            self.event_queue.put((-priority, event))
            
            logger.debug(f"Event emitted: {event_type} from {source}")
            
        except Exception as e:
            logger.error(f"Event emission failed: {e}")
    
    def _event_loop(self):
        """イベントループ"""
        while self.running:
            try:
                # イベントを取得（タイムアウト付き）
                try:
                    priority, event = self.event_queue.get(timeout=1.0)
                    self._process_event(event)
                except queue.Empty:
                    continue
                
            except Exception as e:
                logger.error(f"Event loop error: {e}")
    
    def _process_event(self, event: Event):
        """イベントの処理"""
        try:
            # イベント履歴に追加
            self._add_to_history(event)
            
            # イベントハンドラーを実行
            if event.type in self.event_handlers:
                for handler in self.event_handlers[event.type]:
                    try:
                        handler(event)
                    except Exception as e:
                        logger.error(f"Event handler error: {e}")
            else:
                logger.warning(f"No handlers registered for event type: {event.type}")
            
        except Exception as e:
            logger.error(f"Event processing failed: {e}")
    
    def _add_to_history(self, event: Event):
        """イベント履歴に追加"""
        try:
            self.event_history.append(event)
            
            # 履歴サイズを制限
            if len(self.event_history) > self.max_history_size:
                self.event_history = self.event_history[-self.max_history_size:]
            
        except Exception as e:
            logger.error(f"History addition failed: {e}")
    
    def _generate_event_id(self) -> str:
        """イベントIDの生成"""
        return f"event_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    
    # デフォルトイベントハンドラー
    def _handle_notion_change(self, event: Event):
        """Notion変更イベントの処理"""
        try:
            logger.info(f"Notion change detected: {event.data.get('page_id', 'unknown')}")
            
            # 同期イベントを発生
            self.emit_event('sync_required', {
                'type': 'notion_to_obsidian',
                'page_id': event.data.get('page_id'),
                'action': event.data.get('action', 'update')
            }, source='notion_client', priority=1)
            
        except Exception as e:
            logger.error(f"Notion change handling failed: {e}")
    
    def _handle_obsidian_change(self, event: Event):
        """Obsidian変更イベントの処理"""
        try:
            logger.info(f"Obsidian change detected: {event.data.get('file_path', 'unknown')}")
            
            # 同期イベントを発生
            self.emit_event('sync_required', {
                'type': 'obsidian_to_notion',
                'file_path': event.data.get('file_path'),
                'action': event.data.get('action', 'update')
            }, source='obsidian_monitor', priority=1)
            
        except Exception as e:
            logger.error(f"Obsidian change handling failed: {e}")
    
    def _handle_sync_complete(self, event: Event):
        """同期完了イベントの処理"""
        try:
            logger.info(f"Sync completed: {event.data.get('sync_type', 'unknown')}")
            
            # 分析イベントを発生
            self.emit_event('analysis_required', {
                'content_list': event.data.get('content_list', []),
                'sync_type': event.data.get('sync_type')
            }, source='sync_coordinator', priority=2)
            
        except Exception as e:
            logger.error(f"Sync complete handling failed: {e}")
    
    def _handle_sync_error(self, event: Event):
        """同期エラーイベントの処理"""
        try:
            logger.error(f"Sync error: {event.data.get('error_message', 'Unknown error')}")
            
            # エラー通知イベントを発生
            self.emit_event('notification', {
                'type': 'error',
                'title': 'Sync Error',
                'message': event.data.get('error_message', 'Unknown error'),
                'action': 'retry_sync'
            }, source='sync_coordinator', priority=3)
            
        except Exception as e:
            logger.error(f"Sync error handling failed: {e}")
    
    def _handle_analysis_complete(self, event: Event):
        """分析完了イベントの処理"""
        try:
            logger.info(f"Analysis completed: {event.data.get('analysis_id', 'unknown')}")
            
            # インサイト生成イベントを発生
            self.emit_event('insight_generation_required', {
                'analysis_results': event.data.get('results', {}),
                'analysis_id': event.data.get('analysis_id')
            }, source='analysis_engine', priority=2)
            
        except Exception as e:
            logger.error(f"Analysis complete handling failed: {e}")
    
    def _handle_insight_generated(self, event: Event):
        """インサイト生成イベントの処理"""
        try:
            logger.info(f"Insight generated: {event.data.get('insight_type', 'unknown')}")
            
            # 推奨生成イベントを発生
            self.emit_event('recommendation_generation_required', {
                'insights': event.data.get('insights', []),
                'insight_id': event.data.get('insight_id')
            }, source='insight_generator', priority=2)
            
        except Exception as e:
            logger.error(f"Insight generated handling failed: {e}")
    
    def _handle_recommendation_generated(self, event: Event):
        """推奨生成イベントの処理"""
        try:
            logger.info(f"Recommendation generated: {event.data.get('recommendation_type', 'unknown')}")
            
            # 通知イベントを発生
            self.emit_event('notification', {
                'type': 'info',
                'title': 'New Recommendations',
                'message': f"{len(event.data.get('recommendations', []))} new recommendations available",
                'action': 'view_recommendations'
            }, source='recommendation_system', priority=1)
            
        except Exception as e:
            logger.error(f"Recommendation generated handling failed: {e}")
    
    def _handle_system_error(self, event: Event):
        """システムエラーイベントの処理"""
        try:
            logger.error(f"System error: {event.data.get('error_message', 'Unknown error')}")
            
            # エラー通知イベントを発生
            self.emit_event('notification', {
                'type': 'error',
                'title': 'System Error',
                'message': event.data.get('error_message', 'Unknown error'),
                'action': 'check_logs'
            }, source='system', priority=3)
            
        except Exception as e:
            logger.error(f"System error handling failed: {e}")
    
    def _handle_system_warning(self, event: Event):
        """システム警告イベントの処理"""
        try:
            logger.warning(f"System warning: {event.data.get('warning_message', 'Unknown warning')}")
            
            # 警告通知イベントを発生
            self.emit_event('notification', {
                'type': 'warning',
                'title': 'System Warning',
                'message': event.data.get('warning_message', 'Unknown warning'),
                'action': 'check_status'
            }, source='system', priority=2)
            
        except Exception as e:
            logger.error(f"System warning handling failed: {e}")
    
    def get_event_history(self, event_type: Optional[str] = None, limit: int = 100) -> List[Event]:
        """イベント履歴を取得"""
        try:
            if event_type:
                filtered_events = [e for e in self.event_history if e.type == event_type]
                return filtered_events[-limit:]
            else:
                return self.event_history[-limit:]
            
        except Exception as e:
            logger.error(f"Event history retrieval failed: {e}")
            return []
    
    def get_event_stats(self) -> Dict[str, Any]:
        """イベント統計を取得"""
        try:
            total_events = len(self.event_history)
            
            if total_events == 0:
                return {
                    'total_events': 0,
                    'events_by_type': {},
                    'events_by_source': {},
                    'events_by_priority': {},
                    'recent_events': []
                }
            
            # タイプ別の集計
            events_by_type = {}
            for event in self.event_history:
                events_by_type[event.type] = events_by_type.get(event.type, 0) + 1
            
            # ソース別の集計
            events_by_source = {}
            for event in self.event_history:
                events_by_source[event.source] = events_by_source.get(event.source, 0) + 1
            
            # 優先度別の集計
            events_by_priority = {}
            for event in self.event_history:
                events_by_priority[event.priority] = events_by_priority.get(event.priority, 0) + 1
            
            # 最近のイベント
            recent_events = self.event_history[-10:]
            
            return {
                'total_events': total_events,
                'events_by_type': events_by_type,
                'events_by_source': events_by_source,
                'events_by_priority': events_by_priority,
                'recent_events': recent_events
            }
            
        except Exception as e:
            logger.error(f"Event stats calculation failed: {e}")
            return {}
    
    def clear_history(self):
        """履歴をクリア"""
        self.event_history.clear()
        logger.info("Event history cleared")
    
    def get_queue_size(self) -> int:
        """キューサイズを取得"""
        return self.event_queue.qsize()
    
    def is_running(self) -> bool:
        """実行状態を取得"""
        return self.running
