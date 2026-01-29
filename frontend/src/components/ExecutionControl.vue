<template>
  <a-card hoverable>
    <template #title>
      <div class="flex items-center">
        <ControlOutlined style="margin-right: 8px; color: #1890ff" />
        <span class="text-xl font-semibold">执行控制</span>
      </div>
    </template>
    
    <a-form layout="vertical">
      <a-form-item label="任务目标">
        <a-input 
          v-model:value="taskGoal" 
          placeholder="输入任务目标，例如：生成一个关于人工智能的故事创意，并撰写短篇小说"
          prefix="🎯"
        />
      </a-form-item>
      
      <a-form-item label="会话ID">
        <a-input 
          v-model:value="sessionId" 
          placeholder="输入会话ID，例如：user_123"
          prefix="#"
        />
      </a-form-item>
      
      <a-form-item label="默认模型">
        <a-select v-model:value="model">
          <a-select-option value="qwen3-30b-a3b">ModelScope 千问3-30b-a3b</a-select-option>
          <a-select-option value="qwen3-72b-a3b">ModelScope 千问3-72b-a3b</a-select-option>
          <a-select-option value="llama3-8b">ModelScope LLaMA3-8B</a-select-option>
          <a-select-option value="llama3-70b">ModelScope LLaMA3-70B</a-select-option>
          <a-select-option value="gemini-pro">ModelScope Gemini Pro</a-select-option>
          <a-select-option value="deepseek-chat">DeepSeek Chat</a-select-option>
          <a-select-option value="gpt-3.5-turbo">GPT-3.5 Turbo</a-select-option>
          <a-select-option value="gpt-4">GPT-4</a-select-option>
        </a-select>
      </a-form-item>
      
      <a-divider orientation="left">智能体模型配置</a-divider>
      
      <a-form-item label="创意策划智能体">
        <a-select v-model:value="models.creative">
          <a-select-option value="qwen3-30b-a3b">ModelScope 千问3-30b-a3b</a-select-option>
          <a-select-option value="qwen3-72b-a3b">ModelScope 千问3-72b-a3b</a-select-option>
          <a-select-option value="llama3-8b">ModelScope LLaMA3-8B</a-select-option>
          <a-select-option value="llama3-70b">ModelScope LLaMA3-70B</a-select-option>
          <a-select-option value="gemini-pro">ModelScope Gemini Pro</a-select-option>
          <a-select-option value="deepseek-chat">DeepSeek Chat</a-select-option>
        </a-select>
      </a-form-item>
      
      <a-form-item label="故事剧本智能体">
        <a-select v-model:value="models.story_script">
          <a-select-option value="qwen3-30b-a3b">ModelScope 千问3-30b-a3b</a-select-option>
          <a-select-option value="qwen3-72b-a3b">ModelScope 千问3-72b-a3b</a-select-option>
          <a-select-option value="llama3-8b">ModelScope LLaMA3-8B</a-select-option>
          <a-select-option value="llama3-70b">ModelScope LLaMA3-70B</a-select-option>
          <a-select-option value="gemini-pro">ModelScope Gemini Pro</a-select-option>
          <a-select-option value="deepseek-chat">DeepSeek Chat</a-select-option>
        </a-select>
      </a-form-item>
      
      <a-form-item label="协调智能体">
        <a-select v-model:value="models.coordination">
          <a-select-option value="qwen3-30b-a3b">ModelScope 千问3-30b-a3b</a-select-option>
          <a-select-option value="qwen3-72b-a3b">ModelScope 千问3-72b-a3b</a-select-option>
          <a-select-option value="llama3-8b">ModelScope LLaMA3-8B</a-select-option>
          <a-select-option value="llama3-70b">ModelScope LLaMA3-70B</a-select-option>
          <a-select-option value="gemini-pro">ModelScope Gemini Pro</a-select-option>
          <a-select-option value="deepseek-chat">DeepSeek Chat</a-select-option>
        </a-select>
      </a-form-item>
      
      <a-form-item label="超时时间（秒）">
        <a-input-number 
          v-model:value="timeout" 
          :min="1" 
          :max="3600"
          style="width: 100%"
        />
      </a-form-item>
      
      <a-form-item label="优先级">
        <a-input-number 
          v-model:value="priority" 
          :min="1" 
          :max="5"
          style="width: 100%"
        />
      </a-form-item>
      
      <a-form-item label="文风类型">
        <a-select v-model:value="writingStyle">
          <a-select-option value="sweet">甜宠风格</a-select-option>
          <a-select-option value="suspense">悬疑风格</a-select-option>
          <a-select-option value="counterattack">逆袭风格</a-select-option>
          <a-select-option value="urban">都市风格</a-select-option>
          <a-select-option value="fantasy">奇幻风格</a-select-option>
        </a-select>
      </a-form-item>
      
      <a-form-item label="媒介类型">
        <a-select v-model:value="mediumType">
          <a-select-option value="novel">小说</a-select-option>
          <a-select-option value="screenplay">电影剧本</a-select-option>
          <a-select-option value="stage_play">舞台剧剧本</a-select-option>
          <a-select-option value="short_play">短剧剧本</a-select-option>
        </a-select>
      </a-form-item>
      
      <a-form-item label="章节/场景数量">
        <a-input-number 
          v-model:value="chapterCount" 
          :min="1" 
          :max="20"
          style="width: 100%"
        />
      </a-form-item>
    </a-form>
  </a-card>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Card, Form, Input, Select, InputNumber } from 'ant-design-vue'
