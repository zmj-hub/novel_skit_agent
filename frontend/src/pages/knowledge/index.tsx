import React, { useState, useEffect } from 'react';
import { Card, Button, Input, Table, Tag, Modal, Form, message, Typography, Space, Popconfirm } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, SearchOutlined, BookOutlined } from '@ant-design/icons';
import Layout from '../../components/layout/Layout';

const { Title, Text } = Typography;

// Mock data for knowledge base entries
const mockKnowledgeBase = [
  {
    id: 1,
    title: '科幻小说元素',
    category: '体裁',
    content: '常见元素包括时间旅行、太空探索、外星生命形式、未来科技和平行宇宙等。',
    createdAt: '2026-01-20',
    updatedAt: '2026-01-25',
  },
  {
    id: 2,
    title: '角色塑造技巧',
    category: '写作',
    content: '创建具有优点、缺点、动机和背景故事的立体角色。在故事中展示他们的成长过程。',
    createdAt: '2026-01-18',
    updatedAt: '2026-01-22',
  },
  {
    id: 3,
    title: '世界观构建方法',
    category: '设定',
    content: '为你的世界建立一致的规则，包括地理、文化、历史、政治和魔法系统（如果适用）。',
    createdAt: '2026-01-15',
    updatedAt: '2026-01-15',
  },
  {
    id: 4,
    title: '情节结构设计',
    category: '剧情',
    content: '采用三幕式结构：开端（介绍角色和冲突）、发展（冲突升级）、结局（解决冲突）。',
    createdAt: '2026-01-10',
    updatedAt: '2026-01-10',
  },
  {
    id: 5,
    title: '主题表达技巧',
    category: '主题',
    content: '通过角色行为和情节发展自然地表达主题，避免直接说教。',
    createdAt: '2026-01-05',
    updatedAt: '2026-01-05',
  },
];

