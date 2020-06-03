import Vue from 'vue'
import App from './App.vue'
import router from './router'
import VueResource from 'vue-resource'
import VeeValidate from 'vee-validate'
import Toasted from 'vue-toasted'

Vue.config.productionTip = false

Vue.use(VueResource)
Vue.use(VeeValidate)
Vue.use(Toasted)

Vue.http.interceptors.push(function () {
  return function (response) {
    if (response.status == 401) {
      router.push('auth');
    } else if (response.status == 0) {
      router.push('error');
    }
  }
});

var authKey = localStorage.getItem("auth-key")
if (authKey) {
  Vue.http.headers.common['x-api-key'] = authKey;
} else {
  router.push('auth');
}

Vue.toasted.register('toast',
  (payload) => {
    return `
      <div class="toast show" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-header">
          <span class="badge badge-${payload.type}">&nbsp;</span>
          <strong class="ml-2">${payload.title}</strong>
        </div>
        <div class="toast-body">
          ${payload.message}
        </div>
      </div>
      `;
    },

  {
    className: "toast-background",
    position: 'top-center',
    duration: 3000
  })


new Vue({
  router,
  render: h => h(App)
}).$mount('#app')


