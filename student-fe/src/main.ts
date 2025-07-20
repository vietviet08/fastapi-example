import { createApp } from 'vue'
import router from './router'
import { i18n } from './i18n'
import Toast, { POSITION } from 'vue-toastification'
import 'vue-toastification/dist/index.css'
import './style.css'
import App from './App.vue'

const app = createApp(App)

const toastOptions = {
  position: POSITION.TOP_RIGHT,
  timeout: 5000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: 'button',
  icon: true,
  rtl: false
}

app.use(router)
app.use(i18n)
app.use(Toast, toastOptions)
app.mount('#app')