import { ControlOutlined } from '@ant-design/icons-vue'

const props = defineProps({
  defaultValues: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:taskGoal', 'update:sessionId', 'update:model', 'update:timeout', 'update:priority', 'update:writingStyle', 'update:mediumType', 'update:chapterCount', 'update:models'])

const taskGoal = ref(props.defaultValues.taskGoal || '生成一个关于人工智能的故事创意，并创作故事剧本')
const sessionId = ref(props.defaultValues.sessionId || 'user_' + Math.random().toString(36).substr(2, 9))
const model = ref(props.defaultValues.model || 'qwen3-30b-a3b')
const timeout = ref(props.defaultValues.timeout || 300)
const priority = ref(props.defaultValues.priority || 3)
const writingStyle = ref(props.defaultValues.writingStyle || 'urban')
const mediumType = ref(props.defaultValues.mediumType || 'novel')
const chapterCount = ref(props.defaultValues.chapterCount || 5)
const models = ref({
  creative: props.defaultValues.models?.creative || 'qwen3-30b-a3b',
  story_script: props.defaultValues.models?.story_script || 'qwen3-30b-a3b',
  coordination: props.defaultValues.models?.coordination || 'qwen3-30b-a3b'
})

// 监听值变化并触发更新事件
watch(taskGoal, (newValue) => {
  emit('update:taskGoal', newValue)
})

watch(sessionId, (newValue) => {
  emit('update:sessionId', newValue)
})

watch(model, (newValue) => {
  emit('update:model', newValue)
})

watch(timeout, (newValue) => {
  emit('update:timeout', newValue)
})

watch(priority, (newValue) => {
  emit('update:priority', newValue)
})

watch(writingStyle, (newValue) => {
  emit('update:writingStyle', newValue)
})

watch(mediumType, (newValue) => {
  emit('update:mediumType', newValue)
})

watch(chapterCount, (newValue) => {
  emit('update:chapterCount', newValue)
})

watch(models, (newValue) => {
  emit('update:models', newValue)
}, { deep: true })

// 暴露方法给父组件
defineExpose({
  taskGoal,
  sessionId,
  model,
  timeout,
  priority,
  writingStyle,
  mediumType,
  chapterCount,
  models
})
</script>