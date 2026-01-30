import React from 'react';
import { Layout, Badge, Avatar, Dropdown, Space, Typography, Button, Input } from 'antd';
import { 
  BellOutlined, 
  UserOutlined, 
  DownOutlined, 
  MenuOutlined,
  SearchOutlined,
  QuestionCircleOutlined
} from '@ant-design/icons';

const { Header: AntHeader } = Layout;
const { Text } = Typography;

interface HeaderProps {
  collapsed?: boolean;
  isMobile?: boolean;
  onMenuClick?: () => void;
}

const Header: React.FC<HeaderProps> = ({ 
  collapsed = false, 
  isMobile = false, 
  onMenuClick 
}) => {
  const userMenu = [
    {
      key: 'profile',
      label: '个人资料',
    },
    {
      key: 'settings',
      label: '账号设置',
    },
    {
      type: 'divider',
    },
    {
      key: 'logout',
      label: '退出登录',
      danger: true,
    },
  ];

  const notificationMenu = [
    {
      key: '1',
      label: (
        <div className="py-2">
          <p className="font-medium text-sm">任务完成</p>
          <p className="text-xs text-gray-500">小说创作任务已完成</p>
          <p className="text-xs text-gray-400 mt-1">5分钟前</p>
        </div>
      ),
    },
    {
      key: '2',
      label: (
        <div className="py-2">
          <p className="font-medium text-sm">系统更新</p>
          <p className="text-xs text-gray-500">系统已更新至最新版本</p>
          <p className="text-xs text-gray-400 mt-1">1小时前</p>
        </div>
      ),
    },
    {
      key: '3',
      label: (
        <div className="py-2">
          <p className="font-medium text-sm">新功能上线</p>
          <p className="text-xs text-gray-500">智能对话功能已上线</p>
          <p className="text-xs text-gray-400 mt-1">2小时前</p>
        </div>
      ),
    },
  ];

  return (
    <AntHeader 
      className="flex justify-between items-center fixed top-0 right-0 z-[900] px-6"
      style={{
        height: 64,
        background: 'white',
        borderBottom: '1px solid var(--primary-100)',
        boxShadow: 'var(--shadow-sm)',
        left: isMobile ? 0 : (collapsed ? 80 : 256),
        transition: 'left 0.3s ease',
      }}
    >
      {/* 左侧区域 */}
      <div className="flex items-center gap-4">
        {/* 移动端菜单按钮 */}
        {isMobile && (
          <Button
            type="text"
            icon={<MenuOutlined />}
            onClick={onMenuClick}
            className="flex items-center justify-center"
            style={{ color: 'var(--primary-600)' }}
          />
        )}
        
        {/* 搜索框 */}
        <div className="hidden md:block">
          <Input
            prefix={<SearchOutlined className="text-gray-400" />}
            placeholder="全局搜索..."
            className="w-64"
            style={{
              borderRadius: 'var(--radius-lg)',
              background: 'var(--primary-50)',
              border: 'none',
            }}
          />
        </div>
      </div>

      {/* 右侧区域 */}
      <div className="flex items-center gap-4">
        {/* 帮助按钮 */}
        <Button
          type="text"
          icon={<QuestionCircleOutlined />}
          className="hidden sm:flex items-center justify-center"
          style={{ color: 'var(--primary-500)' }}
        />

        {/* 通知 */}
        <Dropdown
          menu={{ items: notificationMenu }}
          placement="bottomRight"
          trigger={['click']}
          overlayStyle={{ width: 320 }}
        >
          <Badge 
            count={3} 
            size="small"
            style={{ 
              backgroundColor: 'var(--warning-500)',
            }}
          >
            <Button
              type="text"
              icon={<BellOutlined style={{ fontSize: 18 }} />}
              className="flex items-center justify-center"
              style={{ color: 'var(--primary-600)' }}
            />
          </Badge>
        </Dropdown>

        {/* 用户菜单 */}
        <Dropdown 
          menu={{ items: userMenu }} 
          placement="bottomRight"
          trigger={['click']}
        >
          <Space 
            className="cursor-pointer py-1 px-2 rounded-lg hover:bg-gray-100 transition-colors"
            style={{ borderRadius: 'var(--radius-lg)' }}
          >
            <Avatar 
              icon={<UserOutlined />} 
              style={{ 
                background: 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)',
                border: '2px solid white',
                boxShadow: 'var(--shadow-sm)',
              }}
              size="small"
            />
            <div className="hidden lg:block">
              <Text className="text-sm font-medium block leading-tight" style={{ color: 'var(--primary-800)' }}>
                管理员
              </Text>
              <Text className="text-xs block" style={{ color: 'var(--primary-500)' }}>
                admin@novel.com
              </Text>
            </div>
            <DownOutlined className="text-xs" style={{ color: 'var(--primary-400)' }} />
          </Space>
        </Dropdown>
      </div>
    </AntHeader>
  );
};

export default Header;
