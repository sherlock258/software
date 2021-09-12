import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'login',
    component: () => import(/* webpackChunkName: "about" */ '../views/Signin')
  },
  {
    path: '/',
    name: 'Index',
    component: () => import(/* webpackChunkName: "about" */ '../views/Index.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import(/* webpackChunkName: "about" */ '../views/Register.vue')
  },
  {
    path: '/forgetpass',
    name: 'Forgetpass',
    component: () => import(/* webpackChunkName: "about" */ '../views/Forgetpass.vue')
  },
  {
    path: '/write',
    name: 'Write',
    component: () => import(/* webpackChunkName: "about" */ '../views/Write.vue')
  },
  {
    path: '/kindlist',
    name: 'Kindlist',
    component: () => import(/* webpackChunkName: "about" */ '../views/Kindlist.vue')
  },
  {
    path: '/article',
    name: 'Article',
    component: () => import(/* webpackChunkName: "about" */ '../views/Article')
  },
  {
    path: '/mine',
    name: 'Mine',
    component: () => import(/* webpackChunkName: "about" */ '../views/Mine')
  },
  {
    path: '/setting',
    name: 'Setting',
    component: () => import(/* webpackChunkName: "about" */ '../views/Setting')
  },
  {
    path: '/attention',
    name: 'Attention',
    component: () => import(/* webpackChunkName: "about" */ '../views/Attention')
  },
  {
    path: '/like',
    name: 'Like',
    component: () => import(/* webpackChunkName: "about" */ '../views/Like')
  },
  {
    path: '/draft',
    name: 'Draft',
    component: () => import(/* webpackChunkName: "about" */ '../views/Draft')
  },
  {
    path: '/search',
    name: 'Search',
    component: () => import(/* webpackChunkName: "about" */ '../views/Search')
  }
]

const router = new VueRouter({
  routes
})

export default router
