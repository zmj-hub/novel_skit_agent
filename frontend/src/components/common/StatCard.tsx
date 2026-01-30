import React from 'react';
import { Card, Statistic, Typography } from 'antd';
import { ReactNode } from 'react';

const { Text } = Typography;

interface StatCardProps {
  title: string;
  value: string | number;
  prefix?: ReactNode;
  suffix?: ReactNode;
  color?: string;
  description?: string;
}

const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  prefix,
  suffix,
  color = '#1890ff',
  description,
}) => {
  return (
    <Card className="h-full">
      <Statistic
        title={title}
        value={value}
        prefix={prefix}
        suffix={suffix}
        valueStyle={{ color }}
        description={description}
      />
    </Card>
  );
};

export default StatCard;