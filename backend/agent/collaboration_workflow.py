from langgraph.graph import StateGraph, END
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid
import asyncio

from agent.agent_collaboration import (
    CollaborationState, WorkflowState, AgentType, ExecutionStatus,
    ExecutionStep, ReflectionRecord
)
from agent.creative_agent import CreativePlanningAgent
from agent.story_script_agent import StoryScriptAgent
from agent.coordination_agent import CoordinationAgent
from core.config import settings
from core.agent_config import AgentType as ConfigAgentType, get_agent_model


async def planning_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    规划节点：分析任务目标并生成执行计划
    """
    print("=== 规划阶段开始 ===")
    
    # 从状态中获取协作状态
    collaboration_state = CollaborationState.from_dict(state)
    
    # 更新工作流状态为规划中
    collaboration_state.workflow_state = WorkflowState.PLANNING
    collaboration_state.updated_at = datetime.now()
    
    try:
        # 分析任务目标，确定需要使用的智能体
        task_goal = collaboration_state.task_goal
        print(f"任务目标: {task_goal}")
        
        # 获取请求参数
        request_params = getattr(collaboration_state, 'request_params', {})
        print(f"请求参数: {request_params}")
        
        # 生成执行计划
        current_plan = []
        
        # 根据任务目标分析需要的步骤
        if "创意" in task_goal or "故事" in task_goal:
            current_plan.append({
                "step_id": f"step_{uuid.uuid4().hex[:8]}",
                "agent_type": AgentType.CREATIVE.value,
                "task": "生成故事创意框架",
                "parameters": {
                    "hotspots": ["人工智能", "职场压力", "都市情感"],
                    "story_type": "都市情感"
                },
                "dependencies": []
            })
        
        if "故事" in task_goal or "剧本" in task_goal or "写作" in task_goal:
            current_plan.append({
                "step_id": f"step_{uuid.uuid4().hex[:8]}",
                "agent_type": AgentType.STORY_SCRIPT.value,
                "task": "创作故事剧本",
                "parameters": {
                    "style": "urban",
                    "medium_type": "novel",
                    "chapter_count": 5
                },
                "dependencies": [p["step_id"] for p in current_plan if p["agent_type"] == AgentType.CREATIVE.value]
            })
        
        if "协调" in task_goal or "调度" in task_goal or "工作流" in task_goal:
            current_plan.append({
                "step_id": f"step_{uuid.uuid4().hex[:8]}",
                "agent_type": AgentType.SCHEDULER.value,
                "task": "协调智能体工作流",
                "parameters": {
                    "request_priority": 3
                },
                "dependencies": []
            })
        
        # 如果没有生成计划，根据任务目标生成默认计划
        if not current_plan:
            creative_step_id = f"step_{uuid.uuid4().hex[:8]}"
            current_plan = [
                {
                    "step_id": creative_step_id,
                    "agent_type": AgentType.CREATIVE.value,
                    "task": "生成故事创意框架",
                    "parameters": {
                        "hotspots": ["人工智能", "职场压力", "都市情感"],
                        "story_type": "都市情感"
                    },
                    "dependencies": []
                },
                {
                    "step_id": f"step_{uuid.uuid4().hex[:8]}",
                    "agent_type": AgentType.STORY_SCRIPT.value,
                    "task": "创作故事剧本",
                    "parameters": {
                        "style": "urban",
                        "medium_type": "novel",
                        "chapter_count": 5
                    },
                    "dependencies": [creative_step_id]
                }
            ]
        
        # 更新当前计划
        collaboration_state.current_plan = current_plan
        print(f"生成的执行计划: {current_plan}")
        
        # 更新工作流状态为执行中
        collaboration_state.workflow_state = WorkflowState.EXECUTING
        collaboration_state.updated_at = datetime.now()
        
    except Exception as e:
        print(f"规划阶段错误: {e}")
        collaboration_state.workflow_state = WorkflowState.ERROR
        collaboration_state.error_records.append({
            "error_id": f"error_{uuid.uuid4().hex[:8]}",
            "phase": "planning",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        })
        collaboration_state.updated_at = datetime.now()
    
    print("=== 规划阶段结束 ===")
    return collaboration_state.to_dict()


async def execution_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行节点：调用相应智能体完成具体操作
    """
    print("=== 执行阶段开始 ===")
    
    # 从状态中获取协作状态
    collaboration_state = CollaborationState.from_dict(state)
    
    # 更新工作流状态为执行中
    collaboration_state.workflow_state = WorkflowState.EXECUTING
    collaboration_state.updated_at = datetime.now()
    
    try:
        # 遍历执行计划中的每个步骤
        for plan_step in collaboration_state.current_plan:
            step_id = plan_step["step_id"]
            agent_type = plan_step["agent_type"]
            task = plan_step["task"]
            parameters = plan_step["parameters"]
            dependencies = plan_step["dependencies"]
            
            # 检查依赖是否已完成
            all_dependencies_completed = all(
                any(
                    exec_step.step_id == dep and exec_step.status == ExecutionStatus.SUCCESS
                    for exec_step in collaboration_state.execution_history
                )
                for dep in dependencies
            )
            
            if not all_dependencies_completed:
                print(f"步骤 {step_id} 的依赖未完成，跳过执行")
                continue
            
            # 检查是否已经执行过
            if any(exec_step.step_id == step_id for exec_step in collaboration_state.execution_history):
                print(f"步骤 {step_id} 已经执行过，跳过执行")
                continue
            
            print(f"执行步骤: {step_id}, 智能体: {agent_type}, 任务: {task}")
            
            # 创建执行步骤记录
            execution_step = ExecutionStep(
                step_id=step_id,
                agent_type=AgentType(agent_type),
                task=task,
                parameters=parameters,
                status=ExecutionStatus.RUNNING,
                start_time=datetime.now()
            )
            collaboration_state.execution_history.append(execution_step)
            collaboration_state.updated_at = datetime.now()
            
            # 更新智能体状态
            if agent_type in collaboration_state.agent_states:
                agent_state = collaboration_state.agent_states[agent_type]
                agent_state.is_available = False
                agent_state.current_task = task
                agent_state.updated_at = datetime.now()
            
            # 执行具体任务
            result = None
            error = None
            
            try:
                # 根据智能体类型调用相应的智能体
                if agent_type == AgentType.CREATIVE.value:
                    # 创意策划智能体
                    # 从请求参数中获取模型配置
                    request_params = getattr(collaboration_state, 'request_params', {})
                    model = request_params.get("models", {}).get("creative", get_agent_model(ConfigAgentType.CREATIVE))
                    agent = CreativePlanningAgent(model)
                    if task == "生成故事创意框架":
                        result = await agent.process_creative_request(
                            hotspots=parameters.get("hotspots", []),
                            story_type=parameters.get("story_type", "都市情感")
                        )
                
                elif agent_type == AgentType.STORY_SCRIPT.value:
                    # 故事剧本一体化智能体
                    # 从请求参数中获取模型配置
                    request_params = getattr(collaboration_state, 'request_params', {})
                    model = request_params.get("models", {}).get("story_script", get_agent_model(ConfigAgentType.STORY_SCRIPT))
                    agent = StoryScriptAgent(model)
                    if task == "创作故事剧本":
                        # 获取创意框架
                        creative_framework = ""
                        for exec_step in collaboration_state.execution_history:
                            if exec_step.agent_type == AgentType.CREATIVE and exec_step.status == ExecutionStatus.SUCCESS:
                                creative_framework = exec_step.result.get("creative_document", {}).get("document", "")
                                break
                        
                        if creative_framework:
                            # 获取请求参数
                            request_params = getattr(collaboration_state, 'request_params', {})
                            style = parameters.get("style", request_params.get("writing_style", "urban"))
                            medium_type = parameters.get("medium_type", request_params.get("medium_type", "novel"))
                            chapter_count = parameters.get("chapter_count", request_params.get("chapter_count", 5))
                            
                            result = await agent.process_story_request(
                                creative_framework=creative_framework,
                                style=style,
                                medium_type=medium_type,
                                chapter_count=chapter_count
                            )
                        else:
                            error = "没有找到创意框架"
                
                elif agent_type == AgentType.SCHEDULER.value:
                    # 协调智能体
                    # 从请求参数中获取模型配置
                    request_params = getattr(collaboration_state, 'request_params', {})
                    model = request_params.get("models", {}).get("coordination", get_agent_model(ConfigAgentType.COORDINATION))
                    agent = CoordinationAgent(model)
                    if task == "协调智能体工作流":
                        result = await agent.process_coordination_request(
                            task_goal=collaboration_state.task_goal,
                            request_priority=parameters.get("request_priority", 1)
                        )
                
                # 更新执行步骤状态为成功
                execution_step.status = ExecutionStatus.SUCCESS
                execution_step.result = result
                execution_step.end_time = datetime.now()
                
                print(f"步骤 {step_id} 执行成功")
                
            except asyncio.TimeoutError:
                # 处理超时
                error = "执行超时"
                execution_step.status = ExecutionStatus.TIMED_OUT
                execution_step.error = error
                execution_step.end_time = datetime.now()
                print(f"步骤 {step_id} 执行超时")
                
            except Exception as e:
                # 处理其他错误
                error = str(e)
                execution_step.status = ExecutionStatus.FAILED
                execution_step.error = error
                execution_step.end_time = datetime.now()
                print(f"步骤 {step_id} 执行失败: {error}")
            
            # 更新智能体状态
            if agent_type in collaboration_state.agent_states:
                agent_state = collaboration_state.agent_states[agent_type]
                agent_state.is_available = True
                agent_state.current_task = None
                agent_state.last_execution = datetime.now()
                if error:
                    agent_state.error = error
                else:
                    agent_state.error = None
            
            # 更新协作状态
            collaboration_state.updated_at = datetime.now()
        
        # 更新工作流状态为反思中
        collaboration_state.workflow_state = WorkflowState.REFLECTING
        collaboration_state.updated_at = datetime.now()
        
    except Exception as e:
        print(f"执行阶段错误: {e}")
        collaboration_state.workflow_state = WorkflowState.ERROR
        collaboration_state.error_records.append({
            "error_id": f"error_{uuid.uuid4().hex[:8]}",
            "phase": "execution",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        })
        collaboration_state.updated_at = datetime.now()
    
    print("=== 执行阶段结束 ===")
    return collaboration_state.to_dict()


