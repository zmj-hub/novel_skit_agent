<template>
  <header class="sticky top-0 z-40 bg-white shadow-sm border-b border-gray-200">
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <!-- 左侧：Logo和标题 -->
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-primary-500 to-primary-600 flex items-center justify-center shadow-md">
            <AppIcon name="PlayCircleIcon" size="md" class="text-white" />
          </div>
          <div>
            <h1 class="text-xl font-bold text-gray-900 tracking-tight">Novel Skit Agent</h1>
            <p class="text-gray-600 text-sm">智能体协作监控系统</p>
          </div>
        </div>
        
        <!-- 中间：导航菜单（移动端隐藏） -->
        <nav class="hidden md:flex items-center gap-6">
          <a href="#" class="text-gray-600 hover:text-primary-600 transition-colors">监控</a>
          <a href="#" class="text-gray-600 hover:text-primary-600 transition-colors">配置</a>
          <a href="#" class="text-gray-600 hover:text-primary-600 transition-colors">日志</a>
        </nav>
        
        <!-- 右侧：操作按钮 -->
        <div class="flex items-center gap-3">
          <button 
            @click="$emit('start-execution')"
            class="inline-flex items-center gap-2 px-4 py-2 bg-primary-500 hover:bg-primary-600 text-white rounded-lg transition-colors shadow-sm"
          >
            <AppIcon name="PlayIcon" size="sm" />
            启动执行
          </button>
          
          <button 
            @click="$emit('stop-execution')"
            class="inline-flex items-center gap-2 px-4 py-2 bg-danger-500 hover:bg-danger-600 text-white rounded-lg transition-colors shadow-sm"
          >
            <AppIcon name="StopIcon" size="sm" />
            停止执行
          </button>
          
          <!-- 移动端菜单按钮 -->
          <button 
            @click="showMobileMenu = true"
            class="md:hidden p-2 text-gray-600 hover:text-gray-900 transition-colors"
          >
            <AppIcon name="Bars3Icon" size="lg" />
          </button>
        </div>
      </div>
    </div>
    
    <!-- 移动端菜单 -->
    <Transition name="slide">
      <div v-if="showMobileMenu" class="md:hidden fixed inset-0 z-50">
        <div class="absolute inset-0 bg-black/50" @click="showMobileMenu = false" />
        <div class="absolute right-0 top-0 bottom-0 w-80 bg-white shadow-xl">
          <div class="p-4 border-b border-gray-200">
            <div class="flex items-center justify-between">
              <h2 class="text-lg font-semibold text-gray-900">菜单</h2>
              <button 
                @click="showMobileMenu = false"
                class="p-2 text-gray-600 hover:text-gray-900 transition-colors"
              >
                <AppIcon name="XMarkIcon" size="lg" />
              </button>
            </div>
          </div>
          <nav class="p-4 space-y-2">
            <a href="#" class="block px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors">监控</a>
            <a href="#" class="block px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors">配置</a>
            <a href="#" class="block px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors">日志</a>
          </nav>
        </div>
      </div>
    </Transition>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import AppIcon from './common/AppIcon.vue'

const emit = defineEmits(['start-execution', 'stop-execution'])

const showMobileMenu = ref(false)
</script>

<style scoped>
/* 移动端菜单动画 */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
</style>