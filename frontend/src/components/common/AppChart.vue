<template>
  <div class="relative">
    <canvas ref="chartCanvas" />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import {
  Chart as ChartJS,
  ArcElement,
  LineElement,
  BarElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from 'chart.js'

// 注册Chart.js组件
ChartJS.register(
  ArcElement,
  LineElement,
  BarElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
)

const props = defineProps({
  type: { 
    type: String, 
    required: true,
    validator: (value) => ['doughnut', 'line', 'bar', 'pie'].includes(value)
  },
  data: { 
    type: Object, 
    required: true 
  },
  options: { 
    type: Object, 
    default: () => ({}) 
  },
  height: { 
    type: [Number, String], 
    default: 200 
  },
})

const chartCanvas = ref(null)
const chartInstance = ref(null)

// 默认配置
const defaultOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        padding: 20,
        usePointStyle: true,
        font: {
          size: 12
        }
      }
    },
    tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      titleColor: '#fff',
      bodyColor: '#fff',
      borderColor: '#374151',
      borderWidth: 1,
      cornerRadius: 6,
      padding: 12,
      displayColors: true,
    }
  }
}

// 合并配置
const mergedOptions = computed(() => ({
  ...defaultOptions,
  ...props.options
}))

// 创建图表
const createChart = () => {
  if (!chartCanvas.value) return

  // 销毁旧图表
  if (chartInstance.value) {
    chartInstance.value.destroy()
  }

  // 设置canvas高度
  if (typeof props.height === 'number') {
    chartCanvas.value.height = props.height
  } else {
    chartCanvas.value.style.height = props.height
  }

  // 创建新图表
  chartInstance.value = new ChartJS(chartCanvas.value, {
    type: props.type,
    data: props.data,
    options: mergedOptions.value
  })
}

// 更新图表
const updateChart = () => {
  if (chartInstance.value) {
    chartInstance.value.data = props.data
    chartInstance.value.options = mergedOptions.value
    chartInstance.value.update()
  }
}

// 监听数据变化
watch(() => props.data, updateChart, { deep: true })
watch(() => props.options, updateChart, { deep: true })

onMounted(() => {
  createChart()
})

onUnmounted(() => {
  if (chartInstance.value) {
    chartInstance.value.destroy()
  }
})
</script>

<style scoped>
canvas {
  max-width: 100%;
}
</style>