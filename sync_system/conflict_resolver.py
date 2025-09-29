"""
競合解決器
同期競合の検出と解決を行う
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class ConflictResolver:
    """競合解決器クラス"""
    
    def __init__(self):
        self.conflict_rules = {
            'notion_priority': self._resolve_notion_priority,
            'obsidian_priority': self._resolve_obsidian_priority,
            'newer_wins': self._resolve_newer_wins,
            'user_choice': self._resolve_user_choice,
            'merge': self._resolve_merge
        }
        self.conflict_history = []
    
    def detect_conflict(self, notion_content: Dict[str, Any], obsidian_content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """競合を検出"""
        try:
            conflicts = []
            
            # タイトルの競合
            notion_title = notion_content.get('title', '')
            obsidian_title = obsidian_content.get('title', '')
            
            if notion_title != obsidian_title:
                conflicts.append({
                    'type': 'title_conflict',
                    'field': 'title',
                    'notion_value': notion_title,
                    'obsidian_value': obsidian_title,
                    'notion_timestamp': notion_content.get('last_edited_time', ''),
                    'obsidian_timestamp': obsidian_content.get('modified_time', ''),
                    'severity': 'medium'
                })
            
            # コンテンツの競合
            notion_content_text = notion_content.get('content', '')
            obsidian_content_text = obsidian_content.get('content', '')
            
            if notion_content_text != obsidian_content_text:
                conflicts.append({
                    'type': 'content_conflict',
                    'field': 'content',
                    'notion_value': notion_content_text,
                    'obsidian_value': obsidian_content_text,
                    'notion_timestamp': notion_content.get('last_edited_time', ''),
                    'obsidian_timestamp': obsidian_content.get('modified_time', ''),
                    'severity': 'high'
                })
            
            # メタデータの競合
            notion_tags = notion_content.get('tags', [])
            obsidian_tags = obsidian_content.get('tags', [])
            
            if notion_tags != obsidian_tags:
                conflicts.append({
                    'type': 'tags_conflict',
                    'field': 'tags',
                    'notion_value': notion_tags,
                    'obsidian_value': obsidian_tags,
                    'notion_timestamp': notion_content.get('last_edited_time', ''),
                    'obsidian_timestamp': obsidian_content.get('modified_time', ''),
                    'severity': 'low'
                })
            
            logger.info(f"Detected {len(conflicts)} conflicts")
            return conflicts
            
        except Exception as e:
            logger.error(f"Conflict detection failed: {e}")
            return []
    
    def resolve_conflict(self, conflict: Dict[str, Any], resolution_strategy: str = 'user_choice') -> Dict[str, Any]:
        """競合を解決"""
        try:
            if resolution_strategy in self.conflict_rules:
                resolution = self.conflict_rules[resolution_strategy](conflict)
            else:
                resolution = self._resolve_user_choice(conflict)
            
            # 解決履歴に記録
            self.conflict_history.append({
                'conflict': conflict,
                'resolution': resolution,
                'strategy': resolution_strategy,
                'resolved_at': datetime.now().isoformat()
            })
            
            return resolution
            
        except Exception as e:
            logger.error(f"Conflict resolution failed: {e}")
            return {
                'resolved_value': None,
                'resolution_reason': 'Resolution failed',
                'confidence': 0.0,
                'requires_user_input': True
            }
    
    def _resolve_notion_priority(self, conflict: Dict[str, Any]) -> Dict[str, Any]:
        """Notion優先で解決"""
        return {
            'resolved_value': conflict['notion_value'],
            'resolution_reason': 'Notion priority rule',
            'confidence': 0.8,
            'requires_user_input': False
        }
    
    def _resolve_obsidian_priority(self, conflict: Dict[str, Any]) -> Dict[str, Any]:
        """Obsidian優先で解決"""
        return {
            'resolved_value': conflict['obsidian_value'],
            'resolution_reason': 'Obsidian priority rule',
            'confidence': 0.8,
            'requires_user_input': False
        }
    
    def _resolve_newer_wins(self, conflict: Dict[str, Any]) -> Dict[str, Any]:
        """新しい方で解決"""
        try:
            notion_time = self._parse_timestamp(conflict.get('notion_timestamp', ''))
            obsidian_time = self._parse_timestamp(conflict.get('obsidian_timestamp', ''))
            
            if notion_time > obsidian_time:
                return {
                    'resolved_value': conflict['notion_value'],
                    'resolution_reason': 'Newer wins rule (Notion)',
                    'confidence': 0.9,
                    'requires_user_input': False
                }
            else:
                return {
                    'resolved_value': conflict['obsidian_value'],
                    'resolution_reason': 'Newer wins rule (Obsidian)',
                    'confidence': 0.9,
                    'requires_user_input': False
                }
                
        except Exception as e:
            logger.error(f"Newer wins resolution failed: {e}")
            return self._resolve_user_choice(conflict)
    
    def _resolve_user_choice(self, conflict: Dict[str, Any]) -> Dict[str, Any]:
        """ユーザー選択で解決"""
        return {
            'resolved_value': None,
            'resolution_reason': 'User choice required',
            'confidence': 1.0,
            'requires_user_input': True,
            'options': [
                {'value': conflict['notion_value'], 'label': 'Notion version'},
                {'value': conflict['obsidian_value'], 'label': 'Obsidian version'},
                {'value': 'merge', 'label': 'Merge both versions'}
            ]
        }
    
    def _resolve_merge(self, conflict: Dict[str, Any]) -> Dict[str, Any]:
        """マージで解決"""
        try:
            conflict_type = conflict['type']
            
            if conflict_type == 'title_conflict':
                # タイトルのマージ（より長い方を選択）
                notion_title = conflict['notion_value']
                obsidian_title = conflict['obsidian_value']
                
                if len(notion_title) > len(obsidian_title):
                    merged_value = notion_title
                else:
                    merged_value = obsidian_title
                
                return {
                    'resolved_value': merged_value,
                    'resolution_reason': 'Merged titles (longer version)',
                    'confidence': 0.7,
                    'requires_user_input': False
                }
            
            elif conflict_type == 'content_conflict':
                # コンテンツのマージ（両方を結合）
                notion_content = conflict['notion_value']
                obsidian_content = conflict['obsidian_value']
                
                merged_content = f"{notion_content}\n\n---\n\n{obsidian_content}"
                
                return {
                    'resolved_value': merged_content,
                    'resolution_reason': 'Merged content (both versions)',
                    'confidence': 0.6,
                    'requires_user_input': False
                }
            
            elif conflict_type == 'tags_conflict':
                # タグのマージ（両方を結合）
                notion_tags = conflict['notion_value']
                obsidian_tags = conflict['obsidian_value']
                
                merged_tags = list(set(notion_tags + obsidian_tags))
                
                return {
                    'resolved_value': merged_tags,
                    'resolution_reason': 'Merged tags (both versions)',
                    'confidence': 0.9,
                    'requires_user_input': False
                }
            
            else:
                return self._resolve_user_choice(conflict)
                
        except Exception as e:
            logger.error(f"Merge resolution failed: {e}")
            return self._resolve_user_choice(conflict)
    
    def _parse_timestamp(self, timestamp_str: str) -> datetime:
        """タイムスタンプを解析"""
        try:
            if not timestamp_str:
                return datetime.min
            
            # ISO形式のタイムスタンプを解析
            return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            
        except Exception as e:
            logger.error(f"Timestamp parsing failed: {e}")
            return datetime.min
    
    def resolve_multiple_conflicts(self, conflicts: List[Dict[str, Any]], 
                                 resolution_strategy: str = 'user_choice') -> List[Dict[str, Any]]:
        """複数の競合を解決"""
        try:
            resolutions = []
            
            for conflict in conflicts:
                resolution = self.resolve_conflict(conflict, resolution_strategy)
                resolutions.append({
                    'conflict': conflict,
                    'resolution': resolution
                })
            
            return resolutions
            
        except Exception as e:
            logger.error(f"Multiple conflict resolution failed: {e}")
            return []
    
    def get_conflict_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """競合解決履歴を取得"""
        try:
            return self.conflict_history[-limit:]
            
        except Exception as e:
            logger.error(f"Conflict history retrieval failed: {e}")
            return []
    
    def get_conflict_stats(self) -> Dict[str, Any]:
        """競合統計を取得"""
        try:
            total_conflicts = len(self.conflict_history)
            
            if total_conflicts == 0:
                return {
                    'total_conflicts': 0,
                    'resolved_conflicts': 0,
                    'unresolved_conflicts': 0,
                    'resolution_rate': 0.0,
                    'conflicts_by_type': {},
                    'conflicts_by_severity': {}
                }
            
            resolved_conflicts = len([h for h in self.conflict_history if not h['resolution']['requires_user_input']])
            unresolved_conflicts = total_conflicts - resolved_conflicts
            
            # タイプ別の集計
            conflicts_by_type = {}
            for history in self.conflict_history:
                conflict_type = history['conflict']['type']
                conflicts_by_type[conflict_type] = conflicts_by_type.get(conflict_type, 0) + 1
            
            # 重要度別の集計
            conflicts_by_severity = {}
            for history in self.conflict_history:
                severity = history['conflict']['severity']
                conflicts_by_severity[severity] = conflicts_by_severity.get(severity, 0) + 1
            
            return {
                'total_conflicts': total_conflicts,
                'resolved_conflicts': resolved_conflicts,
                'unresolved_conflicts': unresolved_conflicts,
                'resolution_rate': resolved_conflicts / total_conflicts,
                'conflicts_by_type': conflicts_by_type,
                'conflicts_by_severity': conflicts_by_severity
            }
            
        except Exception as e:
            logger.error(f"Conflict stats calculation failed: {e}")
            return {}
    
    def clear_history(self):
        """履歴をクリア"""
        self.conflict_history.clear()
        logger.info("Conflict history cleared")
    
    def set_resolution_strategy(self, conflict_type: str, strategy: str):
        """競合タイプ別の解決戦略を設定"""
        try:
            if strategy in self.conflict_rules:
                # 実際の実装では、設定を保存
                logger.info(f"Set resolution strategy for {conflict_type}: {strategy}")
            else:
                logger.warning(f"Unknown resolution strategy: {strategy}")
                
        except Exception as e:
            logger.error(f"Resolution strategy setting failed: {e}")
    
    def get_resolution_strategies(self) -> List[str]:
        """利用可能な解決戦略を取得"""
        return list(self.conflict_rules.keys())
