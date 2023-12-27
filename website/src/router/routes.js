const routes = [
  { path: '/', redirect: '/home' }, // 默认路径重定向至首页
  { path: '/home', name: 'home', component: () => import('@/views/myHome.vue') },
  { path: '/result', name: 'result', component: () => import('@/views/myResult.vue') },
]

export default routes 