async def reflection_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    反思节点：评估执行结果并决定是否需要调整计划
    """
    print("=== 反思阶段开始 ===")
    
    # 从状态中获取协作状态
    collaboration_state = CollaborationState.from_dict(state)
    
    # 更新工作流状态为反思中
    collaboration_state.workflow_state = WorkflowState.REFLECTING
    collaboration_state.updated_at = datetime.now()
    
    try:
        # 分析执行历史
        execution_history = collaboration_state.execution_history
        successful_steps = [step for step in execution_history if step.status == ExecutionStatus.SUCCESS]
        failed_steps = [step for step in execution_history if step.status == ExecutionStatus.FAILED]
        timed_out_steps = [step for step in execution_history if step.status == ExecutionStatus.TIMED_OUT]
        
        print(f"成功步骤: {len(successful_steps)}")
        print(f"失败步骤: {len(failed_steps)}")
        print(f"超时步骤: {len(timed_out_steps)}")
        
        # 生成反思记录
        reflection_id = f"reflection_{uuid.uuid4().hex[:8]}"
        evaluation = ""
        adjustment_needed = False
        adjustment_reason = ""
        new_plan = []
        
        if len(failed_steps) > 0 or len(timed_out_steps) > 0:
            # 如果有失败或超时的步骤，需要调整计划
            adjustment_needed = True
            adjustment_reason = f"有 {len(failed_steps)} 个步骤失败，{len(timed_out_steps)} 个步骤超时"
            
            evaluation = f"执行过程中出现问题：\n"
            evaluation += f"- 成功执行 {len(successful_steps)} 个步骤\n"
            evaluation += f"- 失败 {len(failed_steps)} 个步骤\n"
            evaluation += f"- 超时 {len(timed_out_steps)} 个步骤\n"
            
            # 生成新的执行计划，重新执行失败的步骤
            for failed_step in failed_steps:
                new_plan.append({
                    "step_id": f"step_{uuid.uuid4().hex[:8]}",
                    "agent_type": failed_step.agent_type.value,
                    "task": failed_step.task,
                    "parameters": failed_step.parameters,
                    "dependencies": []
                })
            
            for timed_out_step in timed_out_steps:
                new_plan.append({
                    "step_id": f"step_{uuid.uuid4().hex[:8]}",
                    "agent_type": timed_out_step.agent_type.value,
                    "task": timed_out_step.task,
                    "parameters": timed_out_step.parameters,
                    "dependencies": []
                })
        
        else:
            # 如果所有步骤都成功执行，评估任务是否完成
            task_goal = collaboration_state.task_goal
            evaluation = f"所有步骤都成功执行完成。\n"
            evaluation += f"任务目标: {task_goal}\n"
            evaluation += f"成功执行 {len(successful_steps)} 个步骤\n"
            
            # 检查是否完成了所有必要的步骤
            if all(
                any(
                    exec_step.agent_type.value == required_agent
                    for exec_step in successful_steps
                )
                for required_agent in [AgentType.CREATIVE.value, AgentType.NOVEL.value, AgentType.STORY_SCRIPT.value]
                if required_agent in [step["agent_type"] for step in collaboration_state.current_plan]
            ):
                # 任务完成
                adjustment_needed = False
                collaboration_state.workflow_state = WorkflowState.COMPLETED
                print("任务完成！")
            else:
                # 任务未完成，需要调整计划
                adjustment_needed = True
                adjustment_reason = "任务目标未完全实现，需要执行更多步骤"
                
                # 生成新的执行计划
                # 这里可以根据任务目标和已执行的步骤，生成更详细的新计划
        
        # 创建反思记录
        reflection_record = ReflectionRecord(
            reflection_id=reflection_id,
            execution_history=execution_history,
            evaluation=evaluation,
            adjustment_needed=adjustment_needed,
            adjustment_reason=adjustment_reason,
            new_plan=new_plan
        )
        
        # 添加反思记录
        collaboration_state.reflection_records.append(reflection_record)
        
        # 如果需要调整计划，更新当前计划
        if adjustment_needed:
            collaboration_state.current_plan = new_plan
            collaboration_state.workflow_state = WorkflowState.PLANNING
            print(f"生成新的执行计划: {new_plan}")
        
        collaboration_state.updated_at = datetime.now()
        
    except Exception as e:
        print(f"反思阶段错误: {e}")
        collaboration_state.workflow_state = WorkflowState.ERROR
        collaboration_state.error_records.append({
            "error_id": f"error_{uuid.uuid4().hex[:8]}",
            "phase": "reflection",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        })
        collaboration_state.updated_at = datetime.now()
    
    print("=== 反思阶段结束 ===")
    return collaboration_state.to_dict()


async def error_handling_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    错误处理节点：处理执行过程中的错误
    """
    print("=== 错误处理阶段开始 ===")
    
    # 从状态中获取协作状态
    collaboration_state = CollaborationState.from_dict(state)
    
    # 处理错误记录
    if collaboration_state.error_records:
        latest_error = collaboration_state.error_records[-1]
        print(f"处理错误: {latest_error['message']}")
        
        # 这里可以添加更详细的错误处理逻辑
        # 例如：重试失败的操作、通知用户、记录错误日志等
    
    # 更新工作流状态为反思中
    collaboration_state.workflow_state = WorkflowState.REFLECTING
    collaboration_state.updated_at = datetime.now()
    
    print("=== 错误处理阶段结束 ===")
    return collaboration_state.to_dict()


