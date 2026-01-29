<template>
  <div :class="['flex items-center justify-center', sizeClasses]">
    <div class="relative">
      <!-- 外圈 -->
      <div 
        :class="[
          'rounded-full border-2 border-gray-200',
          sizeMap[size]
        ]"
      />
      <!-- 旋转圈 -->
      <div 
        :class="[
          'absolute inset-0 rounded-full border-2 border-primary-500 border-t-transparent animate-spin',
          sizeMap[size]
        ]"
      />
    </div>
    <span v-if="text" class="ml-3 text-gray-600">{{ text }}</span>
  </div>
</template>

<script setup>
const props = defineProps({
  size: { 
    type: String, 
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg', 'xl'].includes(value)
  },
  text: { 
    type: String, 
    default: '' 
  },
})

const sizeMap = {
  sm: 'w-4 h-4',
  md: 'w-6 h-6',
  lg: 'w-8 h-8',
  xl: 'w-12 h-12',
}

const sizeClasses = {
  sm: 'py-2',
  md: 'py-4',
  lg: 'py-6',
  xl: 'py-8',
}[props.size]
</script>