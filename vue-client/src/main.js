//import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import 'bootstrap/dist/css/bootstrap.min.css';
import Popper from "vue3-popper";

import App from './App.vue'
import router from './router'

import '@imengyu/vue3-context-menu/lib/vue3-context-menu.css'
import ContextMenu from '@imengyu/vue3-context-menu'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ContextMenu)
app.component("Popper", Popper)

app.mount('#app')