const KnowledgeBase: React.FC = () => {
  const [knowledgeBase, setKnowledgeBase] = useState(mockKnowledgeBase);
  const [searchText, setSearchText] = useState('');
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [editingEntry, setEditingEntry] = useState<any>(null);
  const [form] = Form.useForm();

  // Filter knowledge base entries based on search text
  const filteredKnowledgeBase = knowledgeBase.filter(entry =>
    entry.title.toLowerCase().includes(searchText.toLowerCase()) ||
    entry.category.toLowerCase().includes(searchText.toLowerCase()) ||
    entry.content.toLowerCase().includes(searchText.toLowerCase())
  );

  // Handle modal open for adding new entry
  const handleAddEntry = () => {
    setEditingEntry(null);
    form.resetFields();
    setIsModalVisible(true);
  };

  // Handle modal open for editing entry
  const handleEditEntry = (entry: any) => {
    setEditingEntry(entry);
    form.setFieldsValue(entry);
    setIsModalVisible(true);
  };

  // Handle form submission
  const handleSubmit = (values: any) => {
    if (editingEntry) {
      // Update existing entry
      setKnowledgeBase(knowledgeBase.map(entry =>
        entry.id === editingEntry.id
          ? { ...entry, ...values, updatedAt: new Date().toISOString().split('T')[0] }
          : entry
      ));
      message.success('知识库条目更新成功');
    } else {
      // Add new entry
      const newEntry = {
        id: knowledgeBase.length + 1,
        ...values,
        createdAt: new Date().toISOString().split('T')[0],
        updatedAt: new Date().toISOString().split('T')[0],
      };
      setKnowledgeBase([...knowledgeBase, newEntry]);
      message.success('知识库条目添加成功');
    }
    setIsModalVisible(false);
  };

  // Handle entry deletion
  const handleDeleteEntry = (id: number) => {
    setKnowledgeBase(knowledgeBase.filter(entry => entry.id !== id));
    message.success('知识库条目删除成功');
  };

  // Table columns configuration
  const columns = [
    {
      title: '标题',
      dataIndex: 'title',
      key: 'title',
      render: (text: string) => <Text strong className="text-gray-800">{text}</Text>,
      width: 200,
    },
    {
      title: '分类',
      dataIndex: 'category',
      key: 'category',
      render: (category: string) => (
        <Tag color={getCategoryColor(category)} className="font-medium">{category}</Tag>
      ),
      width: 120,
    },
    {
      title: '内容',
      dataIndex: 'content',
      key: 'content',
      ellipsis: {
        rows: 2,
        expandable: true,
      },
      className: 'text-gray-700',
    },
    {
      title: '创建时间',
      dataIndex: 'createdAt',
      key: 'createdAt',
      className: 'text-gray-500',
      width: 120,
    },
    {
      title: '更新时间',
      dataIndex: 'updatedAt',
      key: 'updatedAt',
      className: 'text-gray-500',
      width: 120,
    },
    {
      title: '操作',
      key: 'actions',
      render: (_: any, record: any) => (
        <Space size="middle">
          <Button
            icon={<EditOutlined />}
            onClick={() => handleEditEntry(record)}
            className="rounded-lg"
            size="middle"
          >
            编辑
          </Button>
          <Popconfirm
            title="确定要删除这条知识库条目吗？"
            onConfirm={() => handleDeleteEntry(record.id)}
            okText="确定"
            cancelText="取消"
          >
            <Button
              danger
              icon={<DeleteOutlined />}
              className="rounded-lg"
              size="middle"
            >
              删除
            </Button>
          </Popconfirm>
        </Space>
      ),
      width: 180,
      fixed: 'right' as const,
    },
  ];

  // Helper function to get category color
  const getCategoryColor = (category: string) => {
    const colorMap: Record<string, string> = {
      体裁: 'blue',
      写作: 'green',
      设定: 'purple',
      角色: 'orange',
      剧情: 'red',
      主题: 'cyan',
    };
    return colorMap[category] || 'default';
  };

  return (
    <Layout title="知识库 - 小说创作助手">
      <div className="knowledge-base-container space-y-8">
        {/* Header Section */}
        <div className="flex justify-between items-center">
          <div>
            <Title level={2} className="text-gray-800 mb-2">知识库</Title>
            <Text type="secondary">管理和查询小说创作相关的知识条目</Text>
          </div>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={handleAddEntry}
            className="rounded-lg"
            size="large"
            style={{ 
              background: 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)',
              border: 'none',
              height: '44px',
              padding: '0 24px'
            }}
          >
            添加条目
          </Button>
        </div>

        {/* Search and Table Section */}
        <Card
          className="shadow-md rounded-lg overflow-hidden"
          style={{ 
            background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(249,250,251,0.95) 100%)',
            boxShadow: '0 4px 20px rgba(0,0,0,0.08)'
          }}
        >
          <div className="flex justify-between items-center mb-6">
            <Text strong className="text-gray-700 text-lg">搜索知识库</Text>
            <Input
              placeholder="按标题、分类或内容搜索"
              prefix={<SearchOutlined />}
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)}
              style={{ width: 400 }}
              className="rounded-lg"
              size="middle"
            />
          </div>

          <Table
            columns={columns}
            dataSource={filteredKnowledgeBase}
            rowKey="id"
            pagination={{ 
              pageSize: 10,
              showSizeChanger: true,
              pageSizeOptions: ['5', '10', '20'],
              showQuickJumper: true,
              showTotal: (total) => `共 ${total} 条记录`,
            }}
            className="rounded-lg overflow-hidden"
            size="middle"
            scroll={{ x: 1200 }}
          />
        </Card>

        {/* Add/Edit Entry Modal */}
        <Modal
          title={editingEntry ? '编辑知识库条目' : '添加知识库条目'}
          open={isModalVisible}
          onCancel={() => setIsModalVisible(false)}
          footer={null}
          className="rounded-lg"
          style={{ borderRadius: '12px' }}
        >
          <Form
            form={form}
            onFinish={handleSubmit}
            layout="vertical"
            className="space-y-6"
          >
            <Form.Item
              name="title"
              label="标题"
              rules={[{ required: true, message: '请输入标题' }]}
              className="mb-4"
            >
              <Input 
                placeholder="请输入知识库条目标题" 
                className="rounded-lg border-gray-300 focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                size="middle"
              />
            </Form.Item>

            <Form.Item
              name="category"
              label="分类"
              rules={[{ required: true, message: '请输入分类' }]}
              className="mb-4"
            >
              <Input 
                placeholder="请输入知识库条目分类" 
                className="rounded-lg border-gray-300 focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                size="middle"
              />
              <Text type="secondary" className="block mt-2">例如：体裁、写作、设定、角色、剧情、主题等</Text>
            </Form.Item>

            <Form.Item
              name="content"
              label="内容"
              rules={[{ required: true, message: '请输入内容' }]}
              className="mb-6"
            >
              <Input.TextArea
                rows={5}
                placeholder="请输入知识库条目内容"
                className="rounded-lg border-gray-300 focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                size="middle"
              />
            </Form.Item>

            <Form.Item className="flex justify-end space-x-4">
              <Button
                onClick={() => setIsModalVisible(false)}
                className="rounded-lg"
                size="middle"
                style={{ width: '100px' }}
              >
                取消
              </Button>
              <Button 
                type="primary" 
                htmlType="submit"
                className="rounded-lg"
                size="middle"
                style={{ 
                  width: '100px',
                  background: 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)',
                  border: 'none'
                }}
              >
                {editingEntry ? '更新' : '添加'}
              </Button>
            </Form.Item>
          </Form>
        </Modal>
      </div>
    </Layout>
  );
};

export default KnowledgeBase;