async def timeout_control_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    超时控制节点：控制智能体执行的超时时间
    """
    print("=== 超时控制阶段开始 ===")
    
    # 从状态中获取协作状态
    collaboration_state = CollaborationState.from_dict(state)
    
    # 处理超时的执行步骤
    for exec_step in collaboration_state.execution_history:
        if exec_step.status == ExecutionStatus.RUNNING:
            # 检查是否超时（默认300秒）
            if exec_step.start_time:
                elapsed_time = (datetime.now() - exec_step.start_time).total_seconds()
                if elapsed_time > 300:
                    exec_step.status = ExecutionStatus.TIMED_OUT
                    exec_step.error = "执行超时"
                    exec_step.end_time = datetime.now()
                    print(f"步骤 {exec_step.step_id} 执行超时")
    
    # 更新工作流状态为反思中
    collaboration_state.workflow_state = WorkflowState.REFLECTING
    collaboration_state.updated_at = datetime.now()
    
    print("=== 超时控制阶段结束 ===")
    return collaboration_state.to_dict()


def create_collaboration_workflow():
    """
    创建智能体协作工作流
    """
    # 创建StateGraph
    workflow = StateGraph(dict)
    
    # 添加节点
    workflow.add_node("planning", planning_node)
    workflow.add_node("execution", execution_node)
    workflow.add_node("reflection", reflection_node)
    workflow.add_node("error_handling", error_handling_node)
    workflow.add_node("timeout_control", timeout_control_node)
    
    # 添加边
    workflow.set_entry_point("planning")
    
    # 规划 → 执行
    workflow.add_edge("planning", "execution")
    
    # 执行 → 反思
    workflow.add_edge("execution", "reflection")
    
    # 反思 → 规划：如果需要调整计划
    def should_adjust_plan(state: Dict[str, Any]) -> str:
        collaboration_state = CollaborationState.from_dict(state)
        if collaboration_state.workflow_state == WorkflowState.PLANNING:
            return "planning"
        elif collaboration_state.workflow_state == WorkflowState.COMPLETED:
            return END
        else:
            return "reflection"
    
    workflow.add_conditional_edges(
        "reflection",
        should_adjust_plan,
        {
            "planning": "planning",
            END: END,
            "reflection": "reflection"
        }
    )
    
    # 执行 → 错误处理：如果执行过程中出现错误
    def should_handle_error(state: Dict[str, Any]) -> str:
        collaboration_state = CollaborationState.from_dict(state)
        if collaboration_state.workflow_state == WorkflowState.ERROR:
            return "error_handling"
        else:
            return "reflection"
    
    workflow.add_conditional_edges(
        "execution",
        should_handle_error,
        {
            "error_handling": "error_handling",
            "reflection": "reflection"
        }
    )
    
    # 错误处理 → 反思
    workflow.add_edge("error_handling", "reflection")
    
    # 执行 → 超时控制：如果执行超时
    def should_handle_timeout(state: Dict[str, Any]) -> str:
        collaboration_state = CollaborationState.from_dict(state)
        # 检查是否有运行中的步骤超时
        for exec_step in collaboration_state.execution_history:
            if exec_step.status == ExecutionStatus.RUNNING:
                if exec_step.start_time:
                    elapsed_time = (datetime.now() - exec_step.start_time).total_seconds()
                    if elapsed_time > 300:
                        return "timeout_control"
        return "reflection"
    
    workflow.add_conditional_edges(
        "execution",
        should_handle_timeout,
        {
            "timeout_control": "timeout_control",
            "reflection": "reflection"
        }
    )
    
    # 超时控制 → 反思
    workflow.add_edge("timeout_control", "reflection")
    
    # 编译工作流
    compiled_workflow = workflow.compile()
    return compiled_workflow


# 创建智能体协作工作流实例
collaboration_workflow = create_collaboration_workflow()
