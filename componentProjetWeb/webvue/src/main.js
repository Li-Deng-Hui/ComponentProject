import Vue from 'vue'
import App from './App.vue'
/*引入elementUI*/
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
Vue.use(ElementUI);
/* --引入elementUI*/

/*引入vue router*/
import VueRouter from 'vue-router'
Vue.use(VueRouter)
/*--引入vue router*/

/*引入Vuex*/
import Vuex from 'vuex'
Vue.use(Vuex)
/*--引入Vuex*/

Vue.config.productionTip = false

import routers from './routers/index'
const router=new VueRouter({routers})

import stores from './stores/index'
const store=new Vuex.Store(stores);

/*axois配置*/
import axios from 'axios'
// 如果你要用到session验证码功能，让请求携带cookie
axios.defaults.withCredentials = true;
// axios 配置
axios.defaults.timeout = 5000;
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';
axios.defaults.baseURL = 'http://localhost:8008';
//http request 拦截器
axios.interceptors.request.use(
    config => {
      var token = sessionStorage.getItem('token');
      config.data = JSON.stringify(config.data);
      config.headers = {
        'Content-Type':'application/json;charset=UTF-8',
      }
      if (token) {
        config.params = {
          'token': token
        }
      }
      return config;
    },
    error => {
      return Promise.reject(error);
    }
);

//http response 拦截器
axios.interceptors.response.use(
    response => {
      // 拿到接口返回值，做逻辑处理
      if (response.data.state || response.data.code == '0') {
        return response.data;
      } else {
        var msg = response.data.msg;
        return Promise.reject(msg) // 抛出错误
      }
    },
    error => {
      return Promise.reject(error)
    }
);
Vue.prototype.$axios=axios;
/*--axois配置*/

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')
