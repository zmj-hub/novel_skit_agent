import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import Header from '@/components/Header.vue'

describe('Header组件测试', () => {
  it('应该正确渲染Header组件', () => {
    const wrapper = mount(Header)
    
    expect(wrapper.exists()).toBe(true)
    expect(wrapper.find('h1').text()).toBe('Novel Skit Agent')
    expect(wrapper.find('p').text()).toBe('智能体协作监控系统')
  })
  
  it('应该在点击启动执行按钮时触发start-execution事件', () => {
    const wrapper = mount(Header)
    
    // 模拟点击启动执行按钮
    wrapper.find('button:first-child').trigger('click')
    
    // 验证事件是否被触发
    expect(wrapper.emitted('start-execution')).toBeTruthy()
  })
  
  it('应该在点击停止执行按钮时触发stop-execution事件', () => {
    const wrapper = mount(Header)
    
    // 模拟点击停止执行按钮
    wrapper.find('button:last-child').trigger('click')
    
    // 验证事件是否被触发
    expect(wrapper.emitted('stop-execution')).toBeTruthy()
  })
  
  it('应该正确渲染图标', () => {
    const wrapper = mount(Header)
    
    // 验证图标是否存在
    expect(wrapper.find('svg').exists()).toBe(true)
  })
})
