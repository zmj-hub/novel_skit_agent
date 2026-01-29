import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import AppIcon from '@/components/AppIcon.vue'

describe('AppIcon组件测试', () => {
  it('应该正确渲染指定的图标', () => {
    const wrapper = mount(AppIcon, {
      props: {
        name: 'play',
        size: 'md',
        color: 'primary'
      }
    })
    
    expect(wrapper.exists()).toBe(true)
  })
  
  it('应该根据size属性调整图标大小', () => {
    const wrapper = mount(AppIcon, {
      props: {
        name: 'play',
        size: 'sm'
      }
    })
    
    expect(wrapper.classes()).toContain('w-4')
    expect(wrapper.classes()).toContain('h-4')
  })
  
  it('应该根据color属性设置图标颜色', () => {
    const wrapper = mount(AppIcon, {
      props: {
        name: 'play',
        color: 'danger'
      }
    })
    
    expect(wrapper.classes()).toContain('text-[var(--danger-color)]')
  })
  
  it('应该支持自定义类名', () => {
    const wrapper = mount(AppIcon, {
      props: {
        name: 'play',
        class: 'custom-class'
      }
    })
    
    expect(wrapper.classes()).toContain('custom-class')
  })
  
  it('应该支持自定义描边宽度', () => {
    const wrapper = mount(AppIcon, {
      props: {
        name: 'play',
        strokeWidth: 1.5
      }
    })
    
    expect(wrapper.attributes('stroke-width')).toBe('1.5')
  })
})
