import React, { useState, useEffect } from 'react';
import { Typography, Form, Input, Select, Button, message, Divider, Space, Card, Alert, Tabs, Descriptions, Table, Progress, Badge } from 'antd';
import { BookOutlined, SettingsOutlined, FileTextOutlined, DownloadOutlined, ArrowLeftOutlined, RocketOutlined, CopyOutlined, EditOutlined, EyeOutlined } from '@ant-design/icons';
import Layout from '../../components/layout/Layout';
import Loading from '../../components/common/Loading';
import api from '../../services/api';
import endpoints from '../../services/endpoints';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;

interface NovelChapter {
  chapter_number: number;
  chapter_title: string;
  chapter_content: string;
  suspense_hook: string;
}

const Novel: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState<boolean>(false);
  const [novelContent, setNovelContent] = useState<string>('');
  const [chapters, setChapters] = useState<NovelChapter[]>([]);
  const [wordCount, setWordCount] = useState<number>(0);
  const [generationSuccess, setGenerationSuccess] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<string>('content');

  // 从localStorage加载创意框架（如果可用）
  useEffect(() => {
    const savedCreativeDocument = localStorage.getItem('creativeDocument');
    if (savedCreativeDocument) {
      form.setFieldsValue({ creative_framework: savedCreativeDocument });
    }
  }, [form]);

  const handleGenerateNovel = async (values: any) => {
    setLoading(true);
    setGenerationSuccess(false);

    try {
      // const response = await api.post(endpoints.novel.write, {
      //   creative_framework: values.creative_framework,
      //   style: values.style,
      //   chapter_count: values.chapter_count,
      //   session_id: values.session_id,
      //   model: values.model,
      // });

      // 模拟API响应
      setTimeout(() => {
        const mockNovelContent = `# 《AI时代的情感抉择》

## 第一章：职场危机

林雨晴站在公司楼下，看着眼前熟悉的玻璃幕墙建筑，心中五味杂陈。今天是她加入这家AI公司的第三个年头，也是她晋升为产品经理的第一天。但此刻，她的心情却一点也不轻松。

"雨晴，你来了！"身后传来一个熟悉的声音。

林雨晴转身，看到陈默正朝着她走来。陈默是公司的AI研发工程师，平时话不多，但技术实力很强。林雨晴对他印象不错，因为他总是能在关键时刻解决技术问题。

"早，陈默。"林雨晴微笑着打招呼。

"恭喜你晋升。"陈默的语气依旧平淡，但眼中闪过一丝真诚的祝福。

"谢谢。"林雨晴点点头，"不过今天的会议可能会很棘手，听说我们的AI助手项目遇到了瓶颈。"

陈默的表情变得严肃起来："我知道，昨天我已经查看了代码，确实有一些问题需要解决。"

两人一边说着，一边走进了电梯。电梯里，林雨晴突然想起了什么："对了，陈默，你是哪年毕业的？我总觉得我们好像在哪里见过。"

陈默的身体微微一僵，眼神闪烁了一下："可能是在行业会议上吧。"他的声音低了下去，似乎不太愿意多谈这个话题。

林雨晴敏锐地察觉到了他的变化，但没有追问。电梯门打开，两人朝着会议室走去，准备迎接新一天的挑战。

## 第二章：意外相遇

会议结束后，林雨晴感到有些疲惫。项目的问题比她想象的还要严重，团队需要在一个月内完成AI助手的升级，否则可能会失去重要的客户。

她决定去楼下的咖啡店买杯咖啡，放松一下心情。当她走进咖啡店时，却意外地看到了陈默坐在角落的位置上，面前放着一台笔记本电脑，正在专注地敲击键盘。

"陈默，这么巧？"林雨晴走过去打招呼。

陈默抬头，看到是她，露出了一个淡淡的微笑："嗯，来这里查资料。"他合上笔记本，示意她坐下。

林雨晴坐下后，点了一杯拿铁。"你在研究什么？"她好奇地问。

"关于AI助手的情感识别模块，我觉得我们可以改进算法，让它更准确地理解用户的情绪。"陈默解释道。

"情感识别？这是个好方向。"林雨晴眼睛一亮，"如果我们能让AI助手更懂用户的情感，产品的竞争力会大大提升。"

陈默点了点头："我也是这么想的。其实，我已经做了一些初步的实验，效果还不错。"

两人越聊越投机，不知不觉中，时间已经过去了一个多小时。当林雨晴看了看手表，惊讶地发现已经快到下班时间了。

"时间过得真快！"她感叹道，"今天谢谢你的分享，让我对项目有了新的思路。"

"不用客气。"陈默站起身，"其实，我一直很欣赏你的工作能力，你对产品的理解很深刻。"

林雨晴有些意外，她没想到平时沉默寡言的陈默会说出这样的话。"谢谢，我也很佩服你的技术实力。"她真诚地说。

两人走出咖啡店，夕阳西下，金色的阳光洒在街道上。林雨晴突然觉得，这个平时熟悉的城市，似乎有了一些不同的味道。

## 第三章：情感纠葛

接下来的日子里，林雨晴和陈默的接触越来越多。他们经常一起讨论项目，一起加班，一起解决问题。在这个过程中，林雨晴发现自己对陈默产生了一种特殊的感觉。

一天晚上，两人加班到很晚，办公室里只剩下他们两个人。林雨晴伸了个懒腰，看着窗外的夜景："没想到加班也能看到这么美的夜景。"

陈默走到她身边，顺着她的目光望去："是啊，平时很少有机会这样看城市的夜景。"

两人静静地站了一会儿，陈默突然开口："雨晴，我有件事想告诉你。"

林雨晴转过头，看着他认真的表情："什么事？"

"其实，我们不是第一次见面。"陈默的声音有些紧张，"大学的时候，我们是同校的，我比你高两届。"

林雨晴愣住了，仔细回忆着大学时代的往事。突然，她想起了一个熟悉的身影："你是那个经常在图书馆学习的学长？"

陈默点了点头："没错，那时候我就注意到你了，你总是坐在靠窗的位置，认真地看书。"

林雨晴的心跳加速了，她没想到，这个平时沉默寡言的同事，竟然是自己大学时代暗恋过的学长。

"我一直想告诉你，但又担心会影响我们的工作关系。"陈默继续说，"现在，我觉得我应该说出来，因为我不想错过你。"

林雨晴的眼眶湿润了，她没想到，自己埋藏在心底多年的感情，竟然会以这样的方式重新浮现。

就在这时，林雨晴的手机突然响了起来，打破了这温馨的氛围。她接起电话，是公司的紧急通知，AI助手的测试出现了严重的问题，需要她立即处理。

林雨晴的表情变得严肃起来，她看了看陈默："对不起，我需要去处理一个紧急问题。"

陈默理解地点了点头："去吧，工作重要。"他的眼中闪过一丝失落，但很快又恢复了平静。

林雨晴抓起包，匆匆离开了办公室，留下陈默一个人站在原地，看着她离去的背影。

## 第四章：AI助手的秘密

接下来的几天，林雨晴一直忙于处理项目的问题，没有时间和陈默单独相处。她的心里充满了矛盾，一方面，她对陈默有着深厚的感情；另一方面，她不想因为个人感情影响工作。

一天，当她正在测试AI助手时，突然发现了一个奇怪的现象。每当她输入特定的关键词时，AI助手的回答会变得特别贴心，就像知道她的喜好一样。

林雨晴觉得有些奇怪，她找到陈默："陈默，我发现AI助手的回答有些异常，你能帮我检查一下代码吗？"

陈默看了看她测试的结果，脸色突然变得苍白。"这...这是我为你定制的版本。"他吞吞吐吐地承认。

"为我定制的？"林雨晴惊讶地问。

陈默点了点头："我在AI助手的代码中添加了一些特殊的逻辑，让它能够根据你的喜好调整回答。我知道这样做不符合公司的规定，但我想让你在工作中更轻松一些。"

林雨晴被他的用心打动了，她看着陈默真诚的眼睛："谢谢你，陈默。你总是这样默默地关心我。"

陈默终于鼓起勇气，握住了她的手："雨晴，我喜欢你，从大学时代就开始了。我知道现在不是谈感情的时候，但我不想再隐瞒自己的心意。"

林雨晴的心跳加速了，她看着陈默的手，感受着他的温度："我...我也喜欢你。"她轻声说。

两人的手紧紧地握在一起，仿佛找到了彼此生命中最重要的人。

## 第五章：抉择时刻

就在两人感情升温的时候，公司的项目也进入了关键阶段。AI助手的升级进展顺利，林雨晴和陈默的合作也越来越默契。

然而，就在项目即将完成的时候，林雨晴收到了一个意外的消息。她被提名参加公司的高层管理培训，这意味着她可能会被调往总部工作。

这个消息让林雨晴陷入了两难的境地。一方面，这是她职业发展的重要机会；另一方面，她不想离开陈默。

她找到陈默，将这个消息告诉了他。"我该怎么办？"她问道，眼中充满了迷茫。

陈默沉默了一会儿，然后认真地说："雨晴，这是一个难得的机会，你应该去。你的能力很强，应该有更广阔的发展空间。"

"可是，我不想离开你。"林雨晴的声音有些哽咽。

陈默伸手擦去她脸上的泪水："我们的感情不会因为距离而改变。我会等你，等你回来。"

林雨晴看着他坚定的眼神，心中充满了感动。她知道，陈默是真心为她着想。

最终，林雨晴决定接受这个机会。在她离开的前一天，两人来到了他们第一次相遇的咖啡店。

"等我回来，我们就在一起，再也不分开。"林雨晴说。

"好，我等你。"陈默握住她的手，眼中充满了期待。

两人相视而笑，仿佛看到了未来的美好。

## 第六章：真相大白

在总部的培训期间，林雨晴一直和陈默保持着联系。他们每天都会视频通话，分享各自的生活。

一天，当林雨晴正在查看公司的内部资料时，突然发现了一个惊人的秘密。原来，陈默是公司创始人的儿子，他隐瞒身份进入公司，是为了了解公司的实际情况，为将来接管公司做准备。

林雨晴感到震惊，她立即给陈默打电话："陈默，你为什么要隐瞒自己的身份？"

陈默沉默了一会儿，然后坦白了一切："我不想因为我的身份而得到特殊待遇，我想通过自己的努力证明自己的能力。"

"那你为什么不告诉我？"林雨晴有些生气。

"我害怕你会因此改变对我的看法。"陈默解释道，"我喜欢你，是因为你是一个独立、坚强的女性，我不想因为我的身份而影响我们的感情。"

林雨晴的情绪逐渐平静下来，她理解陈默的用心。"我明白了，我不会因为你的身份而改变对你的感情。"她真诚地说。

陈默松了一口气："谢谢你的理解。其实，我已经向父亲提出了辞职，我想和你一起创办一家属于我们自己的AI公司，专注于情感智能的研究。"

林雨晴惊喜地问："真的？你愿意为了我放弃继承公司？"

"当然，因为你比任何东西都重要。"陈默坚定地说。

林雨晴的眼眶湿润了，她知道，自己找到了一个值得托付终身的人。

## 第七章：新的开始

培训结束后，林雨晴回到了公司。她和陈默一起辞了职，创办了一家名为"心影智能"的AI公司，专注于情感智能的研究。

他们的公司发展迅速，很快就推出了一款名为"心影"的AI助手，它能够准确地理解用户的情感，成为了市场上的爆款产品。

一年后，林雨晴和陈默在海边举行了婚礼。阳光、沙滩、海浪，一切都那么美好。

"谢谢你，陈默，谢谢你为我做的一切。"林雨晴望着陈默，眼中充满了幸福。

"应该是我谢谢你，雨晴，是你让我找到了人生的方向。"陈默握住她的手，深情地说。

两人相视而笑，在亲友的祝福声中，开始了他们新的生活。

他们知道，未来的路可能会有挑战，但只要他们在一起，就没有什么困难是克服不了的。因为他们相信，爱情的力量是无穷的，而AI的发展，也会因为注入了人类的情感而变得更加美好。

— 全文完 —
`;

        const mockChapters: NovelChapter[] = [
          {
            chapter_number: 1,
            chapter_title: '第一章：职场危机',
            chapter_content: '林雨晴站在公司楼下，看着眼前熟悉的玻璃幕墙建筑，心中五味杂陈。今天是她加入这家AI公司的第三个年头，也是她晋升为产品经理的第一天。但此刻，她的心情却一点也不轻松。...',
            suspense_hook: '陈默的身体微微一僵，眼神闪烁了一下："可能是在行业会议上吧。"他的声音低了下去，似乎不太愿意多谈这个话题。'
          },
          {
            chapter_number: 2,
            chapter_title: '第二章：意外相遇',
            chapter_content: '会议结束后，林雨晴感到有些疲惫。项目的问题比她想象的还要严重，团队需要在一个月内完成AI助手的升级，否则可能会失去重要的客户。...',
            suspense_hook: '林雨晴的心跳加速了，她没想到，自己埋藏在心底多年的感情，竟然会以这样的方式重新浮现。'
          },
          {
            chapter_number: 3,
            chapter_title: '第三章：情感纠葛',
            chapter_content: '接下来的日子里，林雨晴和陈默的接触越来越多。他们经常一起讨论项目，一起加班，一起解决问题。在这个过程中，林雨晴发现自己对陈默产生了一种特殊的感觉。...',
            suspense_hook: '陈默看了看她，眼中闪过一丝失落，但很快又恢复了平静。'
          },
          {
            chapter_number: 4,
            chapter_title: '第四章：AI助手的秘密',
            chapter_content: '接下来的几天，林雨晴一直忙于处理项目的问题，没有时间和陈默单独相处。她的心里充满了矛盾，一方面，她对陈默有着深厚的感情；另一方面，她不想因为个人感情影响工作。...',
            suspense_hook: '两人的手紧紧地握在一起，仿佛找到了彼此生命中最重要的人。'
          },
          {
            chapter_number: 5,
            chapter_title: '第五章：抉择时刻',
            chapter_content: '就在两人感情升温的时候，公司的项目也进入了关键阶段。AI助手的升级进展顺利，林雨晴和陈默的合作也越来越默契。...',
            suspense_hook: '两人相视而笑，仿佛看到了未来的美好。'
          },
          {
            chapter_number: 6,
            chapter_title: '第六章：真相大白',
            chapter_content: '在总部的培训期间，林雨晴一直和陈默保持着联系。他们每天都会视频通话，分享各自的生活。...',
            suspense_hook: '林雨晴的眼眶湿润了，她知道，自己找到了一个值得托付终身的人。'
          },
          {
            chapter_number: 7,
            chapter_title: '第七章：新的开始',
            chapter_content: '培训结束后，林雨晴回到了公司。她和陈默一起辞了职，创办了一家名为"心影智能"的AI公司，专注于情感智能的研究。...',
            suspense_hook: '因为他们相信，爱情的力量是无穷的，而AI的发展，也会因为注入了人类的情感而变得更加美好。'
          },
        ];

        setNovelContent(mockNovelContent);
        setWordCount(mockNovelContent.length);
        setChapters(mockChapters);
        setGenerationSuccess(true);
        message.success('小说生成成功！');
        setLoading(false);
      }, 2000);
    } catch (error) {
      console.error('生成小说错误:', error);
      message.error('生成小说失败');
      setLoading(false);
    }
  };

  const handleExportNovel = async (format: string = 'txt') => {
    const sessionId = form.getFieldValue('session_id');
    if (!sessionId) {
      message.error('需要会话ID');
      return;
    }

    setLoading(true);
    try {
      // const response = await api.post(`${endpoints.novel.export.replace('{session_id}', sessionId)}?format=${format}`);
      message.success(`小说已成功导出为${format}格式！`);
    } catch (error) {
      console.error('导出小说错误:', error);
      message.error('导出小说失败');
    } finally {
      setLoading(false);
    }
  };

  const handleGetChapters = async () => {
    const sessionId = form.getFieldValue('session_id');
    if (!sessionId) {
      message.error('需要会话ID');
      return;
    }

    setLoading(true);
    try {
      // const response = await api.get(endpoints.novel.chapters.replace('{session_id}', sessionId));
      // setChapters(response.chapters || []);
      message.success('章节获取成功！');
    } catch (error) {
      console.error('获取章节错误:', error);
      message.error('获取章节失败');
    } finally {
      setLoading(false);
    }
  };

  const handleBackToCreative = () => {
    window.location.href = '/creative';
  };

  const handleCopyNovel = () => {
    navigator.clipboard.writeText(novelContent);
    message.success('小说内容已复制到剪贴板');
  };

  return (
    <Layout title="小说创作 - 小说创作智能体">
      <div className="space-y-8">
        {/* 页面标题 */}
        <div className="flex flex-col space-y-2">
          <Title level={2} className="m-0">小说创作</Title>
          <Text className="text-gray-600">基于创意框架生成小说内容</Text>
        </div>

        {/* 小说创作表单 */}
        <Card
          title={
            <Space>
              <BookOutlined style={{ color: '#1a365d' }} />
              <span className="text-lg font-semibold">小说创作表单</span>
            </Space>
          }
          variant="borderless"
          className="shadow-md"
          style={{ borderRadius: '12px' }}
        >
          <Form
            form={form}
            onFinish={handleGenerateNovel}
            layout="vertical"
            initialValues={{
              style: 'urban',
              chapter_count: 5,
              model: 'deepseek-chat',
              session_id: `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            }}
          >
            {/* 创意框架 */}
            <Form.Item
              name="creative_framework"
              label={
                <Space>
                  <FileTextOutlined style={{ color: '#1a365d' }} />
                  <span className="font-medium">创意框架</span>
                </Space>
              }
              rules={[{ required: true, message: '请输入创意框架' }]}
            >
              <TextArea
                placeholder="输入创意框架或粘贴来自创意策划的内容"
                rows={8}
                maxLength={5000}
                size="large"
                showCount
              />
              <Text type="secondary" className="block mt-2">
                请在此粘贴创意框架，或使用来自创意策划页面的内容
              </Text>
            </Form.Item>

            {/* 文风选择 */}
            <Form.Item
              name="style"
              label={
                <Space>
                  <SettingsOutlined style={{ color: '#1a365d' }} />
                  <span className="font-medium">文风类型</span>
                </Space>
              }
              rules={[{ required: true, message: '请选择文风类型' }]}
            >
              <Select 
                style={{ width: '100%' }}
                size="large"
                options={[
                  { value: 'urban', label: '都市风格' },
                  { value: 'sweet', label: '甜宠风格' },
                  { value: 'suspense', label: '悬疑风格' },
                  { value: 'fantasy', label: '奇幻风格' },
                  { value: 'historical', label: '历史风格' },
                  { value: 'scifi', label: '科幻风格' },
                ]}
              />
            </Form.Item>

            {/* 章节数量 */}
            <Form.Item
              name="chapter_count"
              label={
                <Space>
                  <BookOutlined style={{ color: '#1a365d' }} />
                  <span className="font-medium">章节数量</span>
                </Space>
              }
              rules={[{ required: true, message: '请输入章节数量' }]}
            >
              <Input 
                type="number" 
                min={1} 
                max={20} 
                placeholder="输入章节数量"
                size="large"
              />
            </Form.Item>

            {/* 模型选择 */}
            <Form.Item
              name="model"
              label={
                <Space>
                  <SettingsOutlined style={{ color: '#1a365d' }} />
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
              label="会话ID"
            >
              <Input 
                readOnly 
                size="large"
                suffix={<CopyOutlined className="text-gray-400 cursor-pointer" />}
              />
            </Form.Item>

            {/* 操作按钮 */}
            <Form.Item>
              <Space className="w-full">
                <Button 
                  onClick={handleBackToCreative}
                  size="large"
                  icon={<ArrowLeftOutlined />}
                >
                  返回创意策划
                </Button>
                <Button 
                  type="primary" 
                  htmlType="submit" 
                  loading={loading}
                  size="large"
                  icon={<RocketOutlined />}
                  className="flex-1"
                  style={{ 
                    height: '48px',
                    fontSize: '16px',
                    borderRadius: '8px',
                    backgroundColor: '#1a365d',
                  }}
                >
                  生成小说
                </Button>
              </Space>
            </Form.Item>
          </Form>
        </Card>

        {/* 小说内容 */}
        {novelContent && (
          <Card
            title={
              <Space>
                <BookOutlined style={{ color: '#1a365d' }} />
                <span className="text-lg font-semibold">小说内容</span>
              </Space>
            }
            variant="borderless"
            className="shadow-md"
            style={{ borderRadius: '12px' }}
            extra={
              <Space>
                <Button
                  icon={<CopyOutlined />}
                  onClick={handleCopyNovel}
                >
                  复制
                </Button>
                <Button
                  icon={<DownloadOutlined />}
                  onClick={() => handleExportNovel('txt')}
                >
                  导出TXT
                </Button>
                <Button
                  type="primary"
                  icon={<DownloadOutlined />}
                  onClick={() => handleExportNovel('pdf')}
                >
                  导出PDF
                </Button>
              </Space>
            }
          >
            {loading ? (
              <Loading message="正在生成小说..." />
            ) : (
              <div className="space-y-6">
                {generationSuccess && (
                  <Alert
                    message="小说生成成功！"
                    type="success"
                    showIcon
                    className="mb-4"
                  />
                )}
                <Divider />
                <Descriptions column={3} bordered>
                  <Descriptions.Item label="字数" span={1}>
                    <Badge count={wordCount} showZero color="blue" />
                  </Descriptions.Item>
                  <Descriptions.Item label="文风" span={1}>
                    {form.getFieldValue('style') === 'urban' && '都市风格'}
                    {form.getFieldValue('style') === 'sweet' && '甜宠风格'}
                    {form.getFieldValue('style') === 'suspense' && '悬疑风格'}
                    {form.getFieldValue('style') === 'fantasy' && '奇幻风格'}
                    {form.getFieldValue('style') === 'historical' && '历史风格'}
                    {form.getFieldValue('style') === 'scifi' && '科幻风格'}
                  </Descriptions.Item>
                  <Descriptions.Item label="章节" span={1}>
                    {form.getFieldValue('chapter_count')}
                  </Descriptions.Item>
                </Descriptions>
                <Divider />
                <Tabs activeKey={activeTab} onChange={setActiveTab}>
                  <Tabs.TabPane tab="全文内容" key="content">
                    <div className="bg-gray-50 p-6 rounded-xl shadow-sm">
                      <pre className="whitespace-pre-wrap font-mono text-sm leading-relaxed text-gray-800">
                        {novelContent}
                      </pre>
                    </div>
                  </Tabs.TabPane>
                  <Tabs.TabPane tab="章节管理" key="chapters">
                    <Space className="mb-6">
                      <Button 
                        onClick={handleGetChapters}
                        icon={<EyeOutlined />}
                      >
                        刷新章节
                      </Button>
                    </Space>
                    {chapters.length > 0 ? (
                      <Table
                        dataSource={chapters}
                        columns={[
                          {
                            title: '章节',
                            dataIndex: 'chapter_number',
                            key: 'chapter_number',
                            width: 80,
                          },
                          {
                            title: '标题',
                            dataIndex: 'chapter_title',
                            key: 'chapter_title',
                            width: 180,
                          },
                          {
                            title: '内容',
                            dataIndex: 'chapter_content',
                            key: 'chapter_content',
                            ellipsis: true,
                            flex: 1,
                          },
                          {
                            title: '悬念钩子',
                            dataIndex: 'suspense_hook',
                            key: 'suspense_hook',
                            ellipsis: true,
                            flex: 1,
                          },
                          {
                            title: '操作',
                            key: 'actions',
                            width: 120,
                            render: () => (
                              <Space>
                                <Button icon={<EditOutlined />} size="small" />
                                <Button icon={<CopyOutlined />} size="small" />
                              </Space>
                            ),
                          },
                        ]}
                        rowKey="chapter_number"
                        pagination={{
                          pageSize: 10,
                        }}
                      />
                    ) : (
                      <Text className="text-gray-400 italic">点击"刷新章节"查看章节详情</Text>
                    )}
                  </Tabs.TabPane>
                  <Tabs.TabPane tab="质量评估" key="quality">
                    <div className="space-y-4">
                      <Card size="small" variant="borderless">
                        <Title level={5}>质量评估</Title>
                        <div className="space-y-4">
                          <div>
                            <div className="flex justify-between mb-1">
                              <Text>完读率影响因素</Text>
                              <Text strong>95%</Text>
                            </div>
                            <Progress percent={95} status="success" />
                            <ul className="list-disc pl-6 mt-2 text-gray-700">
                              <li>情节吸引力强</li>
                              <li>人物塑造立体</li>
                              <li>冲突设计合理</li>
                              <li>情感描写细腻</li>
                            </ul>
                          </div>
                          <div>
                            <div className="flex justify-between mb-1">
                              <Text>文风一致性</Text>
                              <Text strong>92%</Text>
                            </div>
                            <Progress percent={92} status="success" />
                          </div>
                          <div>
                            <div className="flex justify-between mb-1">
                              <Text>悬念钩子有效性</Text>
                              <Text strong>88%</Text>
                            </div>
                            <Progress percent={88} status="active" />
                          </div>
                          <div>
                            <div className="flex justify-between mb-1">
                              <Text>整体评分</Text>
                              <Text strong>92</Text>
                            </div>
                            <Progress percent={92} status="success" />
                          </div>
                        </div>
                      </Card>
                      <Card size="small" variant="borderless">
                        <Title level={5}>优化建议</Title>
                        <ul className="list-disc pl-6 space-y-2 text-gray-700">
                          <li>增加细节描写，增强故事的画面感</li>
                          <li>强化情感渲染，让读者更能感同身受</li>
                          <li>适当增加次要角色，丰富故事层次</li>
                          <li>优化章节过渡，使情节更加流畅</li>
                        </ul>
                      </Card>
                    </div>
                  </Tabs.TabPane>
                </Tabs>
              </div>
            )}
          </Card>
        )}
      </div>
    </Layout>
  );
};

export default Novel;