import React, { useState, useEffect, useRef, useCallback } from 'react';
import TaskProgress from './TaskProgress';

interface WebSocketProgressProps {
  sessionId: string;
  taskId?: string;
}

interface TaskData {
  task_id: string;
  session_id: string;
  story_type: string;
  status: string;
  progress: number;
  current_step: string;
  completed_steps: number;
  total_steps: number;
  step_progress: any[];
  start_time: string;
  end_time?: string;
  estimated_end_time?: string;
  updated_at: string;
}

const WebSocketProgress: React.FC<WebSocketProgressProps> = ({ sessionId, taskId }) => {
  const [tasks, setTasks] = useState<TaskData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);

  // 初始化WebSocket连接
  useEffect(() => {
    const wsUrl = `ws://localhost:8000/api/scheduler/ws/${sessionId}`;
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      console.log('WebSocket连接已建立');
      setLoading(false);
      // 发送获取任务请求
      if (taskId) {
        ws.send(`get_task:${taskId}`);
      } else {
        ws.send('get_tasks');
      }
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('收到WebSocket消息:', data);

        if (data.type === 'tasks') {
          setTasks(data.tasks);
        } else if (data.type === 'task') {
          setTasks([data.task]);
        } else if (data.type === 'error') {
          setError(data.message);
        }
      } catch (err) {
        console.error('解析WebSocket消息失败:', err);
      }
    };

    ws.onclose = () => {
      console.log('WebSocket连接已关闭');
    };

    ws.onerror = (err) => {
      console.error('WebSocket错误:', err);
      setError('WebSocket连接失败');
      setLoading(false);
    };

    wsRef.current = ws;

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [sessionId, taskId]);

  // 刷新任务列表
  const refreshTasks = useCallback(() => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      if (taskId) {
        wsRef.current.send(`get_task:${taskId}`);
      } else {
        wsRef.current.send('get_tasks');
      }
    }
  }, [sessionId, taskId]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-gray-500">加载中...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-red-500">{error}</div>
      </div>
    );
  }

  return (
    <div className="w-full">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-gray-800">实时任务进度</h2>
        <button
          className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
          onClick={refreshTasks}
        >
          刷新
        </button>
      </div>

      {tasks.length === 0 ? (
        <div className="text-center text-gray-500 py-8">
          暂无任务
        </div>
      ) : (
        tasks.map((task) => (
          <TaskProgress
            key={task.task_id}
            taskId={task.task_id}
            sessionId={task.session_id}
            storyType={task.story_type}
            status={task.status}
            progress={task.progress}
            currentStep={task.current_step}
            completedSteps={task.completed_steps}
            totalSteps={task.total_steps}
            steps={task.step_progress}
            createdAt={task.start_time}
            updatedAt={task.updated_at}
          />
        ))
      )}
    </div>
  );
};

export default WebSocketProgress;