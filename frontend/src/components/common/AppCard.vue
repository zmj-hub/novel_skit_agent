<template>
  <div 
    :class="[
      'bg-white rounded-xl shadow-card border border-gray-100',
      'transition-all duration-300',
      hoverable && 'hover:shadow-hover hover:-translate-y-0.5 cursor-pointer',
      className
    ]"
    @click="$emit('click', $event)"
  >
    <!-- 卡片头部 -->
    <div v-if="$slots.header || title" class="px-6 py-4 border-b border-gray-100">
      <slot name="header">
        <div class="flex items-center gap-3">
          <AppIcon v-if="icon" :name="icon" size="md" class="text-primary-500" />
          <h3 class="text-lg font-semibold text-gray-900">{{ title }}</h3>
        </div>
      </slot>
    </div>
    
    <!-- 卡片内容 -->
    <div :class="contentClass">
      <slot />
    </div>
    
    <!-- 卡片底部 -->
    <div v-if="$slots.footer" class="px-6 py-4 border-t border-gray-100">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import AppIcon from './AppIcon.vue'

const props = defineProps({
  title: { 
    type: String, 
    default: '' 
  },
  icon: { 
    type: String, 
    default: '' 
  },
  hoverable: { 
    type: Boolean, 
    default: false 
  },
  className: { 
    type: String, 
    default: '' 
  },
  padding: { 
    type: String, 
    default: 'normal',
    validator: (value) => ['none', 'small', 'normal', 'large'].includes(value)
  },
})

defineEmits(['click'])

const paddingMap = {
  none: '',
  small: 'p-4',
  normal: 'p-6',
  large: 'p-8',
}

const contentClass = computed(() => {
  // 如果有header，内容区域不需要顶部padding
  const hasHeader = props.title || props.$slots?.header
  const basePadding = paddingMap[props.padding] || paddingMap.normal
  
  if (hasHeader) {
    return basePadding.replace('p-', 'px-6 pb-6 pt-4')
  }
  return basePadding
})
</script>