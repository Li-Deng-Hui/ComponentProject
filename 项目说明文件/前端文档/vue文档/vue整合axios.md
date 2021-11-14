# Vue整合axios



# 1、下载axios



```undefined
 npm install axios  --save
```

# 2、在src文件夹在创建http.js文件



```tsx
import Vue from 'vue';
import axios from 'axios';

// 如果你要用到session验证码功能，让请求携带cookie
axios.defaults.withCredentials = true;

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

/**
 * 封装get方法
 * @param url
 * @param data
 * @returns {Promise}
 */
export function get(url, paramenter = {}) {
    return new Promise((resolve, reject) => {
        axios.get(url, { params: paramenter })
            .then(response => {
                resolve(response);
            })
            .catch(err => {
                reject(err)
            })
    })
}

/**
 * 封装post请求
 * @param url
 * @param data
 * @returns {Promise}
 */

export function post(url, data = {}) {
    return new Promise((resolve, reject) => {
        axios.post(url, data).then(response => {
                resolve(response);
            }, err => {
                reject(err)
            })
    })
}


// Vue.prototype.$http = axios;
//定义全局变量
Vue.prototype.$post = post;
Vue.prototype.$get = get;
```

# 3、在main.js 引入http.js文件



```dart
import './http.js'; // http请求
```



作者：前端码农专心造轮子
链接：https://www.jianshu.com/p/e3fe8416c27a
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。