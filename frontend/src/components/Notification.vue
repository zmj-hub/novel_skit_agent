<script setup>
import { message } from 'ant-design-vue'

// 配置全局消息组件
message.config({
  maxCount: 3,
  duration: 3
})

// 导出消息方法
defineExpose({
  success: (content) => message.success(content),
  error: (content) => message.error(content),
  warning: (content) => message.warning(content),
  info: (content) => message.info(content)
})
</script>