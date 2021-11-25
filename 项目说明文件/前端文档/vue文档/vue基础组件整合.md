# Vue 基础组件整合

​		vue的核心组件Vue Router,Vuex

​		文档可以在vue官网查看学习:[Vue.js (vuejs.org)](https://cn.vuejs.org/)



[TOC]



## Vue Router

Vue Router 是 [Vue.js (opens new window)](http://cn.vuejs.org/)官方的路由管理器。它和 Vue.js 的核心深度集成，让构建单页面应用变得易如反掌。包含的功能有：

- 嵌套的路由/视图表
- 模块化的、基于组件的路由配置
- 路由参数、查询、通配符
- 基于 Vue.js 过渡系统的视图过渡效果
- 细粒度的导航控制
- 带有自动激活的 CSS class 的链接
- HTML5 历史模式或 hash 模式，在 IE9 中自动降级
- 自定义的滚动条行为

1. 安装vue router

   ```vue
   npm install vue-router
   ```

2. 在项目main.js中引用vue router

   ```vue
   /*引入vue router*/
   import Vue from 'vue'
   import VueRouter from 'vue-router'
   Vue.use(VueRouter)
   /*--引入vue router*/
   
   ```

3. 配置使用

   src下新建routers目录存放路由文件：index.js

   ```
   import ComponentIndex from '../pages/index';
   import UserLogin from '../pages/user/Login/index'
   
   const routes=[
       {path:'/',name:'componentIndex',component:ComponentIndex},
       {path: '/user/login',name:'userLogin',component: UserLogin}
   ]
   
   export default routes;
   ```

   ![image-20211114134625629](.\image-20211114134625629.png)

   *注意事项：const router=new VueRouter({routes:routers})   路由不生效，需要将路由表赋值给变量routes*

4. 使用，进行路由跳转

   [编程式的导航 | Vue Router (vuejs.org)](https://router.vuejs.org/zh/guide/essentials/navigation.html)



## Vuex

Vuex 是一个专为 Vue.js 应用程序开发的**状态管理模式**。它采用集中式存储管理应用的所有组件的状态，并以相应的规则保证状态以一种可预测的方式发生变化。Vuex 也集成到 Vue 的官方调试工具 [devtools extension (opens new window)](https://github.com/vuejs/vue-devtools)，提供了诸如零配置的 time-travel 调试、状态快照导入导出等高级调试功能。

1. 安装Vuex

   ```
   npm install vuex --save
   ```

2. 在项目main.js中引用Vuex

   ```
   /*引入Vuex*/
   import Vue from 'vue'
   import Vuex from 'vuex'
   Vue.use(Vuex)
   /*--引入Vuex*/
   ```

   

3. 配置使用

   src下新建stores目录存放状态文件：index.js

   ```
   const stores={
       state:{
           name:'组件管理项目'
       },
       mutations:{
   
       }
   }
   export default stores;
   ```

   ![image-20211114134700428](.\image-20211114134700428.png)

4. 使用，状态保存和获取

   [开始 | Vuex (vuejs.org)](https://vuex.vuejs.org/zh/guide/#最简单的-store)

