<template>
  <el-aside :width="isCollapse ? '64px' : '200px'" class="sidebar">
    <div class="logo">
      <el-icon :size="24"><Reading /></el-icon>
      <span v-show="!isCollapse" class="logo-text">小说创作助手</span>
    </div>
    
    <el-menu
      :default-active="activeMenu"
      :collapse="isCollapse"
      :collapse-transition="false"
      router
      background-color="#001529"
      text-color="#ffffffa6"
      active-text-color="#fff"
    >
      <el-menu-item index="/dashboard">
        <el-icon><DataLine /></el-icon>
        <template #title>仪表盘</template>
      </el-menu-item>
      
      <el-menu-item index="/chat">
        <el-icon><ChatDotRound /></el-icon>
        <template #title>智能对话</template>
      </el-menu-item>
      
      <el-menu-item index="/creative">
        <el-icon><MagicStick /></el-icon>
        <template #title>创意策划</template>
      </el-menu-item>
      
      <el-menu-item index="/novel">
        <el-icon><Document /></el-icon>
        <template #title>小说创作</template>
      </el-menu-item>
      
      <el-menu-item index="/collaboration">
        <el-icon><User /></el-icon>
        <template #title>智能体协作</template>
      </el-menu-item>
      
      <el-menu-item index="/scheduler">
        <el-icon><Timer /></el-icon>
        <template #title>任务调度</template>
      </el-menu-item>
      
      <el-menu-item index="/knowledge">
        <el-icon><Collection /></el-icon>
        <template #title>知识库</template>
      </el-menu-item>
      
      <el-menu-item index="/settings">
        <el-icon><Setting /></el-icon>
        <template #title>系统设置</template>
      </el-menu-item>
    </el-menu>
  </el-aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import {
  DataLine,
  ChatDotRound,
  MagicStick,
  Document,
  User,
  Timer,
  Collection,
  Setting,
  Reading,
} from '@element-plus/icons-vue'

const props = defineProps({
  isCollapse: {
    type: Boolean,
    default: false,
  },
})

const route = useRoute()
const activeMenu = computed(() => route.path)
</script>

<style scoped>
.sidebar {
  background-color: #001529;
  transition: width 0.3s;
}

.logo {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  border-bottom: 1px solid #ffffff1a;
}

.logo-text {
  margin-left: 12px;
  white-space: nowrap;
}

.el-menu {
  border-right: none;
}
</style>
