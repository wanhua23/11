import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path:'/',redirect:'/manager/index'},
    { path: '/manager', redirect: '/manager/index',  name: 'manager', component: () => import('../views/Manager.vue'),
      children:[
        { path: 'list', name: 'list',meta:{title:'餐馆列表'}, component: () => import('../views/List.vue'),},
        { path: 'ai', name: 'ai',meta:{title:'ai'}, component: () => import('../views/ai.vue'),},
        { path: 'index', name: 'index',meta:{title:'首页'}, component: () => import('../views/index.vue'),},
        { path: 'add', name: 'add',meta:{title:'添加餐馆'}, component: () => import('../views/add.vue'),},
        { path: 'put', name: 'put',meta:{title:'更新餐馆'}, component: () => import('../views/put.vue'),},
        { path: 'aiList', name: 'aiList',meta:{title:'ai对话历史记录'}, component: () => import('../views/aiList.vue'),},
      ]},
    {path:'/404', name:"notfound", meta:{title:'404找不到页面'}, component:() => import('../views/404.vue')},
    {path:"/:pathMatch(.*)", redirect:'/404'}
  ],
})

router.beforeEach((to, from, next) =>{
  document.title = to.meta.title // 动态设置页面标题
  next()
})

export default router