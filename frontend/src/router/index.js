import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterPage from '../views/RegisterPage.vue'
import LoginPage from '../views/LoginPage.vue'
import ManagerApplications from '../views/ManagerApplications.vue'
import CreateCategory from '../views/CreateCategory.vue'
import AllCategories from '../views/AllCategories.vue'
import UpdateCategory from '../views/UpdateCategory.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterPage
  },
  {
    path: '/login',
    name: 'login',
    component: LoginPage
  },
  {
    path: '/managerapplications',
    name: 'managerapplications',
    component: ManagerApplications
  },
  {
    path: '/createcategory',
    name: 'createcategory',
    component: CreateCategory
  },
  {
    path: '/allcategories',
    name: 'allcategories',
    component: AllCategories
  },
  {
    path: '/updatecategory/:id',
    name: 'UpdateCategory',
    component: UpdateCategory
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
