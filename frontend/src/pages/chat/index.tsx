import React, { useState, useEffect, useRef } from 'react';
import { Typography, Input, Button, List, Avatar, Space, Switch, Select, message, Card, Divider } from 'antd';
import { SendOutlined, UserOutlined, RobotOutlined, DatabaseOutlined, SettingOutlined, PlusOutlined, ClearOutlined, SmileOutlined } from '@ant-design/icons';
import Layout from '../../components/layout/Layout';
import Loading from '../../components/common/Loading';
import api from '../../services/api';
import endpoints from '../../services/endpoints';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;
const { Option } = Select;

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: string;
}

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      content: '你好！我是小说创作智能体，很高兴为你服务。我可以帮你生成故事创意、撰写小说、提供写作建议等。请问有什么我可以帮助你的吗？',
      sender: 'ai',
      timestamp: new Date().toISOString(),
    },
  ]);
  const [inputValue, setInputValue] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [useKnowledge, setUseKnowledge] = useState<boolean>(true);
  const [model, setModel] = useState<string>('deepseek-chat');
  const [sessionId, setSessionId] = useState<string>(() => {
    // 生成随机会话ID（如果不存在）
    const savedSessionId = localStorage.getItem('chatSessionId');
    if (savedSessionId) {
      return savedSessionId;
    }
    const newSessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    localStorage.setItem('chatSessionId', newSessionId);
    return newSessionId;
  });
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!inputValue.trim()) return;

    // 添加用户消息到聊天
    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      sender: 'user',
      timestamp: new Date().toISOString(),
    };

    setMessages([...messages, userMessage]);
    setInputValue('');
    setLoading(true);

    try {
      // 发送消息到API
      // const response = await api.post(endpoints.chat.send, {
      //   message: inputValue,
      //   session_id: sessionId,
      //   use_knowledge: useKnowledge,
      //   model: model,
      // });

      // 模拟API响应
      setTimeout(() => {
        // 添加AI响应到聊天
        const aiMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: `我收到了你的消息："${inputValue}"。这是一个模拟的回复，实际应用中会调用后端API获取真实的AI回复。`,
          sender: 'ai',
          timestamp: new Date().toISOString(),
        };

        setMessages(prev => [...prev, aiMessage]);
        setLoading(false);
      }, 1500);
    } catch (error) {
      message.error('发送消息失败');
      console.error('发送消息错误:', error);

      // 添加错误消息到聊天
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: '抱歉，我无法处理你的消息。请稍后再试。',
        sender: 'ai',
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, errorMessage]);
      setLoading(false);
    }
  };

  const handleNewSession = () => {
    const newSessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    setSessionId(newSessionId);
    localStorage.setItem('chatSessionId', newSessionId);
    setMessages([
      {
        id: 'welcome',
        content: '你好！我是小说创作智能体，很高兴为你服务。我可以帮你生成故事创意、撰写小说、提供写作建议等。请问有什么我可以帮助你的吗？',
        sender: 'ai',
        timestamp: new Date().toISOString(),
      },
    ]);
    message.success('已创建新会话');
  };

  const handleClearChat = () => {
    setMessages([]);
    message.success('聊天记录已清空');
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Layout title="聊天 - 小说创作智能体">
      <div className="h-[calc(100vh-120px)] flex flex-col">
        {/* 聊天头部 */}
        <div className="flex justify-between items-center mb-6 pb-4 border-b border-gray-200">
          <div>
            <Title level={3} className="m-0">与AI聊天</Title>
            <Text className="text-gray-500">小说创作智能体</Text>
          </div>
          <Space>
            <Button 
              onClick={handleClearChat}
              icon={<ClearOutlined />}
            >
              清空聊天
            </Button>
            <Button 
              type="primary"
              onClick={handleNewSession}
              icon={<PlusOutlined />}
            >
              新会话
            </Button>
          </Space>
        </div>

        {/* 聊天消息 */}
        <div className="flex-1 overflow-y-auto mb-6 p-6 bg-gray-50 rounded-xl shadow-sm">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-gray-400">
              <RobotOutlined style={{ fontSize: '48px', marginBottom: '16px' }} />
              <Text>暂无聊天记录</Text>
              <Text className="mt-2">开始与AI聊天吧！</Text>
            </div>
          ) : (
            <List
              dataSource={messages}
              renderItem={(item) => (
                <List.Item 
                  key={item.id} 
                  className={`${item.sender === 'user' ? 'text-right' : 'text-left'} mb-6`}
                >
                  <List.Item.Meta
                    avatar={
                      item.sender === 'user' ? 
                        <Avatar 
                          icon={<UserOutlined />} 
                          style={{ 
                            backgroundColor: '#1a365d',
                            boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
                          }} 
                        /> : 
                        <Avatar 
                          icon={<RobotOutlined />} 
                          style={{ 
                            backgroundColor: '#f59e0b',
                            boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
                          }} 
                        />
                    }
                    title={
                      <Text className={`${item.sender === 'user' ? 'text-gray-600' : 'text-gray-600'}`}>
                        {item.sender === 'user' ? '我' : 'AI'}
                      </Text>
                    }
                    description={
                      <div 
                        className={`inline-block p-4 rounded-lg max-w-[80%] transition-all duration-300 ${item.sender === 'user' ? 
                          'bg-[#1a365d] text-white rounded-tr-none shadow-md' : 
                          'bg-white text-gray-800 rounded-tl-none shadow-md border border-gray-100'
                        }`}
                      >
                        <Text className={item.sender === 'user' ? 'text-white' : 'text-gray-800'}>
                          {item.content}
                        </Text>
                        <div className={`text-xs mt-2 ${item.sender === 'user' ? 'text-white/70' : 'text-gray-400'}`}>
                          {new Date(item.timestamp).toLocaleTimeString()}
                        </div>
                      </div>
                    }
                    className={item.sender === 'user' ? 'flex flex-row-reverse' : ''}
                  />
                </List.Item>
              )}
            />
          )}
          <div ref={messagesEndRef} />
          {loading && (
            <div className="flex justify-start items-center mt-4">
              <Avatar 
                icon={<RobotOutlined />} 
                className="mr-3" 
                style={{ backgroundColor: '#f59e0b' }} 
              />
              <Loading message="AI正在思考..." size="small" />
            </div>
          )}
        </div>

        {/* 设置区域 */}
        <Card 
          className="mb-6"
          variant="borderless"
          style={{ borderRadius: '12px' }}
          styles={{ body: { padding: '16px' } }}
        >
          <div className="flex flex-wrap justify-between items-center gap-4">
            <Space>
              <DatabaseOutlined style={{ color: '#1a365d' }} />
              <span className="text-gray-700">使用知识库</span>
              <Switch 
                checked={useKnowledge} 
                onChange={setUseKnowledge}
                checkedChildren="开启"
                unCheckedChildren="关闭"
                style={{ 
                  backgroundColor: useKnowledge ? '#1a365d' : '#d1d5db',
                  '&:hover': {
                    backgroundColor: useKnowledge ? '#2a4365' : '#9ca3af',
                  },
                }}
              />
            </Space>
            <Space>
              <SettingOutlined style={{ color: '#1a365d' }} />
              <span className="text-gray-700">模型选择</span>
              <Select
                value={model}
                onChange={setModel}
                style={{ width: 180 }}
                options={[
                  { value: 'deepseek-chat', label: 'DeepSeek Chat' },
                  { value: 'qwen3-30b', label: 'Qwen3-30B' },
                  { value: 'gpt-4', label: 'GPT-4' },
                ]}
              />
            </Space>
          </div>
        </Card>

        {/* 输入区域 */}
        <div className="bg-white rounded-xl shadow-md p-4 border border-gray-100">
          <div className="flex gap-3">
            <TextArea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="输入消息..."
              className="flex-1 resize-none"
              rows={4}
              onPressEnter={handleKeyPress}
              style={{ 
                borderRadius: '12px',
                border: '1px solid #e5e7eb',
                '&:focus': {
                  borderColor: '#1a365d',
                  boxShadow: '0 0 0 3px rgba(26, 54, 93, 0.1)',
                },
              }}
            />
            <Button
              type="primary"
              icon={<SendOutlined />}
              onClick={handleSend}
              loading={loading}
              disabled={!inputValue.trim()}
              style={{ 
                backgroundColor: '#1a365d',
                borderRadius: '12px',
                height: '40px',
                alignSelf: 'flex-end',
              }}
              className="self-end"
            >
              发送
            </Button>
          </div>
          <div className="flex justify-between items-center mt-3">
            <Text className="text-xs text-gray-500">
              会话ID: {sessionId}
            </Text>
            <Text className="text-xs text-gray-500">
              按 Enter 发送消息，Shift + Enter 换行
            </Text>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Chat;