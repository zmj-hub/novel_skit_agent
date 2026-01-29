<template>
  <component
    :is="iconComponent"
    :class="iconClasses"
    :style="iconStyle"
  />
</template>

<script setup>
import { computed } from 'vue'
import * as HeroIcons from '@heroicons/vue/24/solid'
import * as HeroIconsOutline from '@heroicons/vue/24/outline'

const props = defineProps({
  name: { 
    type: String, 
    required: true,
    validator: (value) => {
      // 支持带后缀的图标名，如 'ChartPieIcon' 或 'ChartPieIconOutline'
      const baseName = value.replace('Outline', '')
      return HeroIcons[baseName] || HeroIconsOutline[baseName]
    }
  },
  size: { 
    type: String, 
    default: 'md',
    validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl'].includes(value)
  },
  color: { 
    type: String, 
    default: 'currentColor' 
  },
  className: { 
    type: String, 
    default: '' 
  },
})

const sizeMap = {
  xs: 'w-3 h-3',
  sm: 'w-4 h-4', 
  md: 'w-5 h-5',
  lg: 'w-6 h-6',
  xl: 'w-8 h-8',
}

const iconComponent = computed(() => {
  // 优先查找实心图标，如果没有则查找轮廓图标
  const solidIcon = HeroIcons[props.name]
  if (solidIcon) return solidIcon
  
  const outlineIcon = HeroIconsOutline[props.name]
  if (outlineIcon) return outlineIcon
  
  // 如果带Outline后缀，尝试查找基础名称
  if (props.name.endsWith('Outline')) {
    const baseName = props.name.replace('Outline', '')
    return HeroIconsOutline[baseName] || HeroIcons[baseName]
  }
  
  // 默认返回问号图标
  return HeroIcons['QuestionMarkCircleIcon']
})

const iconClasses = computed(() => {
  return [
    sizeMap[props.size] || sizeMap.md,
    props.className
  ].filter(Boolean).join(' ')
})

const iconStyle = computed(() => ({
  color: props.color
}))
</script>

<style scoped>
/* 确保图标不会意外放大 */
svg {
  max-width: 10%;
  max-height: 10%;
}
</style>