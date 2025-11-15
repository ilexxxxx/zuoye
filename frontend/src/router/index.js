import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard },
  { path: '/meeting/:id', name: 'MeetingDetail', component: () => import('../views/MeetingDetail.vue') }

]

export default createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})