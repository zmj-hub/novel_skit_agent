import React, { useState, useEffect } from 'react';
import { Typography, Row, Col, Table, Tag, Button, Modal, Descriptions, Badge, Space, Card, Statistic } from 'antd';
import { 
  ClockCircleOutlined, 
  CheckCircleOutlined, 
  CloseCircleOutlined, 
  LoadingOutlined, 
  DashboardOutlined, 
  CheckSquareOutlined, 
  CloseSquareOutlined, 
  SyncOutlined, 
  UserOutlined, 
  DatabaseOutlined, 
  FileTextOutlined,
  BookOutlined,
  TeamOutlined,
  MessageOutlined
} from '@ant-design/icons';
import Layout from '../../components/layout/Layout';
import StatCard from '../../components/common/StatCard';
import Loading from '../../components/common/Loading';
import api from '../../services/api';
import endpoints from '../../services/endpoints';

const { Title, Text, Paragraph } = Typography;

interface Task {
  id: string;
  taskGoal: string;
  status: 'completed' | 'running' | 'failed';
  startTime: string;
  endTime: string | null;
  duration: string;
  agents: string[];
}

interface AgentStatus {
  [key: string]: 'available' | 'busy' | 'offline';
}

interface WorkflowStep {
  stepId: string;
  agentType: string;
  task: string;
  status: 'success' | 'running' | 'failed';
  startTime: string;
  endTime: string | null;
  duration: string;
  error?: string;
}

