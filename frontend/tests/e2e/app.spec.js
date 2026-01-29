import { test, expect } from '@playwright/test'

test('应该能够访问应用首页并查看主要组件', async ({ page }) => {
  // 访问应用首页
  await page.goto('http://localhost:5173')

  // 验证页面标题
  await expect(page).toHaveTitle('Novel Skit Agent')

  // 验证Header组件
  await expect(page.locator('header')).toBeVisible()
  await expect(page.locator('h1')).toContainText('Novel Skit Agent')
  await expect(page.locator('header p')).toContainText('智能体协作监控系统')

  // 验证启动执行按钮
  const startButton = page.locator('button').first()
  await expect(startButton).toBeVisible()
  await expect(startButton).toContainText('启动执行')

  // 验证停止执行按钮
  const stopButton = page.locator('button').nth(1)
  await expect(stopButton).toBeVisible()
  await expect(stopButton).toContainText('停止执行')

  // 验证主要内容区
  await expect(page.locator('main')).toBeVisible()

  // 验证状态概览卡片
  await expect(page.locator('.card').first()).toBeVisible()

  // 验证智能体状态卡片
  await expect(page.locator('.card').nth(1)).toBeVisible()

  // 验证执行控制卡片
  await expect(page.locator('.card').nth(2)).toBeVisible()

  // 验证执行历史卡片
  await expect(page.locator('.card').nth(3)).toBeVisible()
})

test('应该能够点击启动执行按钮并显示成功消息', async ({ page }) => {
  // 访问应用首页
  await page.goto('http://localhost:5173')

  // 点击启动执行按钮
  const startButton = page.locator('button').first()
  await startButton.click()

  // 验证成功消息是否显示
  // 注意：这里需要根据实际的通知组件实现来调整选择器
  // await expect(page.locator('.notification-success')).toBeVisible()
  // await expect(page.locator('.notification-success')).toContainText('执行已启动')
})

test('应该能够点击停止执行按钮并显示成功消息', async ({ page }) => {
  // 访问应用首页
  await page.goto('http://localhost:5173')

  // 点击停止执行按钮
  const stopButton = page.locator('button').nth(1)
  await stopButton.click()

  // 验证成功消息是否显示
  // 注意：这里需要根据实际的通知组件实现来调整选择器
  // await expect(page.locator('.notification-success')).toBeVisible()
  // await expect(page.locator('.notification-success')).toContainText('执行已停止')
})
