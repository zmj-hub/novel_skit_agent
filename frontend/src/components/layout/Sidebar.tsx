import React from 'react';
import { Menu, Tooltip } from 'antd';
import { Link, useLocation } from 'react-router-dom';
import { 
  DashboardOutlined, 
  MessageOutlined, 
  FileTextOutlined, 
  BookOutlined, 
  TeamOutlined, 
  DatabaseOutlined, 
  SettingOutlined,
  ScheduleOutlined
} from '@ant-design/icons';

interface SidebarProps {
  collapsed?: boolean;
}

const Sidebar: React.FC<SidebarProps> = ({ collapsed = false }) => {
  const location = useLocation();
  const currentPath = location.pathname;

  const menuItems = [
    {
      key: '/dashboard',
      icon: <DashboardOutlined />,
      label: <Link to="/dashboard">仪表盘</Link>,
      title: '仪表盘',
    },
    {
      key: '/chat',
      icon: <MessageOutlined />,
      label: <Link to="/chat">智能对话</Link>,
      title: '智能对话',
    },
    {
      key: '/creative',
      icon: <FileTextOutlined />,
      label: <Link to="/creative">创意策划</Link>,
      title: '创意策划',
    },
    {
      key: '/novel',
      icon: <BookOutlined />,
      label: <Link to="/novel">小说创作</Link>,
      title: '小说创作',
    },
    {
      key: '/collaboration',
      icon: <TeamOutlined />,
      label: <Link to="/collaboration">智能体协作</Link>,
      title: '智能体协作',
    },
    {
      key: '/scheduler',
      icon: <ScheduleOutlined />,
      label: <Link to="/scheduler">任务调度</Link>,
      title: '任务调度',
    },
    {
      key: '/knowledge',
      icon: <DatabaseOutlined />,
      label: <Link to="/knowledge">知识库</Link>,
      title: '知识库',
    },
    {
      key: '/settings',
      icon: <SettingOutlined />,
      label: <Link to="/settings">系统设置</Link>,
      title: '系统设置',
    },
  ];

  return (
    <div className="h-full py-4">
      <Menu
        mode="inline"
        inlineCollapsed={collapsed}
        selectedKeys={[currentPath]}
        items={menuItems.map(item => ({
          ...item,
          label: collapsed ? (
            <Tooltip title={item.title} placement="right">
              {item.label}
            </Tooltip>
          ) : item.label,
        }))}
        className="bg-transparent border-none"
        theme="dark"
        style={{
          backgroundColor: 'transparent',
          border: 'none',
        }}
      />
    </div>
  );
};

export default Sidebar;
