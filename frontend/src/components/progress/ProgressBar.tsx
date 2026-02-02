import React from 'react';

interface ProgressBarProps {
  progress: number;
  status?: 'pending' | 'running' | 'completed' | 'failed' | 'paused';
  label?: string;
  height?: number;
  showPercentage?: boolean;
}

const ProgressBar: React.FC<ProgressBarProps> = ({
  progress,
  status = 'running',
  label,
  height = 8,
  showPercentage = true,
}) => {
  // 根据状态选择颜色
  const getColor = () => {
    switch (status) {
      case 'completed':
        return '#52c41a';
      case 'failed':
        return '#ff4d4f';
      case 'paused':
        return '#faad14';
      case 'running':
        return '#1890ff';
      case 'pending':
      default:
        return '#d9d9d9';
    }
  };

  return (
    <div className="w-full">
      {label && (
        <div className="flex justify-between mb-1">
          <span className="text-sm text-gray-600">{label}</span>
          {showPercentage && (
            <span className="text-sm font-medium">{Math.round(progress)}%</span>
          )}
        </div>
      )}
      <div 
        className="w-full bg-gray-200 rounded-full overflow-hidden" 
        style={{ height: `${height}px` }}
      >
        <div
          className="h-full rounded-full transition-all duration-300 ease-out"
          style={{
            width: `${Math.min(100, Math.max(0, progress))}%`,
            backgroundColor: getColor(),
          }}
        />
      </div>
    </div>
  );
};

export default ProgressBar;