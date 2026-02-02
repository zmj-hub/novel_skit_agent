import React, { useState, useEffect, useRef } from 'react';
import { Typography, Form, Input, Select, Button, message, Divider, Space, Card, Alert, Progress, Timeline, Table, Tag, notification } from 'antd';
import { 
  ScheduleOutlined, 
  RocketOutlined, 
  BookOutlined, 
  SettingOutlined, 
  LoadingOutlined, 
  CheckCircleOutlined, 
  CloseCircleOutlined, 
  TeamOutlined,
  BarChartOutlined,
  UserOutlined,
  SyncOutlined,
  WebSocketOutlined
} from '@ant-design/icons';
import Layout from '../../components/layout/Layout';
import Loading from '../../components/common/Loading';
import api from '../../services/api';
import endpoints from '../../services/endpoints';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;
const { Option } = Select;

interface ProgressUpdate {
  subtask_id: string;
  subtask_name: string;
  agent_name: string;
  progress: number;
  status: string;
  updated_at: string;
}

interface Allocation {
  subtask_id: string;
  subtask_name: string;
  agent_type: string;
  agent_name: string;
  estimated_duration: number;
  priority: number;
  allocated_at: string;
}

const Scheduler: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState<boolean>(false);
  const [showResult, setShowResult] = useState<boolean>(false);
  const [schedulerResult, setSchedulerResult] = useState<any>(null);
  const [progress, setProgress] = useState<number>(0);
  const [progressUpdates, setProgressUpdates] = useState<ProgressUpdate[]>([]);
  const [allocations, setAllocations] = useState<Allocation[]>([]);
  
  // WebSocket相关状态
  const [websocket, setWebsocket] = useState<WebSocket | null>(null);
  const [wsConnected, setWsConnected] = useState<boolean>(false);
  const [wsError, setWsError] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const sessionIdRef = useRef<string>('');

  // 故事类型选项
  const storyTypes = [
    { value: '科幻', label: '科幻' },
    { value: '悬疑', label: '悬疑' },
    { value: '爱情', label: '爱情' },
    { value: '奇幻', label: '奇幻' },
    { value: '历史', label: '历史' },
    { value: '都市', label: '都市' },
    { value: '武侠', label: '武侠' },
    { value: '恐怖', label: '恐怖' },
  ];

  // WebSocket连接函数
  const connectWebSocket = (sessionId: string) => {
    try {
      // 关闭现有连接
      if (wsRef.current) {
        wsRef.current.close();
      }

      // 构建WebSocket URL
      const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const wsUrl = `${wsProtocol}//${window.location.host}/api/scheduler/ws/${sessionId}`;

      // 创建新的WebSocket连接
      const ws = new WebSocket(wsUrl);
      
      // 保存到ref和state
      wsRef.current = ws;
      setWebsocket(ws);
      
      // 连接打开
      ws.onopen = () => {
        console.log('WebSocket连接已建立');
        setWsConnected(true);
        setWsError(null);
        notification.success({
          message: '实时连接已建立',
          description: '您将实时收到任务执行进度更新',
          icon: <WebSocketOutlined style={{ color: '#52c41a' }} />,
        });
      };
      
      // 接收消息
      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log('收到WebSocket消息:', data);
          
          // 处理进度更新
          handleProgressUpdate(data);
        } catch (error) {
          console.error('解析WebSocket消息失败:', error);
        }
      };
      
      // 连接错误
      ws.onerror = (error) => {
        console.error('WebSocket错误:', error);
        setWsError('WebSocket连接错误');
        notification.error({
          message: '实时连接错误',
          description: '无法建立实时连接，将使用轮询获取进度',
          icon: <CloseCircleOutlined style={{ color: '#ff4d4f' }} />,
        });
      };
      
      // 连接关闭
      ws.onclose = () => {
        console.log('WebSocket连接已关闭');
        setWsConnected(false);
        if (wsRef.current === ws) {
          wsRef.current = null;
          setWebsocket(null);
        }
      };
    } catch (error) {
      console.error('建立WebSocket连接失败:', error);
      setWsError('无法建立WebSocket连接');
      notification.error({
        message: '实时连接失败',
        description: '将使用轮询获取进度更新',
        icon: <CloseCircleOutlined style={{ color: '#ff4d4f' }} />,
      });
    }
  };

  // 处理进度更新
  const handleProgressUpdate = (progressData: any) => {
    // 更新整体进度
    if (progressData.overall_progress !== undefined) {
      setProgress(progressData.overall_progress);
    }
    
    // 更新进度更新列表
    if (progressData.updates && Array.isArray(progressData.updates)) {
      setProgressUpdates(progressData.updates);
    }
    
    // 更新状态
    if (progressData.status) {
      // 可以根据状态显示不同的通知
      switch (progressData.status) {
        case 'completed':
          notification.success({
            message: '任务完成',
            description: '所有任务已成功完成',
            icon: <CheckCircleOutlined style={{ color: '#52c41a' }} />,
          });
          break;
        case 'failed':
          notification.error({
            message: '任务失败',
            description: progressData.message || '任务执行失败',
            icon: <CloseCircleOutlined style={{ color: '#ff4d4f' }} />,
          });
          break;
        case 'running':
          // 可以显示正在执行的任务信息
          if (progressData.message) {
            notification.info({
              message: '任务执行中',
              description: progressData.message,
              icon: <SyncOutlined style={{ color: '#1890ff' }} />,
            });
          }
          break;
      }
    }
  };

  // 关闭WebSocket连接
  const disconnectWebSocket = () => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
      setWebsocket(null);
      setWsConnected(false);
    }
  };

  // 组件卸载时关闭WebSocket连接
  useEffect(() => {
    return () => {
      disconnectWebSocket();
    };
  }, []);

  // 处理表单提交
  const handleSubmit = async (values: any) => {
    setLoading(true);
    setShowResult(false);
    setProgress(0);

    // 保存会话ID到ref
    sessionIdRef.current = values.session_id;

    // 构建请求参数
    const requestData = {
      story_description: values.story_description,
      story_type: values.story_type,
      request_priority: values.request_priority,
      session_id: values.session_id,
      model: values.model
    };

    // 建立WebSocket连接
    connectWebSocket(values.session_id);

    // 模拟进度更新（仅作为备用）
    const progressInterval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(progressInterval);
          return 100;
        }
        return prev + 5;
      });
    }, 200);

    try {
      // 真实API调用
      const response = await api.post(endpoints.scheduler.schedule, requestData);
      
      // 确保响应数据包含必要的字段
      const result = {
        response: response.response || '故事创作任务调度成功',
        session_id: response.session_id || values.session_id,
        task_plan: response.task_plan || {
          story_type: values.story_type,
          plan: `为${values.story_type}故事创建完整的创作计划，包括创意构思、情节设计、人物塑造和结局安排`,
          estimated_duration: 120
        },
        task_breakdown: response.task_breakdown || {
          subtasks: []
        },
        agent_allocation: response.agent_allocation || {
          allocations: []
        },
        progress_tracking: response.progress_tracking || {
          progress_updates: [],
          overall_progress: 0
        },
        result_summary: response.result_summary || {
          overall_progress: 0,
          status: 'in_progress',
          completed_tasks: 0,
          total_tasks: 0,
          summary: '任务调度中',
          key_achievements: [],
          next_steps: []
        }
      };
      
      setSchedulerResult(result);
      setProgressUpdates(result.progress_tracking.progress_updates);
      setAllocations(result.agent_allocation.allocations);
      setShowResult(true);
      setProgress(100);
      message.success('故事创作任务调度成功！');
    } catch (error) {
      console.error('调度任务失败:', error);
      message.error('调度任务失败，请重试');
      // 模拟响应作为备用
      const mockResult = {
        response: '故事创作任务调度成功',
        session_id: values.session_id,
        task_plan: {
          story_type: values.story_type,
          plan: `为${values.story_type}故事创建完整的创作计划，包括创意构思、情节设计、人物塑造和结局安排`,
          estimated_duration: 120
        },
        task_breakdown: {
          subtasks: [
            {
              subtask_id: 'subtask_1',
              name: '创意构思与大纲设计',
              description: '根据故事类型和描述，设计故事大纲和整体结构',
              estimated_duration: 30,
              agent_type: 'creative',
              priority: 1
            },
            {
              subtask_id: 'subtask_2',
              name: '人物设定与关系构建',
              description: '设计主要人物及其关系网络',
              estimated_duration: 25,
              agent_type: 'creative',
              priority: 2
            },
            {
              subtask_id: 'subtask_3',
              name: '情节发展与冲突设计',
              description: '设计故事的情节发展和主要冲突',
              estimated_duration: 40,
              agent_type: 'creative',
              priority: 3
            },
            {
              subtask_id: 'subtask_4',
              name: '细节描写与场景渲染',
              description: '为故事添加细节描写和场景渲染',
              estimated_duration: 35,
              agent_type: 'script',
              priority: 4
            },
            {
              subtask_id: 'subtask_5',
              name: '结局设计与主题升华',
              description: '设计故事结局并升华主题',
              estimated_duration: 30,
              agent_type: 'script',
              priority: 5
            }
          ]
        },
        agent_allocation: {
          allocations: [
            {
              subtask_id: 'subtask_1',
              subtask_name: '创意构思与大纲设计',
              agent_type: 'creative',
              agent_name: '创意智能体',
              estimated_duration: 30,
              priority: 1
            },
            {
              subtask_id: 'subtask_2',
              subtask_name: '人物设定与关系构建',
              agent_type: 'creative',
              agent_name: '创意智能体',
              estimated_duration: 25,
              priority: 2
            },
            {
              subtask_id: 'subtask_3',
              subtask_name: '情节发展与冲突设计',
              agent_type: 'creative',
              agent_name: '创意智能体',
              estimated_duration: 40,
              priority: 3
            },
            {
              subtask_id: 'subtask_4',
              subtask_name: '细节描写与场景渲染',
              agent_type: 'script',
              agent_name: '剧本智能体',
              estimated_duration: 35,
              priority: 4
            },
            {
              subtask_id: 'subtask_5',
              subtask_name: '结局设计与主题升华',
              agent_type: 'script',
              agent_name: '剧本智能体',
              estimated_duration: 30,
              priority: 5
            }
          ]
        },
        progress_tracking: {
          progress_updates: [
            {
              subtask_id: 'subtask_1',
              subtask_name: '创意构思与大纲设计',
              agent_name: '创意智能体',
              progress: 100,
              status: 'completed'
            },
            {
              subtask_id: 'subtask_2',
              subtask_name: '人物设定与关系构建',
              agent_name: '创意智能体',
              progress: 100,
              status: 'completed'
            },
            {
              subtask_id: 'subtask_3',
              subtask_name: '情节发展与冲突设计',
              agent_name: '创意智能体',
              progress: 80,
              status: 'in_progress'
            },
            {
              subtask_id: 'subtask_4',
              subtask_name: '细节描写与场景渲染',
              agent_name: '剧本智能体',
              progress: 30,
              status: 'in_progress'
            },
            {
              subtask_id: 'subtask_5',
              subtask_name: '结局设计与主题升华',
              agent_name: '剧本智能体',
              progress: 0,
              status: 'pending'
            }
          ],
          overall_progress: 62
        },
        result_summary: {
          overall_progress: 62,
          status: 'in_progress',
          completed_tasks: 2,
          total_tasks: 5,
          summary: '任务已完成62%，共完成2个任务，总计5个任务',
          key_achievements: [
            '完成故事大纲设计',
            '构建主要人物关系',
            '设计核心情节冲突',
            '渲染关键场景细节'
          ],
          next_steps: [
            '完成剩余任务',
            '整合所有内容',
            '进行质量评估',
            '提交最终结果'
          ]
        }
      };
      
      setSchedulerResult(mockResult);
      setProgressUpdates(mockResult.progress_tracking.progress_updates);
      setAllocations(mockResult.agent_allocation.allocations);
      setShowResult(true);
      setProgress(100);
      message.success('故事创作任务调度成功（模拟数据）！');
    } finally {
      clearInterval(progressInterval);
      setProgress(100);
      setLoading(false);
    }
  };

  // 获取状态标签
  const getStatusTag = (status: string) => {
    switch (status) {
      case 'completed':
        return <Tag color="green">已完成</Tag>;
      case 'in_progress':
        return <Tag color="blue">进行中</Tag>;
      case 'pending':
        return <Tag color="orange">待开始</Tag>;
      default:
        return <Tag color="default">未知</Tag>;
    }
  };

  // 获取智能体类型标签
  const getAgentTypeTag = (agentType: string) => {
    switch (agentType) {
      case 'creative':
        return <Tag color="purple">创意智能体</Tag>;
      case 'script':
        return <Tag color="blue">剧本智能体</Tag>;
      default:
        return <Tag color="default">未知</Tag>;
    }
  };

  return (
    <Layout title="故事创作调度 - 小说创作助手">
      <div className="scheduler-container space-y-8">
        {/* 页面标题 */}
        <div className="animate-fade-in">
          <div className="flex items-center space-x-3 mb-2">
            <ScheduleOutlined className="text-indigo-600 animate-pulse" style={{ fontSize: '24px' }} />
            <Title level={2} className="text-gray-800 mb-0">故事创作调度</Title>
          </div>
          <Text type="secondary">智能协调系统，为您的故事创作任务提供高效的智能体协作方案</Text>
        </div>

        {/* 调度表单 */}
        <Card
          title={
            <Space>
              <RocketOutlined />
              <span>故事创作计划</span>
            </Space>
          }
          variant="borderless"
          className="shadow-md rounded-lg overflow-hidden transition-all duration-300 hover:shadow-lg hover:-translate-y-1"
          style={{ 
            background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(249,250,251,0.95) 100%)',
            boxShadow: '0 4px 20px rgba(0,0,0,0.08)'
          }}
        >
          <Form
            form={form}
            onFinish={handleSubmit}
            layout="vertical"
            initialValues={{
              story_description: '一个关于人工智能与人类情感的科幻故事，讲述了一个AI助手与它的主人之间逐渐发展的情感纽带，以及他们共同面对的挑战',
              story_type: '科幻',
              request_priority: 3,
              model: 'qwen3-30b',
              session_id: `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            }}
            className="space-y-6"
          >
            {/* 故事描述 */}
            <Form.Item
              name="story_description"
              label={
                <Space>
                  <BookOutlined />
                  <span>故事详细描述</span>
                </Space>
              }
              rules={[{ required: true, message: '请输入故事详细描述' }]}
              className="mb-6"
            >
              <TextArea
                placeholder="请详细描述您想要创作的故事内容"
                rows={6}
                className="rounded-lg border-gray-300 focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 transition-all"
              />
              <Text type="secondary" className="block mt-2">详细的描述将帮助智能体更好地理解您的创作意图</Text>
            </Form.Item>

            {/* 故事类型 */}
            <Form.Item
              name="story_type"
              label={
                <Space>
                  <BookOutlined />
                  <span>故事类型</span>
                </Space>
              }
              rules={[{ required: true, message: '请选择故事类型' }]}
              className="mb-6"
            >
              <Select 
                placeholder="请选择故事类型"
                className="rounded-lg border-gray-300"
                size="large"
              >
                {storyTypes.map(type => (
                  <Option key={type.value} value={type.value}>{type.label}</Option>
                ))}
              </Select>
            </Form.Item>

            {/* 调度参数 */}
            <div className="mb-6">
              <Title level={4} className="mb-4 text-gray-800">调度参数</Title>
              <Space orientation="vertical" className="w-full space-y-4">
                <Form.Item
                  name="model"
                  label={
                    <Space>
                      <SettingOutlined />
                      <span>模型选择</span>
                    </Space>
                  }
                >
                  <Select style={{ width: '100%' }} className="rounded-lg">
                    <Option value="qwen3-30b">Qwen3-30B</Option>
                    <Option value="deepseek-chat">DeepSeek Chat</Option>
                    <Option value="gpt-4">GPT-4</Option>
                  </Select>
                </Form.Item>

                <Form.Item
                  name="request_priority"
                  label="优先级"
                >
                  <Select style={{ width: '100%' }} className="rounded-lg">
                    <Option value={1}>低</Option>
                    <Option value={2}>中低</Option>
                    <Option value={3}>中</Option>
                    <Option value={4}>中高</Option>
                    <Option value={5}>高</Option>
                  </Select>
                </Form.Item>

                <Form.Item
                  name="session_id"
                  label="会话ID"
                >
                  <Input 
                    readOnly 
                    className="rounded-lg bg-gray-50"
                  />
                </Form.Item>
              </Space>
            </div>

            {/* 提交按钮 */}
            <Form.Item className="mt-8">
              <Button 
                type="primary" 
                htmlType="submit" 
                loading={loading}
                size="large"
                icon={<RocketOutlined />}
                className="w-full rounded-lg transition-all duration-300 hover:shadow-lg hover:scale-105 active:scale-95"
                style={{ 
                  background: 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)',
                  border: 'none',
                  height: '48px',
                  fontSize: '16px',
                  fontWeight: 500
                }}
              >
                开始调度
              </Button>
            </Form.Item>
          </Form>
        </Card>

        {/* 实时进度显示 */}
        {loading && (
          <Card
            title={
              <Space>
                <SyncOutlined className="text-indigo-600" />
                <span>实时调度进度</span>
                <Tag color={wsConnected ? 'green' : 'red'} size="small">
                  {wsConnected ? '实时连接' : '无实时连接'}
                </Tag>
              </Space>
            }
            variant="borderless"
            className="shadow-md rounded-lg overflow-hidden"
            style={{ 
              background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(249,250,251,0.95) 100%)',
              boxShadow: '0 4px 20px rgba(0,0,0,0.08)'
            }}
          >
            <div className="space-y-6">
              {/* 整体进度条 */}
              <div>
                <div className="flex justify-between items-center mb-2">
                  <Text strong>整体进度</Text>
                  <Text strong>{progress}%</Text>
                </div>
                <Progress 
                  percent={progress} 
                  status={progress >= 100 ? 'success' : 'active'}
                  className="rounded-full"
                  strokeColor={{
                    from: '#6366f1',
                    to: '#4f46e5',
                  }}
                  size="large"
                />
              </div>
              
              {/* 智能体状态卡片 */}
              <div>
                <Title level={5} className="text-gray-700 mb-4">智能体状态</Title>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {/* 创意智能体状态卡片 */}
                  <Card 
                    size="small" 
                    className="border border-gray-100 transition-all duration-300 hover:shadow-md hover:-translate-y-1 hover:border-purple-300"
                    style={{ borderRadius: '12px' }}
                  >
                    <div className="flex items-center space-x-3 mb-3">
                      <div className="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center">
                        <TeamOutlined className="text-purple-600" />
                      </div>
                      <div>
                        <Text strong>创意智能体</Text>
                        <div className="text-xs text-gray-500">负责创意构思与大纲设计</div>
                      </div>
                    </div>
                    <Progress percent={progress > 50 ? 100 : progress * 2} status="active" size="small" />
                    <Text className="text-xs text-gray-500 mt-2 block">
                      {progress < 25 ? '待开始' : progress < 50 ? '进行中' : '已完成'}
                    </Text>
                  </Card>
                  
                  {/* 剧本智能体状态卡片 */}
                  <Card 
                    size="small" 
                    className="border border-gray-100 transition-all duration-300 hover:shadow-md hover:-translate-y-1 hover:border-blue-300"
                    style={{ borderRadius: '12px' }}
                  >
                    <div className="flex items-center space-x-3 mb-3">
                      <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
                        <BookOutlined className="text-blue-600" />
                      </div>
                      <div>
                        <Text strong>剧本智能体</Text>
                        <div className="text-xs text-gray-500">负责细节描写与场景渲染</div>
                      </div>
                    </div>
                    <Progress percent={progress > 75 ? 100 : progress > 50 ? (progress - 50) * 4 : 0} status="active" size="small" />
                    <Text className="text-xs text-gray-500 mt-2 block">
                      {progress < 50 ? '待开始' : progress < 75 ? '进行中' : '已完成'}
                    </Text>
                  </Card>
                  
                  {/* 调度智能体状态卡片 */}
                  <Card 
                    size="small" 
                    className="border border-gray-100 transition-all duration-300 hover:shadow-md hover:-translate-y-1 hover:border-indigo-300"
                    style={{ borderRadius: '12px' }}
                  >
                    <div className="flex items-center space-x-3 mb-3">
                      <div className="w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center">
                        <ScheduleOutlined className="text-indigo-600" />
                      </div>
                      <div>
                        <Text strong>调度智能体</Text>
                        <div className="text-xs text-gray-500">负责任务协调与资源分配</div>
                      </div>
                    </div>
                    <Progress percent={progress} status="active" size="small" />
                    <Text className="text-xs text-gray-500 mt-2 block">
                      {progress < 100 ? '进行中' : '已完成'}
                    </Text>
                  </Card>
                </div>
              </div>
              
              {/* 任务时间线 */}
              <div>
                <Title level={5} className="text-gray-700 mb-4">任务执行时间线</Title>
                <Timeline items={[
                  {
                    children: <Text>开始处理调度请求</Text>,
                    status: progress > 0 ? 'success' : 'default',
                  },
                  {
                    children: <Text>执行任务规划</Text>,
                    status: progress > 20 ? 'success' : progress > 0 ? 'active' : 'default',
                  },
                  {
                    children: <Text>执行任务分解</Text>,
                    status: progress > 40 ? 'success' : progress > 20 ? 'active' : 'default',
                  },
                  {
                    children: <Text>执行智能体分配</Text>,
                    status: progress > 60 ? 'success' : progress > 40 ? 'active' : 'default',
                  },
                  {
                    children: <Text>执行工作流</Text>,
                    status: progress > 80 ? 'success' : progress > 60 ? 'active' : 'default',
                  },
                  {
                    children: <Text>生成执行报告</Text>,
                    status: progress > 90 ? 'success' : progress > 80 ? 'active' : 'default',
                  },
                  {
                    children: <Text>任务完成</Text>,
                    status: progress === 100 ? 'success' : progress > 90 ? 'active' : 'default',
                  },
                ]} />
              </div>
              
              {/* 状态信息 */}
              <div className="bg-gray-50 p-4 rounded-lg">
                <Text className="text-center block">
                  {progress < 20 && '正在初始化调度系统...'}
                  {progress >= 20 && progress < 40 && '正在规划故事创作任务...'}
                  {progress >= 40 && progress < 60 && '正在分解任务并分配智能体...'}
                  {progress >= 60 && progress < 80 && '正在执行工作流...'}
                  {progress >= 80 && progress < 100 && '正在生成执行报告...'}
                  {progress === 100 && '任务调度已完成！'}
                </Text>
              </div>
            </div>
          </Card>
        )}

        {/* 调度结果 */}
        {showResult && schedulerResult && (
          <>
            {/* 总体状态 */}
            <Card
              title={
                <Space>
                  <BarChartOutlined />
                  <span>调度结果</span>
                </Space>
              }
              variant="borderless"
              className="shadow-md rounded-lg overflow-hidden"
              style={{ 
                background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(249,250,251,0.95) 100%)',
                boxShadow: '0 4px 20px rgba(0,0,0,0.08)'
              }}
            >
              <div className="space-y-6 p-4">
                <Alert
                  message={`调度状态: ${schedulerResult.result_summary.status === 'completed' ? '已完成' : '进行中'}`}
                  type={schedulerResult.result_summary.status === 'completed' ? 'success' : 'info'}
                  showIcon
                  className="rounded-lg"
                />
                
                <Divider className="my-4" />
                
                {/* 任务概览 */}
                <div className="space-y-4">
                  <Title level={4} className="text-gray-800 mb-4">任务概览</Title>
                  <Space orientation="vertical" className="w-full">
                    <div className="flex justify-between items-center">
                      <Text strong className="text-gray-700">故事类型:</Text>
                      <Text className="text-gray-600">{schedulerResult.task_plan.story_type}</Text>
                    </div>
                    <div className="flex justify-between items-center">
                      <Text strong className="text-gray-700">总体进度:</Text>
                      <Text className="text-gray-600">{schedulerResult.progress_tracking.overall_progress}%</Text>
                    </div>
                    <div className="flex justify-between items-center">
                      <Text strong className="text-gray-700">已完成任务:</Text>
                      <Text className="text-gray-600">{schedulerResult.result_summary.completed_tasks}/{schedulerResult.result_summary.total_tasks}</Text>
                    </div>
                    <div className="flex justify-between items-center">
                      <Text strong className="text-gray-700">预计工作量:</Text>
                      <Text className="text-gray-600">{schedulerResult.task_plan.estimated_duration}分钟</Text>
                    </div>
                  </Space>
                </div>
                
                <Divider className="my-4" />
                
                {/* 智能体分配 */}
                <div className="space-y-4">
                  <Title level={4} className="text-gray-800 mb-4">智能体分配</Title>
                  <Table
                    dataSource={allocations}
                    columns={[
                      {
                        title: '任务ID',
                        dataIndex: 'subtask_id',
                        key: 'subtask_id',
                        width: 120,
                      },
                      {
                        title: '任务名称',
                        dataIndex: 'subtask_name',
                        key: 'subtask_name',
                        flex: 1,
                      },
                      {
                        title: '智能体',
                        dataIndex: 'agent_name',
                        key: 'agent_name',
                        width: 120,
                        render: (agent_name: string) => (
                          <Tag color={agent_name.includes('创意') ? 'purple' : 'blue'}>{agent_name}</Tag>
                        ),
                      },
                      {
                        title: '预计时长',
                        dataIndex: 'estimated_duration',
                        key: 'estimated_duration',
                        width: 100,
                        render: (duration: number) => `${duration}分钟`,
                      },
                      {
                        title: '优先级',
                        dataIndex: 'priority',
                        key: 'priority',
                        width: 80,
                        render: (priority: number) => (
                          <Tag color={priority >= 4 ? 'red' : priority >= 3 ? 'orange' : 'blue'}>
                            {priority}
                          </Tag>
                        ),
                      },
                    ]}
                    rowKey="subtask_id"
                    className="rounded-lg overflow-hidden"
                    size="middle"
                  />
                </div>
                
                <Divider className="my-4" />
                
                {/* 进度跟踪 */}
                <div className="space-y-4">
                  <Title level={4} className="text-gray-800 mb-4">进度跟踪</Title>
                  <Table
                    dataSource={progressUpdates}
                    columns={[
                      {
                        title: '任务名称',
                        dataIndex: 'subtask_name',
                        key: 'subtask_name',
                        flex: 1,
                      },
                      {
                        title: '智能体',
                        dataIndex: 'agent_name',
                        key: 'agent_name',
                        width: 120,
                      },
                      {
                        title: '进度',
                        dataIndex: 'progress',
                        key: 'progress',
                        width: 150,
                        render: (progress: number) => (
                          <Progress percent={progress} size="small" />
                        ),
                      },
                      {
                        title: '状态',
                        dataIndex: 'status',
                        key: 'status',
                        width: 100,
                        render: (status: string) => getStatusTag(status),
                      },
                    ]}
                    rowKey="subtask_id"
                    className="rounded-lg overflow-hidden"
                    size="middle"
                  />
                </div>
                
                <Divider className="my-4" />
                
                {/* 关键成果 */}
                <div className="space-y-4">
                  <Title level={4} className="text-gray-800 mb-4">关键成果</Title>
                  <div className="bg-indigo-50 rounded-lg p-4">
                    <Space orientation="vertical" className="w-full">
                      {schedulerResult.result_summary.key_achievements.map((achievement: string, index: number) => (
                        <div key={index} className="flex items-center space-x-2">
                          <CheckCircleOutlined className="text-green-500" />
                          <Text className="text-gray-700">{achievement}</Text>
                        </div>
                      ))}
                    </Space>
                  </div>
                </div>
                
                {/* 下一步 */}
                <div className="space-y-4">
                  <Title level={4} className="text-gray-800 mb-4">下一步</Title>
                  <div className="bg-blue-50 rounded-lg p-4">
                    <Space orientation="vertical" className="w-full">
                      {schedulerResult.result_summary.next_steps.map((step: string, index: number) => (
                        <div key={index} className="flex items-center space-x-2">
                          <RocketOutlined className="text-blue-500" />
                          <Text className="text-gray-700">{step}</Text>
                        </div>
                      ))}
                    </Space>
                  </div>
                </div>
              </div>
            </Card>
          </>
        )}
      </div>
    </Layout>
  );
};

export default Scheduler;