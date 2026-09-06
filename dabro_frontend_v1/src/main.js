import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import 'lenis/dist/lenis.css'
import { startLenis } from '@/plugins/lenis'

import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'

const app = createApp(App)
startLenis()

app.use(createPinia())
app.use(router)
app.use(Antd)

app.mount('#app')
