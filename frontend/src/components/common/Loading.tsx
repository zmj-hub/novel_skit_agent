import React from 'react';
import { Spin, Typography } from 'antd';

const { Text } = Typography;

interface LoadingProps {
  message?: string;
  size?: 'small' | 'middle' | 'large';
  fullscreen?: boolean;
}

const Loading: React.FC<LoadingProps> = ({
  message = 'Loading...',
  size = 'middle',
  fullscreen = false,
}) => {
  if (fullscreen) {
    return (
      <div className="fixed inset-0 bg-white bg-opacity-80 flex flex-col justify-center items-center z-50">
        <Spin size={size} />
        <Text className="mt-4">{message}</Text>
      </div>
    );
  }

  return (
    <div className="flex flex-col justify-center items-center py-8">
      <Spin size={size} />
      <Text className="mt-4">{message}</Text>
    </div>
  );
};

export default Loading;