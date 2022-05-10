import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import VueCookies from 'vue-cookies'

Vue.config.productionTip = false
Vue.use(VueCookies, { expire: '1d' })
new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')
