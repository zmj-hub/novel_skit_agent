import { lazy, Suspense } from 'react';
import { Navigate } from 'react-router-dom';

// 懒加载页面组件
const Dashboard = lazy(() => import('../pages/dashboard'));
const Chat = lazy(() => import('../pages/chat'));
const Creative = lazy(() => import('../pages/creative'));
const Novel = lazy(() => import('../pages/novel'));
const Collaboration = lazy(() => import('../pages/collaboration'));
const Scheduler = lazy(() => import('../pages/scheduler'));
const Knowledge = lazy(() => import('../pages/knowledge'));
const Settings = lazy(() => import('../pages/settings'));

// 路由配置
const routes = [
  {
    path: '/',
    element: <Navigate to="/dashboard" replace />,
  },
  {
    path: '/dashboard',
    element: (
      <Suspense fallback={<div>Loading...</div>}>
        <Dashboard />
      </Suspense>
    ),
  },
  {
    path: '/chat',
    element: (
      <Suspense fallback={<div>Loading...</div>}>
        <Chat />
      </Suspense>
    ),
  },
  {
    path: '/creative',
    element: (
      <Suspense fallback={<div>Loading...</div>}>
        <Creative />
      </Suspense>
    ),
  },
  {
    path: '/novel',
    element: (
      <Suspense fallback={<div>Loading...</div>}>
        <Novel />
      </Suspense>
    ),
  },
  {
    path: '/collaboration',
    element: (
      <Suspense fallback={<div>Loading...</div>}>
        <Collaboration />
      </Suspense>
    ),
  },
  {
    path: '/scheduler',
    element: (
      <Suspense fallback={<div>Loading...</div>}>
        <Scheduler />
      </Suspense>
    ),
  },
  {
    path: '/knowledge',
    element: (
      <Suspense fallback={<div>Loading...</div>}>
        <Knowledge />
      </Suspense>
    ),
  },
  {
    path: '/settings',
    element: (
      <Suspense fallback={<div>Loading...</div>}>
        <Settings />
      </Suspense>
    ),
  },
];

export default routes;