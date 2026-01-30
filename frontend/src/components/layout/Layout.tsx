import React, { ReactNode, useState, useEffect } from 'react';
import { Layout as AntLayout, Button, Drawer } from 'antd';
import { MenuOutlined, MenuFoldOutlined } from '@ant-design/icons';
import Sidebar from './Sidebar';
import Header from './Header';

const { Content, Sider } = AntLayout;

interface LayoutProps {
  children: ReactNode;
  title?: string;
}

const Layout: React.FC<LayoutProps> = ({ children, title = '小说创作智能体' }) => {
  const [collapsed, setCollapsed] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const [mobileDrawerOpen, setMobileDrawerOpen] = useState(false);

  // 设置页面标题
  useEffect(() => {
    document.title = title;
  }, [title]);

  // 监听窗口大小变化
  useEffect(() => {
    const handleResize = () => {
      const mobile = window.innerWidth < 768;
      setIsMobile(mobile);
      
      if (mobile) {
        setCollapsed(true);
      } else {
        setCollapsed(false);
      }
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // 切换侧边栏
  const toggleSidebar = () => {
    if (isMobile) {
      setMobileDrawerOpen(!mobileDrawerOpen);
    } else {
      setCollapsed(!collapsed);
    }
  };

  // 关闭移动端抽屉
  const closeMobileDrawer = () => {
    setMobileDrawerOpen(false);
  };

  // 计算侧边栏宽度
  const siderWidth = isMobile ? 0 : (collapsed ? 80 : 256);

  // 侧边栏内容
  const sidebarContent = (
    <div className="h-full flex flex-col" style={{ background: 'linear-gradient(180deg, #1e293b 0%, #0f172a 100%)' }}>
      {/* Logo 区域 */}
      <div 
        className="flex items-center justify-between px-4 py-4 border-b"
        style={{ borderColor: 'rgba(255, 255, 255, 0.1)' }}
      >
        <div className="flex items-center gap-3">
          <div 
            className="w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0"
            style={{ background: 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)' }}
          >
            <span className="text-white text-lg font-bold">N</span>
          </div>
          {!collapsed && (
            <div className="overflow-hidden">
              <h1 className="text-white font-semibold text-base leading-tight whitespace-nowrap">小说创作</h1>
              <p className="text-white/60 text-xs whitespace-nowrap">智能体系统</p>
            </div>
          )}
        </div>
        {!isMobile && (
          <Button
            type="text"
            icon={collapsed ? <MenuOutlined /> : <MenuFoldOutlined />}
            onClick={toggleSidebar}
            className="text-white/70 hover:text-white hover:bg-white/10 flex-shrink-0"
          />
        )}
      </div>
      
      {/* 导航菜单 */}
      <div className="flex-1 overflow-y-auto overflow-x-hidden">
        <Sidebar collapsed={collapsed} />
      </div>
      
      {/* 底部信息 */}
      {!collapsed && (
        <div 
          className="px-4 py-3 border-t text-center"
          style={{ borderColor: 'rgba(255, 255, 255, 0.1)' }}
        >
          <p className="text-white/40 text-xs">版本 2.0.0</p>
          <p className="text-white/30 text-xs mt-1">© 2026 Novel Skit Agent</p>
        </div>
      )}
    </div>
  );

  return (
    <AntLayout className="min-h-screen" style={{ background: '#f8fafc' }}>
      {/* 桌面端侧边栏 */}
      {!isMobile && (
        <Sider
          trigger={null}
          collapsible
          collapsed={collapsed}
          width={256}
          collapsedWidth={80}
          className="fixed left-0 top-0 h-screen"
          style={{
            zIndex: 1000,
            background: 'linear-gradient(180deg, #1e293b 0%, #0f172a 100%)',
            boxShadow: '4px 0 24px rgba(0, 0, 0, 0.15)',
          }}
        >
          {sidebarContent}
        </Sider>
      )}

      {/* 移动端抽屉 */}
      {isMobile && (
        <Drawer
          placement="left"
          closable={false}
          onClose={closeMobileDrawer}
          open={mobileDrawerOpen}
          width={256}
          bodyStyle={{ padding: 0 }}
          style={{ background: 'linear-gradient(180deg, #1e293b 0%, #0f172a 100%)' }}
        >
          {sidebarContent}
        </Drawer>
      )}

      {/* 主内容区域 */}
      <AntLayout
        style={{
          marginLeft: siderWidth,
          minHeight: '100vh',
          transition: 'margin-left 0.3s ease',
        }}
      >
        {/* 顶部导航栏 */}
        <div
          className="fixed top-0 right-0 h-16 flex items-center justify-between px-6 bg-white border-b"
          style={{
            left: siderWidth,
            zIndex: 900,
            borderColor: '#e2e8f0',
            boxShadow: '0 1px 3px rgba(0, 0, 0, 0.05)',
            transition: 'left 0.3s ease',
          }}
        >
          <div className="flex items-center gap-4">
            {/* 移动端菜单按钮 */}
            {isMobile && (
              <Button
                type="text"
                icon={<MenuOutlined />}
                onClick={toggleSidebar}
                style={{ color: '#64748b' }}
              />
            )}
            <h1 className="text-lg font-medium text-slate-800">{title}</h1>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm text-slate-600">管理员</span>
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white text-sm font-medium">
              A
            </div>
          </div>
        </div>

        {/* 内容区域 */}
        <Content 
          style={{ 
            marginTop: 64,
            padding: '24px',
            background: '#f8fafc',
            minHeight: 'calc(100vh - 64px)',
          }}
        >
          <div 
            style={{
              background: 'white',
              borderRadius: '12px',
              boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
              padding: '24px',
              minHeight: 'calc(100vh - 112px)',
            }}
          >
            {children}
          </div>
        </Content>
      </AntLayout>
    </AntLayout>
  );
};

export default Layout;
