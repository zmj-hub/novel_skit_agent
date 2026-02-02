import React from 'react';
import ProgressBar from './ProgressBar';

interface Step {
  step_id: string;
  step_name: string;
  status: string;
  progress: number;
  start_time: string;
  end_time?: string;
  estimated_end_time?: string;
}

interface TaskProgressProps {
  taskId: string;
  sessionId: string;
  storyType: string;
  status: string;
  progress: number;
  currentStep: string;
  completedSteps: number;
  totalSteps: number;
  steps: Step[];
  createdAt: string;
  updatedAt: string;
}

const TaskProgress: React.FC<TaskProgressProps> = ({
  taskId,
  sessionId,
  storyType,
  status,
  progress,
  currentStep,
  completedSteps,
  totalSteps,
  steps,
  createdAt,
  updatedAt,
}) => {
  // 根据状态获取状态文本和颜色
  const getStatusInfo = () => {
    switch (status) {
      case 'pending':
        return { text: '待处理', color: 'text-gray-500' };
      case 'running':
        return { text: '执行中', color: 'text-blue-500' };
      case 'completed':
        return { text: '已完成', color: 'text-green-500' };
      case 'failed':
        return { text: '失败', color: 'text-red-500' };
      case 'paused':
        return { text: '暂停', color: 'text-yellow-500' };
      default:
        return { text: '未知', color: 'text-gray-500' };
    }
  };

  const statusInfo = getStatusInfo();

  return (
    <div className="bg-white rounded-lg shadow-md p-4 mb-4">
      <div className="flex justify-between items-center mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-800">任务进度</h3>
          <p className="text-sm text-gray-500">
            任务ID: {taskId} | 会话ID: {sessionId} | 故事类型: {storyType}
          </p>
        </div>
        <div className="text-right">
          <p className={`text-sm font-medium ${statusInfo.color}`}>
            状态: {statusInfo.text}
          </p>
          <p className="text-xs text-gray-500">
            更新时间: {new Date(updatedAt).toLocaleString()}
          </p>
        </div>
      </div>

      <ProgressBar
        progress={progress}
        status={status as any}
        label="整体进度"
        height={12}
      />

      <div className="mt-4">
        <h4 className="text-sm font-medium text-gray-700 mb-2">当前步骤: {currentStep}</h4>
        <p className="text-sm text-gray-600">
          已完成 {completedSteps}/{totalSteps} 个步骤
        </p>
      </div>

      <div className="mt-4 border-t border-gray-100 pt-4">
        <h4 className="text-sm font-medium text-gray-700 mb-2">步骤详情</h4>
        {steps.map((step) => (
          <div key={step.step_id} className="mb-2">
            <ProgressBar
              progress={step.progress}
              status={step.status as any}
              label={step.step_name}
              height={6}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default TaskProgress;