import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from .models import TaskProgress

class ProgressStorage:
    """进度存储系统"""
    
    def __init__(self, storage_dir: str = None):
        """
        初始化存储系统
        
        Args:
            storage_dir: 存储目录路径，默认为 backend/data/progress
        """
        # 内存存储
        self.memory_storage: Dict[str, TaskProgress] = {}
        
        # 文件存储目录
        if storage_dir is None:
            self.storage_dir = os.path.join(os.path.dirname(__file__), "..", "data", "progress")
        else:
            self.storage_dir = storage_dir
        
        # 确保存储目录存在
        os.makedirs(self.storage_dir, exist_ok=True)
    
    def save(self, task_progress: TaskProgress):
        """
        保存任务进度
        
        Args:
            task_progress: 任务进度对象
        """
        # 保存到内存
        self.memory_storage[task_progress.task_id] = task_progress
        
        # 保存到文件
        file_path = os.path.join(self.storage_dir, f"{task_progress.task_id}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(task_progress.to_dict(), f, ensure_ascii=False, indent=2)
    
    def get(self, task_id: str) -> Optional[TaskProgress]:
        """
        获取任务进度
        
        Args:
            task_id: 任务ID
            
        Returns:
            Optional[TaskProgress]: 任务进度对象，不存在则返回None
        """
        # 先从内存获取
        if task_id in self.memory_storage:
            return self.memory_storage[task_id]
        
        # 从文件获取
        file_path = os.path.join(self.storage_dir, f"{task_id}.json")
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 重建TaskProgress对象
                    progress = TaskProgress(
                        task_id=data['task_id'],
                        session_id=data['session_id'],
                        story_type=data['story_type']
                    )
                    # 恢复其他属性
                    progress.status = data['status']
                    progress.start_time = data['start_time']
                    progress.end_time = data['end_time']
                    progress.estimated_end_time = data['estimated_end_time']
                    progress.current_step = data['current_step']
                    progress.completed_steps = data['completed_steps']
                    progress.total_steps = data['total_steps']
                    progress.progress = data['progress']
                    progress.updated_at = data['updated_at']
                    
                    # 恢复步骤进度
                    for step_data in data['step_progress']:
                        step = progress.add_step(step_data['step_name'], step_data['agent_name'])
                        step.step_id = step_data['step_id']
                        step.status = step_data['status']
                        step.progress = step_data['progress']
                        step.start_time = step_data['start_time']
                        step.end_time = step_data['end_time']
                        step.estimated_duration = step_data['estimated_duration']
                        step.actual_duration = step_data['actual_duration']
                    
                    # 恢复异常
                    for anomaly_data in data['anomalies']:
                        from .models import Anomaly
                        anomaly = Anomaly(
                            type=anomaly_data['type'],
                            severity=anomaly_data['severity'],
                            description=anomaly_data['description']
                        )
                        anomaly.anomaly_id = anomaly_data['anomaly_id']
                        anomaly.detected_at = anomaly_data['detected_at']
                        anomaly.resolved = anomaly_data['resolved']
                        anomaly.resolution = anomaly_data['resolution']
                        progress.add_anomaly(anomaly)
                    
                    # 保存到内存
                    self.memory_storage[task_id] = progress
                    return progress
            except Exception as e:
                print(f"Error loading task progress from file: {e}")
                return None
        
        return None
    
    def get_by_session(self, session_id: str) -> List[TaskProgress]:
        """
        根据会话ID获取任务进度列表
        
        Args:
            session_id: 会话ID
            
        Returns:
            List[TaskProgress]: 任务进度列表
        """
        # 从内存中获取
        memory_tasks = [p for p in self.memory_storage.values() if p.session_id == session_id]
        
        # 从文件中获取
        file_tasks = []
        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(self.storage_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if data.get('session_id') == session_id:
                            # 检查是否已在内存中
                            task_id = data['task_id']
                            if task_id not in self.memory_storage:
                                # 重建TaskProgress对象
                                progress = TaskProgress(
                                    task_id=data['task_id'],
                                    session_id=data['session_id'],
                                    story_type=data['story_type']
                                )
                                # 恢复其他属性
                                progress.status = data['status']
                                progress.start_time = data['start_time']
                                progress.end_time = data['end_time']
                                progress.estimated_end_time = data['estimated_end_time']
                                progress.current_step = data['current_step']
                                progress.completed_steps = data['completed_steps']
                                progress.total_steps = data['total_steps']
                                progress.progress = data['progress']
                                progress.updated_at = data['updated_at']
                                
                                # 恢复步骤进度
                                for step_data in data['step_progress']:
                                    step = progress.add_step(step_data['step_name'], step_data['agent_name'])
                                    step.step_id = step_data['step_id']
                                    step.status = step_data['status']
                                    step.progress = step_data['progress']
                                    step.start_time = step_data['start_time']
                                    step.end_time = step_data['end_time']
                                    step.estimated_duration = step_data['estimated_duration']
                                    step.actual_duration = step_data['actual_duration']
                                
                                # 恢复异常
                                for anomaly_data in data['anomalies']:
                                    from .models import Anomaly
                                    anomaly = Anomaly(
                                        type=anomaly_data['type'],
                                        severity=anomaly_data['severity'],
                                        description=anomaly_data['description']
                                    )
                                    anomaly.anomaly_id = anomaly_data['anomaly_id']
                                    anomaly.detected_at = anomaly_data['detected_at']
                                    anomaly.resolved = anomaly_data['resolved']
                                    anomaly.resolution = anomaly_data['resolution']
                                    progress.add_anomaly(anomaly)
                                
                                file_tasks.append(progress)
                except Exception as e:
                    print(f"Error loading task progress from file: {e}")
        
        return memory_tasks + file_tasks
    
    def delete(self, task_id: str):
        """
        删除任务进度
        
        Args:
            task_id: 任务ID
        """
        # 从内存删除
        if task_id in self.memory_storage:
            del self.memory_storage[task_id]
        
        # 从文件删除
        file_path = os.path.join(self.storage_dir, f"{task_id}.json")
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting task progress file: {e}")
    
    def list_all(self) -> List[TaskProgress]:
        """
        列出所有任务进度
        
        Returns:
            List[TaskProgress]: 任务进度列表
        """
        # 从内存获取
        memory_tasks = list(self.memory_storage.values())
        
        # 从文件获取
        file_tasks = []
        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(self.storage_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # 检查是否已在内存中
                        task_id = data['task_id']
                        if task_id not in self.memory_storage:
                            # 重建TaskProgress对象
                            progress = TaskProgress(
                                task_id=data['task_id'],
                                session_id=data['session_id'],
                                story_type=data['story_type']
                            )
                            # 恢复其他属性
                            progress.status = data['status']
                            progress.start_time = data['start_time']
                            progress.end_time = data['end_time']
                            progress.estimated_end_time = data['estimated_end_time']
                            progress.current_step = data['current_step']
                            progress.completed_steps = data['completed_steps']
                            progress.total_steps = data['total_steps']
                            progress.progress = data['progress']
                            progress.updated_at = data['updated_at']
                            
                            # 恢复步骤进度
                            for step_data in data['step_progress']:
                                step = progress.add_step(step_data['step_name'], step_data['agent_name'])
                                step.step_id = step_data['step_id']
                                step.status = step_data['status']
                                step.progress = step_data['progress']
                                step.start_time = step_data['start_time']
                                step.end_time = step_data['end_time']
                                step.estimated_duration = step_data['estimated_duration']
                                step.actual_duration = step_data['actual_duration']
                            
                            # 恢复异常
                            for anomaly_data in data['anomalies']:
                                from .models import Anomaly
                                anomaly = Anomaly(
                                    type=anomaly_data['type'],
                                    severity=anomaly_data['severity'],
                                    description=anomaly_data['description']
                                )
                                anomaly.anomaly_id = anomaly_data['anomaly_id']
                                anomaly.detected_at = anomaly_data['detected_at']
                                anomaly.resolved = anomaly_data['resolved']
                                anomaly.resolution = anomaly_data['resolution']
                                progress.add_anomaly(anomaly)
                            
                            file_tasks.append(progress)
                except Exception as e:
                    print(f"Error loading task progress from file: {e}")
        
        return memory_tasks + file_tasks
    
    def clear_memory(self):
        """
        清空内存存储
        """
        self.memory_storage.clear()
    
    def get_storage_stats(self) -> Dict[str, int]:
        """
        获取存储统计信息
        
        Returns:
            Dict[str, int]: 统计信息
        """
        # 内存存储统计
        memory_count = len(self.memory_storage)
        
        # 文件存储统计
        file_count = 0
        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json'):
                file_count += 1
        
        return {
            "memory_count": memory_count,
            "file_count": file_count,
            "total_count": memory_count + file_count
        }

# 全局存储实例
storage = ProgressStorage()


class ReportStorage:
    """执行报告存储系统"""
    
    def __init__(self, storage_dir: str = None):
        """
        初始化报告存储系统
        
        Args:
            storage_dir: 存储目录路径，默认为 backend/data/reports
        """
        # 内存存储
        self.memory_storage: Dict[str, Any] = {}
        
        # 文件存储目录
        if storage_dir is None:
            self.storage_dir = os.path.join(os.path.dirname(__file__), "..", "data", "reports")
        else:
            self.storage_dir = storage_dir
        
        # 确保存储目录存在
        os.makedirs(self.storage_dir, exist_ok=True)
    
    def _get_report_filename(self, task_id: str, step_index: int, step_name: str) -> str:
        """
        生成报告文件名
        
        Args:
            task_id: 任务ID
            step_index: 步骤索引
            step_name: 步骤名称
            
        Returns:
            str: 文件名
        """
        # 清理步骤名称，移除不安全的字符
        safe_step_name = "".join(c for c in step_name if c.isalnum() or c in "_-").strip()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{task_id}_step{step_index:03d}_{safe_step_name}_{timestamp}.json"
    
    def save_step_report(self, report) -> str:
        """
        保存步骤执行报告
        
        Args:
            report: 步骤执行报告对象 (StepExecutionReport)
            
        Returns:
            str: 保存的文件路径
        """
        # 保存到内存
        report_key = f"{report.task_id}_{report.step_index}"
        self.memory_storage[report_key] = report
        
        # 生成文件名
        filename = self._get_report_filename(
            report.task_id, 
            report.step_index, 
            report.step_name
        )
        file_path = os.path.join(self.storage_dir, filename)
        
        # 保存到文件
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(report.to_dict(), f, ensure_ascii=False, indent=2)
            return file_path
        except Exception as e:
            print(f"Error saving step report to file: {e}")
            return ""
    
    def get_step_report(self, task_id: str, step_index: int) -> Optional[Any]:
        """
        获取步骤执行报告
        
        Args:
            task_id: 任务ID
            step_index: 步骤索引
            
        Returns:
            Optional[StepExecutionReport]: 步骤执行报告对象，不存在则返回None
        """
        # 先从内存获取
        report_key = f"{task_id}_{step_index}"
        if report_key in self.memory_storage:
            return self.memory_storage[report_key]
        
        # 从文件搜索
        try:
            for filename in os.listdir(self.storage_dir):
                if filename.startswith(f"{task_id}_step{step_index:03d}_") and filename.endswith('.json'):
                    file_path = os.path.join(self.storage_dir, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        return data
        except Exception as e:
            print(f"Error loading step report from file: {e}")
        
        return None
    
    def get_task_reports(self, task_id: str) -> List[Dict[str, Any]]:
        """
        获取任务的所有步骤执行报告
        
        Args:
            task_id: 任务ID
            
        Returns:
            List[Dict[str, Any]]: 步骤执行报告列表，按步骤索引排序
        """
        reports = []
        
        # 从内存获取
        for key, report in self.memory_storage.items():
            if key.startswith(f"{task_id}_"):
                reports.append(report.to_dict() if hasattr(report, 'to_dict') else report)
        
        # 从文件获取
        try:
            for filename in os.listdir(self.storage_dir):
                if filename.startswith(f"{task_id}_step") and filename.endswith('.json'):
                    # 检查是否已在内存中
                    parts = filename.split('_')
                    if len(parts) >= 2 and parts[1].startswith('step'):
                        step_index = int(parts[1][4:7])  # 提取步骤索引
                        report_key = f"{task_id}_{step_index}"
                        if report_key not in self.memory_storage:
                            file_path = os.path.join(self.storage_dir, filename)
                            with open(file_path, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                reports.append(data)
        except Exception as e:
            print(f"Error loading task reports from files: {e}")
        
        # 按步骤索引排序
        reports.sort(key=lambda x: x.get('step_index', 0))
        return reports
    
    def delete_task_reports(self, task_id: str):
        """
        删除任务的所有报告
        
        Args:
            task_id: 任务ID
        """
        # 从内存删除
        keys_to_delete = [key for key in self.memory_storage.keys() if key.startswith(f"{task_id}_")]
        for key in keys_to_delete:
            del self.memory_storage[key]
        
        # 从文件删除
        try:
            for filename in os.listdir(self.storage_dir):
                if filename.startswith(f"{task_id}_") and filename.endswith('.json'):
                    file_path = os.path.join(self.storage_dir, filename)
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        print(f"Error deleting report file {filename}: {e}")
        except Exception as e:
            print(f"Error deleting task reports: {e}")
    
    def clear_memory(self):
        """清空内存存储"""
        self.memory_storage.clear()
    
    def get_storage_stats(self) -> Dict[str, int]:
        """
        获取存储统计信息
        
        Returns:
            Dict[str, int]: 统计信息
        """
        # 内存存储统计
        memory_count = len(self.memory_storage)
        
        # 文件存储统计
        file_count = 0
        try:
            for filename in os.listdir(self.storage_dir):
                if filename.endswith('.json'):
                    file_count += 1
        except Exception:
            pass
        
        return {
            "memory_count": memory_count,
            "file_count": file_count,
            "total_count": memory_count + file_count
        }


# 全局报告存储实例
report_storage = ReportStorage()
