import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins'


Vue.config.productionTip = false

Vue.use(require('vue-moment'));



new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
