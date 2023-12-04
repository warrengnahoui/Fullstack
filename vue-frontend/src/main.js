import { createApp } from 'vue'
import App from './App.vue'
import { router, store } from './router'

const app = createApp(App)

app.use(router)
app.use(store)

app.mount('#app')
