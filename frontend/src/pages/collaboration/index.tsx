import React, { useState } from 'react';
import { Typography, Form, Input, Select, Button, message, Divider, Space, Card, Alert, Progress, Timeline, Table, Tag } from 'antd';
import { TeamOutlined, RocketOutlined, ClockCircleOutlined, SettingOutlined, CancelOutlined, CheckCircleOutlined, LoadingOutlined } from '@ant-design/icons';
import Layout from '../../components/layout/Layout';
import Loading from '../../components/common/Loading';
import api from '../../services/api';
import endpoints from '../../services/endpoints';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;

interface ExecutionStep {
  stepId: string;
  agentType: string;
  task: string;
  status: string;
  startTime: string;
  endTime: string | null;
  duration: string;
}

interface ReflectionRecord {
  id: string;
  content: string;
  timestamp: string;
}

const Collaboration: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState<boolean>(false);
  const [collaborationStatus, setCollaborationStatus] = useState<string>('idle');
  const [executionSteps, setExecutionSteps] = useState<ExecutionStep[]>([]);
  const [reflectionRecords, setReflectionRecords] = useState<ReflectionRecord[]>([]);
  const [progress, setProgress] = useState<number>(0);
  const [sessionId, setSessionId] = useState<string>('');
  const [taskGoal, setTaskGoal] = useState<string>('');
  const [showStatus, setShowStatus] = useState<boolean>(false);

  const handleCollaborate = async (values: any) => {
    setLoading(true);
    setCollaborationStatus('running');
    setProgress(0);
    setShowStatus(true);

    try {
      // 模拟API响应
      setTimeout(() => {
        const mockResponse = {
          session_id: values.session_id,
          task_goal: values.task_goal,
          workflow_state: 'completed',
          execution_history: [
            {
              stepId: '1',
              agentType: '策划助手',
              task: '分析任务目标，制定创作计划',
              status: 'completed',
              startTime: new Date().toISOString(),
              endTime: new Date(Date.now() + 1000 * 30).toISOString(),
              duration: '30秒'
            },
            {
              stepId: '2',
              agentType: '创作助手',
              task: '根据计划生成小说大纲',
              status: 'completed',
              startTime: new Date(Date.now() + 1000 * 30).toISOString(),
              endTime: new Date(Date.now() + 1000 * 60).toISOString(),
              duration: '30秒'
            },
            {
              stepId: '3',
              agentType: '编辑助手',
              task: '审核大纲并提供修改建议',
              status: 'completed',
              startTime: new Date(Date.now() + 1000 * 60).toISOString(),
              endTime: new Date(Date.now() + 1000 * 90).toISOString(),
              duration: '30秒'
            },
            {
              stepId: '4',
              agentType: '创作助手',
              task: '根据建议完成小说内容',
              status: 'completed',
              startTime: new Date(Date.now() + 1000 * 90).toISOString(),
              endTime: new Date(Date.now() + 1000 * 180).toISOString(),
              duration: '90秒'
            },
            {
              stepId: '5',
              agentType: '编辑助手',
              task: '最终审核并优化内容',
              status: 'completed',
              startTime: new Date(Date.now() + 1000 * 180).toISOString(),
              endTime: new Date(Date.now() + 1000 * 210).toISOString(),
              duration: '30秒'
            }
          ],
          reflection_records: [
            {
              id: '1',
              content: '任务目标明确，创作方向清晰，适合生成完整的小说内容',
              timestamp: new Date().toISOString()
            },
            {
              id: '2',
              content: '大纲结构合理，情节发展流畅，人物设定鲜明',
              timestamp: new Date(Date.now() + 1000 * 60).toISOString()
            },
            {
              id: '3',
              content: '小说内容符合设定风格，语言流畅，情感表达到位',
              timestamp: new Date(Date.now() + 1000 * 210).toISOString()
            }
          ]
        };

        setSessionId(mockResponse.session_id);
        setTaskGoal(mockResponse.task_goal);
        setCollaborationStatus(mockResponse.workflow_state);
        setExecutionSteps(mockResponse.execution_history);
        setReflectionRecords(mockResponse.reflection_records);
        setProgress(100);
        message.success('协作任务执行成功！');
        setLoading(false);
      }, 2000);

      // 真实API调用（注释掉）
      /*
      const response = await api.post(endpoints.collaboration.collaborate, {
        task_goal: values.task_goal,
        session_id: values.session_id,
        model: values.model,
        timeout: values.timeout,
        priority: values.priority,
        writing_style: values.writing_style,
        medium_type: values.medium_type,
        chapter_count: values.chapter_count,
      });

      setSessionId(response.session_id);
      setTaskGoal(response.task_goal);
      setCollaborationStatus(response.workflow_state);
      setExecutionSteps(response.execution_history || []);
      setReflectionRecords(response.reflection_records || []);
      setProgress(100);
      message.success('协作任务执行成功！');
      */
    } catch (error) {
      console.error('启动协作任务失败:', error);
      message.error('启动协作任务失败');
      setCollaborationStatus('failed');
      setLoading(false);
    }
  };

  const handleCancelCollaboration = async () => {
    if (!sessionId) {
      message.error('会话ID不能为空');
      return;
    }

    setLoading(true);

    try {
      // 模拟取消操作
      setTimeout(() => {
        setCollaborationStatus('cancelled');
        message.success('协作任务已成功取消！');
        setLoading(false);
      }, 1000);

      // 真实API调用（注释掉）
      /*
      const response = await api.post(endpoints.collaboration.cancel.replace('{session_id}', sessionId));
      setCollaborationStatus('cancelled');
      message.success('协作任务已成功取消！');
      */
    } catch (error) {
      console.error('取消协作任务失败:', error);
      message.error('取消协作任务失败');
      setLoading(false);
    }
  };

  const handleGetStatus = async () => {
    if (!sessionId) {
      message.error('会话ID不能为空');
      return;
    }

    setLoading(true);

    try {
      // 模拟获取状态
      setTimeout(() => {
        message.success('协作任务状态获取成功！');
        setLoading(false);
      }, 1000);

      // 真实API调用（注释掉）
      /*
      const response = await api.get(endpoints.collaboration.status.replace('{session_id}', sessionId));
      setCollaborationStatus(response.status);
      message.success('协作任务状态获取成功！');
      */
    } catch (error) {
      console.error('获取协作任务状态失败:', error);
      message.error('获取协作任务状态失败');
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'green';
      case 'running':
        return 'blue';
      case 'failed':
        return 'red';
      case 'cancelled':
        return 'orange';
      default:
        return 'default';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'completed':
        return '已完成';
      case 'running':
        return '运行中';
      case 'failed':
        return '失败';
      case 'cancelled':
        return '已取消';
      case 'idle':
        return '未开始';
      default:
        return status;
    }
  };

  return (
    <Layout title="智能协作 - 小说创作助手">
      <div className="space-y-8">
        {/* Collaboration Form */}
        <Card
          title={
            <Space>
              <TeamOutlined />
              <span>智能协作</span>
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
            onFinish={handleCollaborate}
            layout="vertical"
            initialValues={{
              task_goal: '生成一个关于人工智能的故事，并创作一部短篇小说',
              model: 'qwen3-30b',
              timeout: 300,
              priority: 3,
              writing_style: 'urban',
              medium_type: 'novel',
              chapter_count: 5,
              session_id: `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            }}
            className="space-y-6"
          >
            {/* Task Goal */}
            <Form.Item
              name="task_goal"
              label={
                <Space>
                  <RocketOutlined />
                  <span>任务目标</span>
                </Space>
              }
              rules={[{ required: true, message: '请输入任务目标' }]}
              className="mb-6"
            >
              <TextArea
                placeholder="请输入智能协作的任务目标"
                rows={4}
                className="rounded-lg border-gray-300 focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 transition-all"
              />
              <Text type="secondary" className="block mt-2">描述您希望智能助手协作完成的任务</Text>
            </Form.Item>

            {/* Collaboration Parameters */}
            <div className="mb-6">
              <Title level={4} className="mb-4 text-gray-800">协作参数</Title>
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
                  name="timeout"
                  label={
                    <Space>
                      <ClockCircleOutlined />
                      <span>超时时间（秒）</span>
                    </Space>
                  }
                >
                  <Input 
                    type="number" 
                    min={60} 
                    max={3600} 
                    placeholder="请输入超时时间（秒）" 
                    className="rounded-lg"
                  />
                </Form.Item>

                <Form.Item
                  name="priority"
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
                  name="writing_style"
                  label="写作风格"
                >
                  <Select style={{ width: '100%' }} className="rounded-lg">
                    <Option value="urban">都市</Option>
                    <Option value="sweet">甜蜜言情</Option>
                    <Option value="suspense">悬疑</Option>
                    <Option value="fantasy">奇幻</Option>
                    <Option value="historical">历史</Option>
                    <Option value="scifi">科幻</Option>
                  </Select>
                </Form.Item>

                <Form.Item
                  name="medium_type"
                  label="创作类型"
                >
                  <Select style={{ width: '100%' }} className="rounded-lg">
                    <Option value="novel">小说</Option>
                    <Option value="script">剧本</Option>
                    <Option value="dialogue">对话</Option>
                    <Option value="description">描写</Option>
                  </Select>
                </Form.Item>

                <Form.Item
                  name="chapter_count"
                  label="章节/场景数"
                >
                  <Input 
                    type="number" 
                    min={1} 
                    max={20} 
                    placeholder="请输入章节/场景数量" 
                    className="rounded-lg"
                  />
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

            {/* Action Buttons */}
            <Form.Item className="mt-8">
              <Space className="w-full">
                <Button 
                  type="primary" 
                  htmlType="submit" 
                  loading={loading}
                  size="large"
                  icon={<RocketOutlined />}
                  className="flex-1 rounded-lg"
                  style={{ 
                    background: 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)',
                    border: 'none',
                    height: '48px',
                    fontSize: '16px',
                    fontWeight: 500
                  }}
                >
                  开始协作
                </Button>
                {sessionId && (
                  <Button 
                    onClick={handleGetStatus}
                    className="rounded-lg"
                    style={{ height: '48px' }}
                  >
                    获取状态
                  </Button>
                )}
                {collaborationStatus === 'running' && (
                  <Button 
                    danger 
                    onClick={handleCancelCollaboration} 
                    icon={<CancelOutlined />}
                    className="rounded-lg"
                    style={{ height: '48px' }}
                  >
                    取消
                  </Button>
                )}
              </Space>
            </Form.Item>
          </Form>
        </Card>

        {/* Collaboration Status */}
        {showStatus && (
          <Card
            title={
              <Space>
                <TeamOutlined />
                <span>协作状态</span>
              </Space>
            }
            variant="borderless"
            className="shadow-md rounded-lg overflow-hidden"
            style={{ 
              background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(249,250,251,0.95) 100%)',
              boxShadow: '0 4px 20px rgba(0,0,0,0.08)'
            }}
          >
            {loading ? (
              <Loading message="正在启动协作任务..." />
            ) : (
              <div className="space-y-6 p-4">
                <Alert
                  message={`协作状态: ${getStatusText(collaborationStatus)}`}
                  type={getStatusColor(collaborationStatus) as any}
                  showIcon
                  className="rounded-lg"
                />
                <Divider className="my-4" />
                <Space className="w-full">
                  <Text strong className="text-gray-700">任务目标: </Text>
                  <Text className="flex-1 text-gray-600">{taskGoal || '未设置'}</Text>
                </Space>
                <Divider className="my-4" />
                <div className="mb-6">
                  <Text className="block mb-2 text-gray-700">执行进度</Text>
                  <Progress 
                    percent={progress} 
                    status={collaborationStatus === 'completed' ? 'success' : collaborationStatus === 'failed' ? 'exception' : 'active'}
                    className="rounded-full"
                    strokeColor={{
                      from: '#6366f1',
                      to: '#4f46e5',
                    }}
                  />
                </div>
                <Divider className="my-4" />
                <div className="mb-6">
                  <Title level={4} className="mb-4 text-gray-800">执行步骤</Title>
                  {executionSteps.length > 0 ? (
                    <Timeline className="rounded-lg p-4 bg-gray-50">
                      {executionSteps.map((step, index) => (
                        <Timeline.Item 
                          key={index} 
                          color={getStatusColor(step.status)}
                          className="mb-3"
                        >
                          <Space orientation="vertical" className="w-full">
                            <Text strong className="text-gray-800">{step.agentType}</Text>
                            <Text className="text-gray-600">{step.task}</Text>
                            <Text type="secondary">{getStatusText(step.status)} - {step.duration}</Text>
                          </Space>
                        </Timeline.Item>
                      ))}
                    </Timeline>
                  ) : (
                    <div className="rounded-lg p-6 bg-gray-50 text-center">
                      <Text type="secondary">暂无执行步骤</Text>
                    </div>
                  )}
                </div>
                <Divider className="my-4" />
                <div className="mb-6">
                  <Title level={4} className="mb-4 text-gray-800">反思记录</Title>
                  {reflectionRecords.length > 0 ? (
                    <Table
                      dataSource={reflectionRecords}
                      columns={[
                        {
                          title: '内容',
                          dataIndex: 'content',
                          key: 'content',
                          className: 'text-gray-700'
                        },
                        {
                          title: '时间',
                          dataIndex: 'timestamp',
                          key: 'timestamp',
                          className: 'text-gray-500',
                          render: (text: string) => (
                            <Text type="secondary">{new Date(text).toLocaleString()}</Text>
                          )
                        },
                      ]}
                      rowKey="id"
                      className="rounded-lg overflow-hidden"
                      size="middle"
                    />
                  ) : (
                    <div className="rounded-lg p-6 bg-gray-50 text-center">
                      <Text type="secondary">暂无反思记录</Text>
                    </div>
                  )}
                </div>
              </div>
            )}
          </Card>
        )}
      </div>
    </Layout>
  );
};

export default Collaboration;