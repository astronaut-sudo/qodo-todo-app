import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import Dashboard from '../views/Dashboard.vue';
import Completed from '../views/Completed.vue';

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/login', name: 'login', component: Login },
  { path: '/register', name: 'register', component: Register },
  { path: '/dashboard', name: 'dashboard', component: Dashboard },
  { path: '/completed', name: 'completed', component: Completed }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
