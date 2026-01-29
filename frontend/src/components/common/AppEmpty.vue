<template>
  <div class="flex flex-col items-center justify-center py-12 text-center">
    <div class="w-16 h-16 mb-4 rounded-full bg-gray-100 flex items-center justify-center">
      <AppIcon name="InboxIcon" size="xl" class="text-gray-400" />
    </div>
    <h3 class="text-lg font-medium text-gray-900 mb-1">{{ title }}</h3>
    <p class="text-sm text-gray-500 max-w-xs">{{ description }}</p>
    <slot />
  </div>
</template>

<script setup>
import AppIcon from './AppIcon.vue'

const props = defineProps({
  title: { 
    type: String, 
    default: '暂无数据' 
  },
  description: { 
    type: String, 
    default: '当前没有可显示的数据' 
  },
})
</script>