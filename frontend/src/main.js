import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import './assets/tailwind.css'
import 'ant-design-vue/dist/reset.css'

const app = createApp(App)
app.use(createPinia())
app.mount('#app')