const Dashboard: React.FC = () => {
  const [monitoringData, setMonitoringData] = useState<any>({
    totalTasks: 128,
    successTasks: 112,
    failedTasks: 8,
    runningTasks: 8,
    agentStatuses: {
      creative: 'available',
      novel: 'available',
      collaboration: 'busy',
      chat: 'available',
      knowledge: 'available',
    },
    executionHistory: [
      {
        id: 'task_001',
        taskGoal: '生成一个关于人工智能的科幻小说创意',
        status: 'completed',
        startTime: '2026-01-30 10:00:00',
        endTime: '2026-01-30 10:05:30',
        duration: '5m 30s',
        agents: ['creative', 'novel'],
      },
      {
        id: 'task_002',
        taskGoal: '撰写短篇小说《AI时代的情感抉择》',
        status: 'completed',
        startTime: '2026-01-30 09:30:00',
        endTime: '2026-01-30 09:50:15',
        duration: '20m 15s',
        agents: ['novel', 'collaboration'],
      },
      {
        id: 'task_003',
        taskGoal: '分析市场热点并生成创意框架',
        status: 'running',
        startTime: '2026-01-30 09:00:00',
        endTime: null,
        duration: '10m 00s',
        agents: ['creative'],
      },
      {
        id: 'task_004',
        taskGoal: '生成小说章节内容',
        status: 'failed',
        startTime: '2026-01-30 08:30:00',
        endTime: '2026-01-30 08:40:00',
        duration: '10m 00s',
        agents: ['novel'],
      },
    ],
  });
  const [loading, setLoading] = useState<boolean>(false);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [workflowSteps, setWorkflowSteps] = useState<WorkflowStep[]>([]);
  const [workflowLoading, setWorkflowLoading] = useState<boolean>(false);
  const [workflowModalVisible, setWorkflowModalVisible] = useState<boolean>(false);

  useEffect(() => {
    // fetchMonitoringData();
  }, []);

  const fetchMonitoringData = async () => {
    setLoading(true);
    try {
      const response = await api.get(endpoints.monitoring.data);
      setMonitoringData(response);
    } catch (error) {
      console.error('获取监控数据失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchWorkflowDetails = async (taskId: string) => {
    setWorkflowLoading(true);
    try {
      // const response = await api.get(endpoints.monitoring.workflow.replace('{task_id}', taskId));
      // setWorkflowSteps(response.steps || []);
      // 模拟数据
      setWorkflowSteps([
        {
          stepId: 'step_001',
          agentType: 'creative',
          task: '分析市场热点',
          status: 'success',
          startTime: '2026-01-30 10:00:00',
          endTime: '2026-01-30 10:01:30',
          duration: '1m 30s',
        },
        {
          stepId: 'step_002',
          agentType: 'creative',
          task: '生成故事创意',
          status: 'success',
          startTime: '2026-01-30 10:01:30',
          endTime: '2026-01-30 10:03:30',
          duration: '2m 00s',
        },
        {
          stepId: 'step_003',
          agentType: 'novel',
          task: '优化创意框架',
          status: 'success',
          startTime: '2026-01-30 10:03:30',
          endTime: '2026-01-30 10:05:30',
          duration: '2m 00s',
        },
      ]);
      setWorkflowModalVisible(true);
    } catch (error) {
      console.error('获取工作流详情失败:', error);
    } finally {
      setWorkflowLoading(false);
    }
  };

  const handleViewWorkflow = (task: Task) => {
    setSelectedTask(task);
    fetchWorkflowDetails(task.id);
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircleOutlined className="text-green-500" />;
      case 'running':
        return <LoadingOutlined className="text-blue-500" />;
      case 'failed':
        return <CloseCircleOutlined className="text-red-500" />;
      default:
        return null;
    }
  };

  const getStatusTag = (status: string) => {
    switch (status) {
      case 'completed':
      case 'success':
        return <Tag color="green">已完成</Tag>;
      case 'running':
        return <Tag color="blue">运行中</Tag>;
      case 'failed':
        return <Tag color="red">失败</Tag>;
      default:
        return <Tag color="default">未知</Tag>;
    }
  };

  const getAgentStatusBadge = (status: string) => {
    switch (status) {
      case 'available':
        return <Badge status="success" text="可用" />;
      case 'busy':
        return <Badge status="processing" text="忙碌" />;
      case 'offline':
        return <Badge status="error" text="离线" />;
      default:
        return <Badge status="default" text="未知" />;
    }
  };

  const getAgentName = (agent: string) => {
    const names: { [key: string]: string } = {
      creative: '创意智能体',
      novel: '小说智能体',
      collaboration: '协作智能体',
      chat: '聊天智能体',
      knowledge: '知识库智能体',
    };
    return names[agent] || agent;
  };

  const getAgentIcon = (agent: string) => {
    switch (agent) {
      case 'creative':
        return <FileTextOutlined className="mr-2" />;
      case 'novel':
        return <BookOutlined className="mr-2" />;
      case 'collaboration':
        return <TeamOutlined className="mr-2" />;
      case 'chat':
        return <MessageOutlined className="mr-2" />;
      case 'knowledge':
        return <DatabaseOutlined className="mr-2" />;
      default:
        return <UserOutlined className="mr-2" />;
    }
  };

  const getAgentTag = (agent: string) => {
    const names: { [key: string]: string } = {
      creative: '创意',
      novel: '小说',
      collaboration: '协作',
      chat: '聊天',
      knowledge: '知识库',
    };
    return names[agent] || agent;
  };

  if (loading) {
    return <Loading message="加载仪表盘数据..." />;
  }

  return (
    <Layout title="仪表盘 - 小说创作智能体">
      <div>
        {/* 页面标题 */}
        <div className="flex justify-between items-center mb-6">
          <Title level={2} className="m-0 text-2xl font-bold text-slate-800">系统概览</Title>
          <Button 
            type="primary" 
            onClick={fetchMonitoringData}
            icon={<SyncOutlined />}
            className="bg-indigo-600 hover:bg-indigo-700"
          >
            刷新数据
          </Button>
        </div>
        
        {/* 统计卡片 */}
        <Row gutter={[16, 16]} className="mb-6">
          <Col xs={24} sm={12} md={6}>
            <Card className="h-full hover:shadow-md transition-shadow">
              <Statistic
                title="总任务数"
                value={monitoringData?.totalTasks || 0}
                styles={{ content: { color: '#1e293b', fontSize: '28px', fontWeight: 600 } }}
                prefix={<CheckSquareOutlined className="text-slate-600 mr-2" />}
              />
              <div className="mt-2 text-sm text-green-600">
                ↑ 12% 较上周
              </div>
            </Card>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Card className="h-full hover:shadow-md transition-shadow">
              <Statistic
                title="成功任务"
                value={monitoringData?.successTasks || 0}
                styles={{ content: { color: '#10b981', fontSize: '28px', fontWeight: 600 } }}
                prefix={<CheckCircleOutlined className="text-green-500 mr-2" />}
              />
              <div className="mt-2 text-sm text-green-600">
                ↑ 8% 较上周
              </div>
            </Card>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Card className="h-full hover:shadow-md transition-shadow">
              <Statistic
                title="失败任务"
                value={monitoringData?.failedTasks || 0}
                styles={{ content: { color: '#ef4444', fontSize: '28px', fontWeight: 600 } }}
                prefix={<CloseSquareOutlined className="text-red-500 mr-2" />}
              />
              <div className="mt-2 text-sm text-red-600">
                ↓ 2% 较上周
              </div>
            </Card>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Card className="h-full hover:shadow-md transition-shadow">
              <Statistic
                title="运行中任务"
                value={monitoringData?.runningTasks || 0}
                styles={{ content: { color: '#f59e0b', fontSize: '28px', fontWeight: 600 } }}
                prefix={<SyncOutlined className="text-amber-500 mr-2" />}
              />
              <div className="mt-2 text-sm text-amber-600">
                ↑ 5% 较上周
              </div>
            </Card>
          </Col>
        </Row>

        {/* 智能体状态 */}
        <Card 
          title="智能体状态" 
          className="mb-6"
          variant="borderless"
          style={{ borderRadius: '12px', boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)' }}
          styles={{ header: { borderBottom: '1px solid #f1f5f9', fontWeight: 600 } }}
        >
          <Row gutter={[16, 16]}>
            {Object.entries(monitoringData?.agentStatuses || {}).map(([agent, status]) => (
              <Col key={agent} xs={24} sm={12} md={8} lg={6}>
                <Card 
                  className="h-full"
                  variant="borderless"
                  style={{ 
                    borderRadius: '8px',
                    border: '1px solid #f1f5f9',
                    background: '#fafafa'
                  }}
                  styles={{ body: { padding: '16px' } }}
                >
                  <Space orientation="vertical" style={{ width: '100%' }} size="small">
                    <div className="flex justify-between items-center">
                      <Text strong className="text-slate-700">
                        {getAgentName(agent)}
                      </Text>
                        {getAgentStatusBadge(status as string)}
                    </div>
                    <div className="flex items-center text-sm text-slate-500">
                      {getAgentIcon(agent)}
                      最后更新: {new Date().toLocaleTimeString()}
                    </div>
                  </Space>
                </Card>
              </Col>
            ))}
          </Row>
        </Card>

        {/* 执行历史 */}
        <Card 
          title="执行历史" 
          className="mb-6"
          variant="borderless"
          style={{ borderRadius: '12px', boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)' }}
          styles={{ header: { borderBottom: '1px solid #f1f5f9', fontWeight: 600 } }}
        >
          <Table
            dataSource={monitoringData?.executionHistory || []}
            columns={[
              {
                title: '任务ID',
                dataIndex: 'id',
                key: 'id',
                width: 100,
              },
              {
                title: '任务目标',
                dataIndex: 'taskGoal',
                key: 'taskGoal',
                ellipsis: true,
              },
              {
                title: '状态',
                dataIndex: 'status',
                key: 'status',
                width: 100,
                render: (status: string) => getStatusTag(status),
              },
              {
                title: '开始时间',
                dataIndex: 'startTime',
                key: 'startTime',
                width: 160,
              },
              {
                title: '持续时间',
                dataIndex: 'duration',
                key: 'duration',
                width: 100,
              },
              {
                title: '智能体',
                dataIndex: 'agents',
                key: 'agents',
                width: 150,
                render: (agents: string[]) => (
                  <Space wrap>
                    {agents.map((agent, index) => (
                      <Tag key={index} color="blue">
                        {getAgentTag(agent)}
                      </Tag>
                    ))}
                  </Space>
                ),
              },
              {
                title: '操作',
                key: 'actions',
                width: 120,
                render: (_: any, record: Task) => (
                  <Button 
                    type="link" 
                    onClick={() => handleViewWorkflow(record)}
                    className="text-indigo-600 hover:text-indigo-700"
                  >
                    查看工作流
                  </Button>
                ),
              },
            ]}
            rowKey="id"
            pagination={{
              pageSize: 10,
              showSizeChanger: true,
              pageSizeOptions: ['10', '20', '50'],
            }}
          />
        </Card>

        {/* 工作流详情模态框 */}
        <Modal
          title={`工作流详情: ${selectedTask?.id}`}
          open={workflowModalVisible}
          onCancel={() => setWorkflowModalVisible(false)}
          footer={[
            <Button key="close" onClick={() => setWorkflowModalVisible(false)}>
              关闭
            </Button>,
          ]}
          width={900}
          centered
          style={{ borderRadius: '12px' }}
        >
          {workflowLoading ? (
            <Loading message="加载工作流详情..." />
          ) : (
            <div>
              <Descriptions title="任务信息" className="mb-6" bordered>
                <Descriptions.Item label="任务ID">{selectedTask?.id}</Descriptions.Item>
                <Descriptions.Item label="任务目标">{selectedTask?.taskGoal}</Descriptions.Item>
                <Descriptions.Item label="状态">{getStatusTag(selectedTask?.status || '')}</Descriptions.Item>
                <Descriptions.Item label="开始时间">{selectedTask?.startTime}</Descriptions.Item>
                <Descriptions.Item label="结束时间">{selectedTask?.endTime || 'N/A'}</Descriptions.Item>
                <Descriptions.Item label="持续时间">{selectedTask?.duration}</Descriptions.Item>
              </Descriptions>

              <Title level={4}>工作流步骤</Title>
              <Table
                dataSource={workflowSteps}
                columns={[
                  {
                    title: '步骤ID',
                    dataIndex: 'stepId',
                    key: 'stepId',
                    width: 100,
                  },
                  {
                    title: '智能体类型',
                    dataIndex: 'agentType',
                    key: 'agentType',
                    width: 120,
                    render: (agentType: string) => (
                      <Text>{getAgentName(agentType)}</Text>
                    ),
                  },
                  {
                    title: '任务',
                    dataIndex: 'task',
                    key: 'task',
                    ellipsis: true,
                  },
                  {
                    title: '状态',
                    dataIndex: 'status',
                    key: 'status',
                    width: 100,
                    render: (status: string) => getStatusTag(status),
                  },
                  {
                    title: '开始时间',
                    dataIndex: 'startTime',
                    key: 'startTime',
                    width: 160,
                  },
                  {
                    title: '持续时间',
                    dataIndex: 'duration',
                    key: 'duration',
                    width: 100,
                  },
                  {
                    title: '错误',
                    dataIndex: 'error',
                    key: 'error',
                    ellipsis: true,
                    render: (error: string) => error || 'N/A',
                  },
                ]}
                rowKey="stepId"
                pagination={false}
              />
            </div>
          )}
        </Modal>
      </div>
    </Layout>
  );
};

export default Dashboard;
