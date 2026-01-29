<template>
  <component 
    :is="iconComponent" 
    :class="[iconSize, iconColor, customClass]"
    :stroke-width="strokeWidth"
  />
</template>

<script setup>
import { computed } from 'vue'
import {
  // 常用图标
  Play,
  Square,
  CheckCircle2,
  XCircle,
  AlertCircle,
  Clock,
  Users2,
  User2,
  FileClock,
  BookOpen,
  Settings,
  RefreshCw,
  Plus,
  Minus,
  ChevronDown,
  ChevronUp,
  ChevronLeft,
  ChevronRight,
  Search,
  Filter,
  Download,
  Upload,
  Trash2,
  Edit,
  Eye,
  EyeOff,
  Home,
  BarChart2,
  Menu,
  X,
  // 新增任务状态相关图标
  Loader2,
  PlayCircle,
  FileCheck,
  CircleCheck,
  CircleX,
  // 执行控制相关图标
  Target,
  MessageSquare,
  Hash,
  Cpu,
  Timer,
  Flag
} from 'lucide-vue-next'

const props = defineProps({
  // 图标名称
  name: {
    type: String,
    required: true
  },
  // 图标大小
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg', 'xl'].includes(value)
  },
  // 图标颜色
  color: {
    type: String,
    default: 'primary'
  },
  // 自定义类名
  class: {
    type: String,
    default: ''
  },
  // 描边宽度
  strokeWidth: {
    type: Number,
    default: 2
  }
})

// 图标映射
const iconMap = {
  play: Play,
  stop: Square,
  check: CheckCircle2,
  x: XCircle,
  alert: AlertCircle,
  clock: Clock,
  users: Users2,
  user: User2,
  file: FileClock,
  book: BookOpen,
  settings: Settings,
  refresh: RefreshCw,
  plus: Plus,
  minus: Minus,
  down: ChevronDown,
  up: ChevronUp,
  left: ChevronLeft,
  right: ChevronRight,
  search: Search,
  filter: Filter,
  download: Download,
  upload: Upload,
  trash: Trash2,
  edit: Edit,
  eye: Eye,
  eyeOff: EyeOff,
  home: Home,
  dashboard: BarChart2,
  menu: Menu,
  close: X,
  // 新增任务状态相关图标
  loading: Loader2,
  playCircle: PlayCircle,
  fileCheck: FileCheck,
  success: CircleCheck,
  error: CircleX,
  // 执行控制相关图标
  target: Target,
  message: MessageSquare,
  hash: Hash,
  cpu: Cpu,
  timer: Timer,
  flag: Flag
}

// 计算图标组件
const iconComponent = computed(() => {
  return iconMap[props.name] || Play
})

// 计算图标大小
const iconSize = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'w-4 h-4'
    case 'lg':
      return 'w-8 h-8'
    case 'xl':
      return 'w-10 h-10'
    default: // md
      return 'w-6 h-6'
  }
})

// 计算图标颜色
const iconColor = computed(() => {
  switch (props.color) {
    case 'primary':
      return 'text-[var(--primary-color)]'
    case 'secondary':
      return 'text-[var(--secondary-color)]'
    case 'success':
      return 'text-[var(--success-color)]'
    case 'warning':
      return 'text-[var(--warning-color)]'
    case 'danger':
      return 'text-[var(--danger-color)]'
    case 'dark':
      return 'text-[var(--text-primary)]'
    case 'light':
      return 'text-[var(--text-secondary)]'
    case 'white':
      return 'text-white'
    default:
      return 'text-[var(--text-primary)]'
  }
})

// 自定义类名
const customClass = computed(() => props.class)
</script>
