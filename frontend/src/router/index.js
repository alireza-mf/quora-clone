import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Register from '../views/Register.vue'
import Login from '../views/Login.vue'
import Question from "../views/Question.vue"
import QuestionEditor from "../views/QuestionEditor.vue"

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/register',
    name:'Register',
    component: Register
  },
  {
    path: '/login',
    name:'Login',
    component: Login
  },
  {
    path: "/question/:slug",
    name: "Question",
    component: Question,
    props: true
  },
  {
    path: "/ask",
    name: "QuestionEditor",
    component: QuestionEditor,
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router