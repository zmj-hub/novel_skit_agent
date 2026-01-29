from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import os

from core.agent_config import agent_config
from core.config import settings


class ModelVersion:
    """模型版本类"""
    def __init__(self,
                 model_id: str,
                 version: str,
                 name: str,
                 description: str = "",
                 is_active: bool = False,
                 created_at: Optional[datetime] = None,
                 last_used_at: Optional[datetime] = None,
                 compatibility: Dict[str, Any] = None):
        self.model_id = model_id
        self.version = version
        self.name = name
        self.description = description
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.last_used_at = last_used_at
        self.compatibility = compatibility or {
            "agents": [],
            "features": [],
            "min_version": "1.0.0"
        }

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "model_id": self.model_id,
            "version": self.version,
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "last_used_at": self.last_used_at.isoformat() if self.last_used_at else None,
            "compatibility": self.compatibility
        }

    def update_last_used(self):
        """更新最后使用时间"""
        self.last_used_at = datetime.now()


class ModelVersionManager:
    """模型版本管理器"""
    def __init__(self):
        self.model_versions: Dict[str, List[ModelVersion]] = {}
        self.version_history: List[Dict[str, Any]] = []
        self.version_file = "config/model_versions.json"
        self._load_versions()
        self._init_default_versions()

    def _load_versions(self):
        """从文件加载模型版本"""
        try:
            if os.path.exists(self.version_file):
                with open(self.version_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for model_id, versions in data.get("model_versions", {}).items():
                        self.model_versions[model_id] = []
                        for version_data in versions:
                            version = ModelVersion(
                                model_id=version_data["model_id"],
                                version=version_data["version"],
                                name=version_data["name"],
                                description=version_data.get("description", ""),
                                is_active=version_data.get("is_active", False),
                                created_at=datetime.fromisoformat(version_data["created_at"]),
                                last_used_at=datetime.fromisoformat(version_data["last_used_at"]) if version_data.get("last_used_at") else None,
                                compatibility=version_data.get("compatibility", {})
                            )
                            self.model_versions[model_id].append(version)
                self.version_history = data.get("version_history", [])
        except Exception as e:
            print(f"加载模型版本失败: {e}")

    def _save_versions(self):
        """保存模型版本到文件"""
        try:
            # 确保配置目录存在
            config_dir = os.path.dirname(self.version_file)
            if config_dir and not os.path.exists(config_dir):
                os.makedirs(config_dir)

            data = {
                "model_versions": {},
                "version_history": self.version_history
            }

            for model_id, versions in self.model_versions.items():
                try:
                    data["model_versions"][model_id] = [v.to_dict() for v in versions]
                except Exception as e:
                    print(f"序列化模型版本失败: {model_id}, {e}")
                    data["model_versions"][model_id] = []

            with open(self.version_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存模型版本失败: {e}")

    def _init_default_versions(self):
        """初始化默认模型版本"""
        # 协调智能体模型版本
        self.add_model_version(
            model_id="coordination",
            version="1.0.0",
            name="Qwen/Qwen3-235B-A22B-Instruct-2507",
            description="协调智能体默认模型，负责任务分发、流程控制与跨智能体通信",
            is_active=True,
            compatibility={
                "agents": ["coordination"],
                "features": ["task_distribution", "process_control", "cross_agent_communication"],
                "min_version": "1.0.0"
            }
        )

        # 创意策划智能体模型版本
        self.add_model_version(
            model_id="creative",
            version="1.0.0",
            name="deepseek-chat",
            description="创意策划智能体默认模型，专注于创意生成与方案设计",
            is_active=True,
            compatibility={
                "agents": ["creative"],
                "features": ["creative_generation", "scenario_design", "concept_development"],
                "min_version": "1.0.0"
            }
        )

        # 剧本创作智能体模型版本
        self.add_model_version(
            model_id="story_script",
            version="1.0.0",
            name="Qwen/Qwen3-30B-A3B-Instruct-2507",
            description="剧本创作智能体默认模型，负责剧本内容的创作与优化",
            is_active=True,
            compatibility={
                "agents": ["story_script"],
                "features": ["script_writing", "content_optimization", "story_development"],
                "min_version": "1.0.0"
            }
        )

    def add_model_version(self,
                         model_id: str,
                         version: str,
                         name: str,
                         description: str = "",
                         is_active: bool = False,
                         compatibility: Dict[str, Any] = None) -> bool:
        """添加模型版本"""
        if model_id not in self.model_versions:
            self.model_versions[model_id] = []

        # 检查版本是否已存在
        for existing_version in self.model_versions[model_id]:
            if existing_version.version == version:
                print(f"模型版本已存在: {model_id}-{version}")
                return False

        # 创建新版本
        new_version = ModelVersion(
            model_id=model_id,
            version=version,
            name=name,
            description=description,
            is_active=is_active,
            compatibility=compatibility
        )

        self.model_versions[model_id].append(new_version)

        # 如果设置为活跃，则将其他版本设置为非活跃
        if is_active:
            for version in self.model_versions[model_id]:
                if version != new_version:
                    version.is_active = False

        # 记录版本历史
        self.version_history.append({
            "action": "add",
            "model_id": model_id,
            "version": version,
            "name": name,
            "timestamp": datetime.now().isoformat()
        })

        # 保存版本
        self._save_versions()
        print(f"模型版本已添加: {model_id}-{version} ({name})")
        return True

    def switch_model_version(self, model_id: str, version: str) -> bool:
        """切换模型版本"""
        if model_id not in self.model_versions:
            print(f"模型不存在: {model_id}")
            return False

        # 找到目标版本
        target_version = None
        for v in self.model_versions[model_id]:
            if v.version == version:
                target_version = v
                break

        if not target_version:
            print(f"模型版本不存在: {model_id}-{version}")
            return False

        # 检查兼容性
        if not self._check_compatibility(target_version):
            print(f"模型版本不兼容: {model_id}-{version}")
            return False

        # 切换版本
        for v in self.model_versions[model_id]:
            v.is_active = (v == target_version)

        # 更新最后使用时间
        target_version.update_last_used()

        # 记录版本历史
        self.version_history.append({
            "action": "switch",
            "model_id": model_id,
            "version": version,
            "name": target_version.name,
            "timestamp": datetime.now().isoformat()
        })

        # 保存版本
        self._save_versions()
        print(f"模型版本已切换: {model_id}-{version} ({target_version.name})")
        return True

    def rollback_model_version(self, model_id: str) -> bool:
        """回滚模型版本"""
        if model_id not in self.model_versions:
            print(f"模型不存在: {model_id}")
            return False

        versions = self.model_versions[model_id]
        if len(versions) < 2:
            print(f"没有可回滚的版本: {model_id}")
            return False

        # 找到当前活跃版本
        current_active = None
        for v in versions:
            if v.is_active:
                current_active = v
                break

        if not current_active:
            print(f"没有活跃版本: {model_id}")
            return False

        # 找到上一个版本
        # 按创建时间排序
        sorted_versions = sorted(versions, key=lambda x: x.created_at, reverse=True)
        previous_version = None
        for v in sorted_versions:
            if v != current_active:
                previous_version = v
                break

        if not previous_version:
            print(f"没有可回滚的版本: {model_id}")
            return False

        # 切换到上一个版本
        return self.switch_model_version(model_id, previous_version.version)

    def _check_compatibility(self, version: ModelVersion) -> bool:
        """检查模型版本兼容性"""
        # 这里可以添加更复杂的兼容性检查逻辑
        # 例如检查模型是否支持所需的功能，是否与当前系统版本兼容等
        compatibility = version.compatibility
        
        # 检查最小系统版本
        min_version = compatibility.get("min_version", "1.0.0")
        # 假设当前系统版本为1.0.0
        current_version = "1.0.0"
        
        # 简单的版本比较
        def version_to_tuple(v):
            return tuple(map(int, v.split(".")))
        
        if version_to_tuple(current_version) < version_to_tuple(min_version):
            print(f"系统版本不兼容，需要至少 {min_version}")
            return False

        return True

    def get_active_version(self, model_id: str) -> Optional[ModelVersion]:
        """获取活跃版本"""
        if model_id not in self.model_versions:
            return None

        for version in self.model_versions[model_id]:
            if version.is_active:
                return version

        return None

    def get_all_versions(self, model_id: Optional[str] = None) -> Dict[str, List[ModelVersion]]:
        """获取所有版本"""
        if model_id:
            return {model_id: self.model_versions.get(model_id, [])}
        else:
            return self.model_versions

    def get_version_history(self) -> List[Dict[str, Any]]:
        """获取版本历史"""
        return self.version_history

    def get_model_name(self, model_id: str) -> str:
        """获取模型名称"""
        active_version = self.get_active_version(model_id)
        if active_version:
            return active_version.name
        else:
            # 返回默认模型名称
            default_models = {
                "coordination": "Qwen/Qwen3-235B-A22B-Instruct-2507",
                "creative": "deepseek-chat",
                "story_script": "Qwen/Qwen3-30B-A3B-Instruct-2507"
            }
            return default_models.get(model_id, "")

    def validate_model_compatibility(self, model_id: str, agent_type: str) -> bool:
        """验证模型与智能体的兼容性"""
        active_version = self.get_active_version(model_id)
        if not active_version:
            return False

        compatibility = active_version.compatibility
        supported_agents = compatibility.get("agents", [])
        return agent_type in supported_agents


# 创建全局模型版本管理器实例
model_version_manager = ModelVersionManager()
