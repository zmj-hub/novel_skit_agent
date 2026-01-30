import React, { useState } from 'react';
import { Typography, Form, Input, Select, Button, message, Divider, Space, Card, Alert, Progress, Timeline, Table, Tag } from 'antd';
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
  UserOutlined
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

  // 处理表单提交
  const handleSubmit = async (values: any) => {
    setLoading(true);
    setShowResult(false);
    setProgress(0);

    // 构建请求参数
    const requestData = {
      story_description: values.story_description,
      story_type: values.story_type,
      request_priority: values.request_priority,
      session_id: values.session_id,
      model: values.model
    };

    // 模拟进度更新
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
        <div>
          <div className="flex items-center space-x-3 mb-2">
            <ScheduleOutlined className="text-indigo-600" style={{ fontSize: '24px' }} />
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
          className="shadow-md rounded-lg overflow-hidden"
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
                className="w-full rounded-lg"
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

        {/* 进度显示 */}
        {loading && (
          <Card
            title="调度进度"
            variant="borderless"
            className="shadow-md rounded-lg overflow-hidden"
          >
            <div className="space-y-4">
              <Progress 
                percent={progress} 
                status="active"
                className="rounded-full"
                strokeColor={{
                  from: '#6366f1',
                  to: '#4f46e5',
                }}
              />
              <Text className="text-center block">正在调度故事创作任务，请稍候...</Text>
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