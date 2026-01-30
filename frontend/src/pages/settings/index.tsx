import React, { useState } from 'react';
import { Card, Form, Input, Button, Switch, Select, message, Typography, Space, Divider } from 'antd';
import { 
  SettingOutlined, 
  AppstoreOutlined, 
  CodeOutlined, 
  ThemeOutlined, 
  GlobalOutlined, 
  BellOutlined, 
  SaveOutlined, 
  InfoCircleOutlined,
  LayoutOutlined,
  VersionOutlined
} from '@ant-design/icons';
import Layout from '../../components/layout/Layout';

const { Option } = Select;
const { Title, Text, Paragraph } = Typography;

const Settings: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState<boolean>(false);

  // Initial form values
  const initialValues = {
    apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
    appName: import.meta.env.VITE_APP_NAME || '小说创作助手',
    appVersion: import.meta.env.VITE_APP_VERSION || '1.0.0',
    theme: 'light',
    notifications: true,
    autoSave: true,
    language: 'zh',
  };

  // Handle form submission
  const handleSubmit = (_values: any) => {
    setLoading(true);
    
    // In a real app, you would save these settings to localStorage or an API
    setTimeout(() => {
      message.success('设置保存成功');
      setLoading(false);
    }, 1000);
  };

  return (
    <Layout title="设置 - 小说创作助手">
      <div className="settings-container space-y-8">
        {/* Header Section */}
        <div>
          <div className="flex items-center space-x-3 mb-2">
            <SettingOutlined className="text-indigo-600" style={{ fontSize: '24px' }} />
            <Title level={2} className="text-gray-800 mb-0">设置</Title>
          </div>
          <Text type="secondary">配置应用程序的各项设置</Text>
        </div>
        
        {/* Application Settings Card */}
        <Card
          title={
            <Space>
              <AppstoreOutlined />
              <span>应用设置</span>
            </Space>
          }
          className="shadow-md rounded-lg overflow-hidden"
          style={{ 
            background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(249,250,251,0.95) 100%)',
            boxShadow: '0 4px 20px rgba(0,0,0,0.08)'
          }}
        >
          <Form 
            form={form} 
            onFinish={handleSubmit} 
            initialValues={initialValues} 
            layout="vertical"
            className="space-y-6"
          >
            <Form.Item
              name="appName"
              label={
                <Space>
                  <AppstoreOutlined className="text-gray-600" />
                  <span>应用名称</span>
                </Space>
              }
              rules={[{ required: true, message: '请输入应用名称' }]}
              className="mb-4"
            >
              <Input 
                placeholder="请输入应用名称" 
                className="rounded-lg border-gray-300 focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                size="middle"
              />
            </Form.Item>
            
            <Form.Item
              name="appVersion"
              label={
                <Space>
                  <VersionOutlined className="text-gray-600" />
                  <span>应用版本</span>
                </Space>
              }
              className="mb-4"
            >
              <Input 
                placeholder="请输入应用版本" 
                className="rounded-lg border-gray-300 focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                size="middle"
              />
            </Form.Item>
            
            <Form.Item
              name="apiBaseUrl"
              label={
                <Space>
                  <CodeOutlined className="text-gray-600" />
                  <span>API基础地址</span>
                </Space>
              }
              rules={[{ required: true, message: '请输入API基础地址' }]}
              className="mb-4"
            >
              <Input 
                placeholder="请输入API基础地址" 
                className="rounded-lg border-gray-300 focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                size="middle"
              />
            </Form.Item>
            
            <Form.Item
              name="theme"
              label={
                <Space>
                  <ThemeOutlined className="text-gray-600" />
                  <span>主题</span>
                </Space>
              }
              className="mb-4"
            >
              <Select 
                placeholder="选择主题"
                className="rounded-lg border-gray-300"
                size="middle"
              >
                <Option value="light">浅色</Option>
                <Option value="dark">深色</Option>
                <Option value="system">跟随系统</Option>
              </Select>
            </Form.Item>
            
            <Form.Item
              name="language"
              label={
                <Space>
                  <GlobalOutlined className="text-gray-600" />
                  <span>语言</span>
                </Space>
              }
              className="mb-4"
            >
              <Select 
                placeholder="选择语言"
                className="rounded-lg border-gray-300"
                size="middle"
              >
                <Option value="zh">中文</Option>
                <Option value="en">English</Option>
              </Select>
            </Form.Item>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <Form.Item
                name="notifications"
                label={
                  <Space>
                    <BellOutlined className="text-gray-600" />
                    <span>通知</span>
                  </Space>
                }
                valuePropName="checked"
              >
                <Switch 
                  checkedChildren="开启" 
                  unCheckedChildren="关闭" 
                  className="text-indigo-600"
                />
              </Form.Item>
              
              <Form.Item
                name="autoSave"
                label={
                  <Space>
                    <SaveOutlined className="text-gray-600" />
                    <span>自动保存</span>
                  </Space>
                }
                valuePropName="checked"
              >
                <Switch 
                  checkedChildren="开启" 
                  unCheckedChildren="关闭" 
                  className="text-indigo-600"
                />
              </Form.Item>
            </div>
            
            <Form.Item className="mt-8">
              <Button 
                type="primary" 
                htmlType="submit" 
                loading={loading}
                size="large"
                icon={<SaveOutlined />}
                className="rounded-lg"
                style={{ 
                  background: 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)',
                  border: 'none',
                  height: '48px',
                  padding: '0 32px',
                  fontSize: '16px',
                  fontWeight: 500
                }}
              >
                保存设置
              </Button>
            </Form.Item>
          </Form>
        </Card>
        
        {/* About Card */}
        <Card
          title={
            <Space>
              <InfoCircleOutlined />
              <span>关于</span>
            </Space>
          }
          className="shadow-md rounded-lg overflow-hidden"
          style={{ 
            background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(249,250,251,0.95) 100%)',
            boxShadow: '0 4px 20px rgba(0,0,0,0.08)'
          }}
        >
          <div className="space-y-4 p-4">
            <div className="flex items-start space-x-3">
              <AppstoreOutlined className="text-gray-500 mt-1" />
              <div>
                <Text strong className="text-gray-700">应用版本:</Text>
                <Text className="ml-2 text-gray-600">{initialValues.appVersion}</Text>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <CodeOutlined className="text-gray-500 mt-1" />
              <div>
                <Text strong className="text-gray-700">API基础地址:</Text>
                <Paragraph className="ml-2 text-gray-600 mt-0">{initialValues.apiBaseUrl}</Paragraph>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <LayoutOutlined className="text-gray-500 mt-1" />
              <div>
                <Text strong className="text-gray-700">环境:</Text>
                <Text className="ml-2 text-gray-600">
                  {import.meta.env.DEV ? '开发环境' : '生产环境'}
                </Text>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <VersionOutlined className="text-gray-500 mt-1" />
              <div>
                <Text strong className="text-gray-700">构建日期:</Text>
                <Text className="ml-2 text-gray-600">{new Date().toLocaleString()}</Text>
              </div>
            </div>
            <Divider className="my-4" />
            <div className="bg-indigo-50 rounded-lg p-4">
              <Text className="text-indigo-800">
                小说创作助手是一款专为作家和创作者设计的智能工具，
                提供创意策划、小说写作、智能协作等功能，
                帮助您更高效地完成创作任务。
              </Text>
            </div>
          </div>
        </Card>
      </div>
    </Layout>
  );
};

export default Settings;