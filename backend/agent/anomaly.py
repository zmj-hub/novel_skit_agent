import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from .models import TaskProgress, StepProgress, Anomaly
from .storage import storage

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnomalyDetector:
    """异常检测器"""
    
    def __init__(self, timeout_threshold: int = 30):
        """
        初始化异常检测器
        
        Args:
            timeout_threshold: 超时阈值（分钟）
        """
        self.timeout_threshold = timeout_threshold
    
    def detect_timeout(self, step: StepProgress) -> Optional[Anomaly]:
        """
        检测步骤超时
        
        Args:
            step: 步骤进度对象
            
        Returns:
            Optional[Anomaly]: 异常对象，如果没有异常则返回None
        """
        if step.status == "running":
            # 计算步骤运行时间
            start_time = datetime.fromisoformat(step.start_time)
            current_time = datetime.now()
            running_time = (current_time - start_time).total_seconds() / 60
            
            # 检查是否超时
            if running_time > max(step.estimated_duration * 1.5, self.timeout_threshold):
                return Anomaly(
                    "timeout",
                    "medium",
                    f"步骤 {step.step_name} 执行超时，已运行 {running_time:.1f} 分钟"
                )
        
        return None
    
    def detect_progress_stuck(self, step: StepProgress, previous_progress: float) -> Optional[Anomaly]:
        """
        检测进度停滞
        
        Args:
            step: 步骤进度对象
            previous_progress: 之前的进度
            
        Returns:
            Optional[Anomaly]: 异常对象，如果没有异常则返回None
        """
        if step.status == "running" and step.progress == previous_progress:
            # 检查步骤是否停滞
            start_time = datetime.fromisoformat(step.start_time)
            current_time = datetime.now()
            running_time = (current_time - start_time).total_seconds() / 60
            
            if running_time > self.timeout_threshold / 2:
                return Anomaly(
                    "progress_stuck",
                    "low",
                    f"步骤 {step.step_name} 进度停滞，当前进度 {step.progress}%"
                )
        
        return None
    
    def detect_error(self, step: StepProgress) -> Optional[Anomaly]:
        """
        检测步骤错误
        
        Args:
            step: 步骤进度对象
            
        Returns:
            Optional[Anomaly]: 异常对象，如果没有异常则返回None
        """
        if step.status == "failed":
            return Anomaly(
                "error",
                "high",
                f"步骤 {step.step_name} 执行失败"
            )
        
        return None
    
    def detect_all(self, task_progress: TaskProgress, previous_progress: Dict[str, float] = None) -> List[Anomaly]:
        """
        检测所有异常
        
        Args:
            task_progress: 任务进度对象
            previous_progress: 之前的进度字典，键为步骤ID，值为进度
            
        Returns:
            List[Anomaly]: 异常列表
        """
        anomalies = []
        
        if previous_progress is None:
            previous_progress = {}
        
        for step in task_progress.step_progress:
            # 检测超时
            timeout_anomaly = self.detect_timeout(step)
            if timeout_anomaly:
                anomalies.append(timeout_anomaly)
            
            # 检测进度停滞
            prev_progress = previous_progress.get(step.step_id, -1)
            if prev_progress >= 0:
                progress_anomaly = self.detect_progress_stuck(step, prev_progress)
                if progress_anomaly:
                    anomalies.append(progress_anomaly)
            
            # 检测错误
            error_anomaly = self.detect_error(step)
            if error_anomaly:
                anomalies.append(error_anomaly)
        
        return anomalies

class AlertSystem:
    """警报系统"""
    
    def __init__(self):
        """
        初始化警报系统
        """
        self.anomalies = []
    
    def add_anomaly(self, anomaly: Anomaly):
        """
        添加异常
        
        Args:
            anomaly: 异常对象
        """
        self.anomalies.append(anomaly)
        self._generate_alert(anomaly)
    
    def _generate_alert(self, anomaly: Anomaly):
        """
        生成警报
        
        Args:
            anomaly: 异常对象
        """
        # 根据严重程度生成不同级别的警报
        if anomaly.severity == "high":
            logger.error(f"[HIGH ALERT] {anomaly.description}")
        elif anomaly.severity == "medium":
            logger.warning(f"[MEDIUM ALERT] {anomaly.description}")
        else:
            logger.info(f"[LOW ALERT] {anomaly.description}")
    
    def get_alerts(self) -> List[Anomaly]:
        """
        获取所有警报
        
        Returns:
            List[Anomaly]: 异常列表
        """
        return self.anomalies
    
    def clear_alerts(self):
        """
        清除所有警报
        """
        self.anomalies.clear()
    
    def resolve_anomaly(self, anomaly_id: str, resolution: str):
        """
        解决异常
        
        Args:
            anomaly_id: 异常ID
            resolution: 解决方案
        """
        for anomaly in self.anomalies:
            if anomaly.anomaly_id == anomaly_id:
                anomaly.resolved = True
                anomaly.resolution = resolution
                logger.info(f"[RESOLVED] Anomaly {anomaly_id}: {resolution}")
                break

class AnomalyMonitor:
    """异常监控器"""
    
    def __init__(self, timeout_threshold: int = 30):
        """
        初始化异常监控器
        
        Args:
            timeout_threshold: 超时阈值（分钟）
        """
        self.detector = AnomalyDetector(timeout_threshold)
        self.alert_system = AlertSystem()
        self.previous_progress = {}
    
    def monitor_task(self, task_id: str) -> List[Anomaly]:
        """
        监控任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            List[Anomaly]: 新检测到的异常列表
        """
        task_progress = storage.get(task_id)
        if not task_progress:
            return []
        
        # 检测异常
        new_anomalies = self.detector.detect_all(task_progress, self.previous_progress)
        
        # 记录新异常
        for anomaly in new_anomalies:
            self.alert_system.add_anomaly(anomaly)
            task_progress.add_anomaly(anomaly)
        
        # 保存任务进度
        if new_anomalies:
            storage.save(task_progress)
        
        # 更新之前的进度
        self.previous_progress = {}
        for step in task_progress.step_progress:
            self.previous_progress[step.step_id] = step.progress
        
        return new_anomalies
    
    def monitor_all_tasks(self) -> Dict[str, List[Anomaly]]:
        """
        监控所有任务
        
        Returns:
            Dict[str, List[Anomaly]]: 任务ID到异常列表的映射
        """
        tasks = storage.list_all()
        results = {}
        
        for task in tasks:
            if task.status in ["running", "pending"]:
                anomalies = self.monitor_task(task.task_id)
                if anomalies:
                    results[task.task_id] = anomalies
        
        return results
    
    def get_alerts(self) -> List[Anomaly]:
        """
        获取所有警报
        
        Returns:
            List[Anomaly]: 异常列表
        """
        return self.alert_system.get_alerts()
    
    def clear_alerts(self):
        """
        清除所有警报
        """
        self.alert_system.clear_alerts()
    
    def resolve_anomaly(self, anomaly_id: str, resolution: str):
        """
        解决异常
        
        Args:
            anomaly_id: 异常ID
            resolution: 解决方案
        """
        self.alert_system.resolve_anomaly(anomaly_id, resolution)

# 全局异常监控器实例
anomaly_monitor = AnomalyMonitor()
