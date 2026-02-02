import React, { useState } from 'react';
import { Typography, Form, Input, Select, Button, Tag, message, Divider, Space, Card, Alert, Tabs, Tooltip } from 'antd';
import { RocketOutlined, FireOutlined, BookOutlined, SettingOutlined, FileTextOutlined, ArrowRightOutlined, PlusOutlined, DeleteOutlined, CopyOutlined } from '@ant-design/icons';
import Layout from '../../components/layout/Layout';
import Loading from '../../components/common/Loading';
import api from '../../services/api';
import endpoints from '../../services/endpoints';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;

const Creative: React.FC = () => {
  const [form] = Form.useForm();
  const [hotspots, setHotspots] = useState<string[]>([]);
  const [hotspotInput, setHotspotInput] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [creativeDocument, setCreativeDocument] = useState<string>('');
  const [generationSuccess, setGenerationSuccess] = useState<boolean>(false);

  const handleAddHotspot = () => {
    if (hotspotInput.trim() && !hotspots.includes(hotspotInput.trim())) {
      setHotspots([...hotspots, hotspotInput.trim()]);
      setHotspotInput('');
    }
  };

  const handleRemoveHotspot = (hotspot: string) => {
    setHotspots(hotspots.filter(item => item !== hotspot));
  };

  const handleGenerateCreative = async (values: any) => {
    if (hotspots.length === 0) {
      message.error('请至少添加一个热点');
      return;
    }

    setLoading(true);
    setGenerationSuccess(false);

    try {
      // 发送请求到API
      // const response = await api.post(endpoints.creative.plan, {
      //   hotspots,
      //   story_type: values.story_type,
      //   session_id: values.session_id,
      //   model: values.model,
      // });

      // 模拟API响应
      setTimeout(() => {
        const mockCreativeDocument = `# 《AI时代的情感抉择》故事创意框架\n\n## 1. 人物设定\n\n### 林雨晴\n- **背景故事**：30岁，AI公司产品经理，事业心强，外表坚强内心敏感\n- **性格特征**：独立自信，思维敏捷，对工作充满热情，但在情感上有些封闭\n- **目标动机**：追求职业成功的同时，寻找真正的情感归属\n- **人物弧光**：从自我封闭到敞开心扉，学会平衡事业与情感\n\n### 陈默\n- **背景故事**：32岁，AI研发工程师，林雨晴的同事，技术天才\n- **性格特征**：内敛沉默，专注于技术，对林雨晴默默关心\n- **目标动机**：通过技术改变世界，同时希望获得林雨晴的认可\n- **人物弧光**：从默默无闻到勇敢表达，学会在爱情中主动出击\n\n## 2. 剧情大纲\n\n### 小说章回结构\n1. 第一章：职场危机\n2. 第二章：意外相遇\n3. 第三章：情感纠葛\n4. 第四章：AI助手的秘密\n5. 第五章：抉择时刻\n6. 第六章：真相大白\n7. 第七章：新的开始\n\n### 短剧集数结构\n1. 第一集：职场挑战\n2. 第二集：偶遇旧爱\n3. 第三集：抉择时刻\n4. 第四集：AI助手的建议\n5. 第五集：情感冲突\n6. 第六集：真相揭露\n7. 第七集：幸福结局\n\n## 3. 核心反转节点\n\n### 第二集结尾\n- **转折点内容**：林雨晴发现陈默是她大学时期暗恋的学长\n- **情感冲击力**：高\n- **剧情作用**：为后续情感发展埋下伏笔\n\n### 第四集结尾\n- **转折点内容**：林雨晴发现自己依赖的AI助手是陈默为她定制的\n- **情感冲击力**：高\n- **剧情作用**：揭示陈默的深情，推动情感发展\n\n### 第六集结尾\n- **转折点内容**：林雨晴面临职业晋升与情感选择的两难境地\n- **情感冲击力**：高\n- **剧情作用**：考验人物性格，推动最终抉择\n\n## 4. 主题与风格\n\n### 核心主题\n在科技高速发展的时代，如何保持人性的温度，平衡事业与情感\n\n### 文风配置\n- **文风类型**：都市情感\n- **文风名称**：温暖现实主义\n- **文风描述**：语言细腻真实，情感真挚动人，情节紧凑有张力\n\n## 5. 商业评估\n\n### 商业可行性\n- **市场潜力**：高，都市情感题材受众广泛，AI元素符合当前热点\n- **IP开发**：适合改编为电视剧、网剧等多种形式\n- **目标受众**：25-40岁都市白领，对情感和科技话题感兴趣的群体\n\n### 情感共鸣力\n- **情感触点**：职场压力、情感困惑、科技与人性的冲突\n- **共鸣强度**：高，能够引发目标受众的情感共鸣\n\n### 跨媒介改编潜力\n- **影视化**：适合改编为电视剧或网剧\n- **游戏化**：可开发为互动式剧情游戏\n- **衍生产品**：可开发周边产品如小说、剧本集等\n`;

        setCreativeDocument(mockCreativeDocument);
        setGenerationSuccess(true);
        message.success('创意框架生成成功');
        setLoading(false);
      }, 2000);
    } catch (error) {
      console.error('生成创意框架错误:', error);
      message.error('生成创意框架失败');
      setLoading(false);
    }
  };

  const handleNavigateToNovel = () => {
    // 存储创意文档到localStorage，传递给小说创作页面
    localStorage.setItem('creativeDocument', creativeDocument);
    // 导航到小说创作页面
    window.location.href = '/novel';
  };

  const handleCopyToClipboard = () => {
    navigator.clipboard.writeText(creativeDocument);
    message.success('创意框架已复制到剪贴板');
  };

  return (
    <Layout title="创意策划 - 小说创作智能体">
      <div className="space-y-8">
        {/* 页面标题 */}
        <div className="flex flex-col space-y-2">
          <Title level={2} className="m-0">创意策划</Title>
          <Text className="text-gray-600">基于市场热点生成故事创意框架</Text>
        </div>

        {/* 创意策划表单 */}
        <Card
          title={
            <Space>
              <FileTextOutlined style={{ color: '#1a365d' }} />
              <span className="text-lg font-semibold">创意策划表单</span>
            </Space>
          }
          variant="borderless"
          className="shadow-md"
          style={{ borderRadius: '12px' }}
        >
          <Form
            form={form}
            onFinish={handleGenerateCreative}
            layout="vertical"
            initialValues={{
              story_type: '都市情感',
              model: 'deepseek-chat',
              session_id: `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            }}
          >
            {/* 热点输入 */}
            <Form.Item label={
              <Space>
                <FireOutlined style={{ color: '#f59e0b' }} />
                <span className="font-medium">市场热点</span>
              </Space>
            }>
              <div className="space-y-4">
                <div className="flex gap-3">
                  <Input
                    value={hotspotInput}
                    onChange={(e) => setHotspotInput(e.target.value)}
                    placeholder="输入热点并按回车添加"
                    onPressEnter={handleAddHotspot}
                    className="flex-1"
                    size="large"
                    prefix={<PlusOutlined className="text-gray-400" />}
                  />
                  <Button 
                    type="primary" 
                    onClick={handleAddHotspot}
                    size="large"
                    icon={<PlusOutlined />}
                  >
                    添加
                  </Button>
                </div>
                <div className="flex flex-wrap gap-3">
                  {hotspots.map((hotspot, index) => (
                    <Tag 
                      key={index} 
                      closable 
                      onClose={() => handleRemoveHotspot(hotspot)}
                      style={{ 
                        borderRadius: '16px',
                        padding: '4px 12px',
                        fontSize: '14px',
                        backgroundColor: '#f0f4f8',
                        border: '1px solid #e2e8f0',
                      }}
                      closeIcon={<DeleteOutlined className="text-gray-500" />}
                    >
                      <Space size="small">
                        {hotspot}
                      </Space>
                    </Tag>
                  ))}
                  {hotspots.length === 0 && (
                    <Text className="text-gray-400 italic">
                      请添加市场热点，如：人工智能、职场压力、都市情感等
                    </Text>
                  )}
                </div>
              </div>
            </Form.Item>

            {/* 故事类型 */}
            <Form.Item
              name="story_type"
              label={
                <Space>
                  <BookOutlined style={{ color: '#1a365d' }} />
                  <span className="font-medium">故事类型</span>
                </Space>
              }
              rules={[{ required: true, message: '请选择故事类型' }]}
            >
              <Select 
                style={{ width: '100%' }}
                size="large"
                options={[
                  { value: '都市情感', label: '都市情感' },
                  { value: '职场奋斗', label: '职场奋斗' },
                  { value: '科幻未来', label: '科幻未来' },
                  { value: '历史穿越', label: '历史穿越' },
                  { value: '悬疑推理', label: '悬疑推理' },
                  { value: '奇幻冒险', label: '奇幻冒险' },
                  { value: '校园青春', label: '校园青春' },
                  { value: '武侠江湖', label: '武侠江湖' },
                ]}
              />
            </Form.Item>

            {/* 模型选择 */}
            <Form.Item
              name="model"
              label={
                <Space>
                  <SettingOutlined style={{ color: '#1a365d' }} />
                  <span className="font-medium">模型选择</span>
                </Space>
              }
            >
              <Select 
                style={{ width: '100%' }}
                size="large"
                options={[
                  { value: 'deepseek-chat', label: 'DeepSeek Chat' },
                  { value: 'qwen3-30b', label: 'Qwen3-30B' },
                  { value: 'gpt-4', label: 'GPT-4' },
                ]}
              />
            </Form.Item>

            {/* 会话ID */}
            <Form.Item
              name="session_id"
              label={
                <Space>
                  <span className="font-medium">会话ID</span>
                  <Tooltip title="用于标识当前会话，请勿修改">
                    <InfoCircleOutlined className="text-gray-400" />
                  </Tooltip>
                </Space>
              }
            >
              <Input 
                readOnly 
                size="large"
                suffix={<CopyOutlined className="text-gray-400 cursor-pointer" />}
              />
            </Form.Item>

            {/* 生成按钮 */}
            <Form.Item>
              <Button 
                type="primary" 
                htmlType="submit" 
                loading={loading}
                size="large"
                icon={<RocketOutlined />}
                className="w-full"
                style={{ 
                  height: '48px',
                  fontSize: '16px',
                  borderRadius: '8px',
                  backgroundColor: '#1a365d',
                }}
              >
                生成创意框架
              </Button>
            </Form.Item>
          </Form>
        </Card>

        {/* 创意文档 */}
        {creativeDocument && (
          <Card
            title={
              <Space>
                <FileTextOutlined style={{ color: '#1a365d' }} />
                <span className="text-lg font-semibold">创意框架文档</span>
              </Space>
            }
            variant="borderless"
            className="shadow-md"
            style={{ borderRadius: '12px' }}
            extra={
              <Space>
                <Button
                  icon={<CopyOutlined />}
                  onClick={handleCopyToClipboard}
                >
                  复制
                </Button>
                <Button
                  type="primary"
                  icon={<ArrowRightOutlined />}
                  onClick={handleNavigateToNovel}
                >
                  前往小说创作
                </Button>
              </Space>
            }
          >
            {loading ? (
              <Loading message="正在生成创意框架..." />
            ) : (
              <div className="space-y-6">
                {generationSuccess && (
                  <Alert
                    message="创意框架生成成功！"
                    type="success"
                    showIcon
                    action={
                      <Button size="small" onClick={handleNavigateToNovel}>
                        开始创作小说
                      </Button>
                    }
                    className="mb-4"
                  />
                )}
                <Divider />
                <Tabs defaultActiveKey="content">
                  <Tabs.TabPane tab="创意框架内容" key="content">
                    <div className="bg-gray-50 p-6 rounded-xl shadow-sm">
                      <pre className="whitespace-pre-wrap font-mono text-sm leading-relaxed text-gray-800">
                        {creativeDocument}
                      </pre>
                    </div>
                  </Tabs.TabPane>
                  <Tabs.TabPane tab="创作建议" key="suggestions">
                    <div className="space-y-4">
                      <Card size="small" variant="borderless">
                        <Title level={5}>创作建议</Title>
                        <ul className="list-disc pl-6 space-y-2 text-gray-700">
                          <li>保持人物性格的一致性，确保角色行为符合设定</li>
                          <li>注重细节描写，增强故事的真实感和代入感</li>
                          <li>合理安排情节节奏，张弛有度，避免情节拖沓</li>
                          <li>突出AI元素与情感主线的融合，避免科技元素喧宾夺主</li>
                          <li>结尾部分应给读者留下思考空间，增强故事的余韵</li>
                        </ul>
                      </Card>
                      <Card size="small" variant="borderless">
                        <Title level={5}>市场分析</Title>
                        <ul className="list-disc pl-6 space-y-2 text-gray-700">
                          <li>AI题材当前市场热度高，受众接受度强</li>
                          <li>都市情感题材受众广泛，市场潜力大</li>
                          <li>建议重点宣传AI与情感的结合点，突出故事的独特性</li>
                          <li>可考虑开发衍生产品，如短剧、有声书等</li>
                        </ul>
                      </Card>
                    </div>
                  </Tabs.TabPane>
                </Tabs>
                <Divider />
                <div className="flex justify-end gap-3">
                  <Button
                    type="primary"
                    size="large"
                    icon={<ArrowRightOutlined />}
                    onClick={handleNavigateToNovel}
                    style={{ 
                      backgroundColor: '#f59e0b',
                      borderColor: '#f59e0b',
                    }}
                  >
                    前往小说创作
                  </Button>
                </div>
              </div>
            )}
          </Card>
        )}
      </div>
    </Layout>
  );
};

// 缺少的图标组件
const InfoCircleOutlined = (props: any) => {
  return <SettingOutlined {...props} />;
};

export default Creative;