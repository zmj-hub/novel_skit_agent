<template>
  <el-container class="layout-container">
    <Sidebar :is-collapse="isCollapse" />
    
    <el-container class="main-container">
      <Header :is-collapse="isCollapse" @toggle-sidebar="toggleSidebar" />
      
      <el-main class="main-content">
        <div class="page-container">
          <slot />
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref } from 'vue'
import Sidebar from './Sidebar.vue'
import Header from './Header.vue'

const isCollapse = ref(false)

const toggleSidebar = () => {
  isCollapse.value = !isCollapse.value
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
  width: 100vw;
}

.main-container {
  flex-direction: column;
  background-color: #f0f2f5;
}

.main-content {
  padding: 20px;
  overflow-y: auto;
}

.page-container {
  background-color: #fff;
  border-radius: 4px;
  min-height: calc(100vh - 104px);
  padding: 20px;
}
</style>
