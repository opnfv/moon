import Vue from 'vue'
import Router from 'vue-router'
import Models from './views/Models.vue'
import Auth from './views/Auth.vue'
import Rules from './views/Rules.vue'
import PDP from './views/Pdps.vue'
import Admin from './views/Admin.vue'
import ErrorPage from './views/Error.vue'
import Assignments from "./views/Assignments";

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/auth',
      name: 'auth',
      component: Auth
    },
    {
      path: '/',
      redirect: { name: 'models' }
    },
    {
      path: '/models',
      name: 'models',
      component: Models
    },
    {
      path: '/rules',
      name: 'rules',
      component: Rules
    },
    {
      path: '/assignments',
      name: 'assignments',
      component: Assignments
    },
    {
      path: '/pdp',
      name: 'pdp',
      component: PDP
    },
    {
      path: '/admin',
      name: 'admin',
      component: Admin
    },
    {
      path: '/error',
      name: 'error',
      component: ErrorPage
    },
    
  ]
})
