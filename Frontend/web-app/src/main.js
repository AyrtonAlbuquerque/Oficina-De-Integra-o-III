import Vue from 'vue';
import VueCookies from 'vue-cookies';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify';
import alert from './plugins/alert';

Vue.config.productionTip = false;

Vue.use(VueCookies);
Vue.use(alert);

new Vue({
  router,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
