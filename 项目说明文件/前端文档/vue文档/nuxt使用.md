# Nuxt.js使用

> 官网：[Nuxt - Installation (nuxtjs.org)](https://nuxtjs.org/docs/get-started/installation)

##### 为什么使用nuxt.js?

vue单页面应用渲染是从服务器获取所需js，在客户端将其解析生成html挂载于
 id为app的DOM元素上，这样会存在两大问题。

1. 由于资源请求量大，造成网站首屏加载缓慢，不利于用户体验。
2. 由于页面内容通过js插入，对于内容性网站来说，搜索引擎无法抓取网站内容，不利于SEO。
    Nuxt.js 是一个基于Vue.js的通用应用框架，预设了利用Vue.js开发服务端渲染的应用所需要的各种配置。可以将html在服务端渲染，合成完整的html文件再输出到浏览器。

除此之外，nuxt与vue还有一些其他方面的区别。

1. 路由
    nuxt按照 pages 文件夹的目录结构自动生成路由
    vue需在 src/router/index.js 手动配置路由
2. 入口页面
    nuxt页面入口为 layouts/default.vue
    vue页面入口为 src/App.vue

1. webpack配置
    nuxt内置webpack，允许根据服务端需求，在 nuxt.config.js 中的build属性自定义构建webpack的配置，覆盖默认配置
    vue关于webpack的配置存放在build文件夹下

下图为关于nuxt的简单概述



![img](https:////upload-images.jianshu.io/upload_images/6550096-7845f281c8565e50.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

NUXT.js.png

> nuxt是关于服务端渲染的，如若想让组件在客户端渲染，可以使用`<no-ssr></no-ssr>`将其包裹起来（该标签最多只能包含一个子组件/元素）。
>  这样在未获取到内容时，页面先采用`<div class="no-ssr-placeholder" data-v-2a183b29=""></div>`占位，然后将获取到的html覆盖该占位



**Nuxt 是 Vue 上的 SSR，也就是服务端渲染应用框架，可在很大程度上解决当前 SPA 和 CSR 的首页加载慢，不利于 SEO 的问题。**

简单的说Nuxt.js是Vue.js的通用框架，最常用的就是用来作SSR（服务器端渲染）。再直白点说，就是Vue.js原来是开发SPA（单页应用）的，但是随着技术的普及，很多人想用Vue开发多页应用，并在服务端完成渲染。这时候就出现了Nuxt.js这个框架，她简化了SSR的开发难度。还可以直接用命令把我们制作的vue项目生成为静态html

##### 什么是SSR？

SSR，即服务器渲染，就是在服务器端将对Vue页面进行渲染生成html文件，将html页面传递给浏览器。

SSR两个优点：

- SEO 不同于SPA的HTML只有一个无实际内容的HTML和一个app.js，SSR生成的HTML是有内容的，这让搜索引擎能够索引到页面内容。
- 更快内容到达时间 传统的SPA应用是将bundle.js从服务器获取，然后在客户端解析并挂载到dom。而SSR直接将HTML字符串传递给浏览器。大大加快了首屏加载时间。

Nuxt.js的官方网站是这样介绍的：

> NuxtJS 让你构建你的下一个 Vue.js 应用程序变得更有信心。这是一个 开源 的框架，让 web 开发变得简单而强大。

Nuxt.js是特点（优点）：

- 基于 Vue.js
- 自动代码分层
- 服务端渲染
- 强大的路由功能，支持异步数据
- 静态文件服务
- ES6/ES7 语法支持
- 打包和压缩 JS 和 CSS
- HTML头部标签管理
- 本地开发支持热加载
- 集成ESLint
- 支持各种样式预处理器： SASS、LESS、 Stylus等等

##### 1. Nuxt环境搭建和Hello World

Nuxt.js 十分简单易用。一个简单的项目只需将 nuxt 添加为依赖组件即可。

为了快速入门，Nuxt.js 团队创建了脚手架工具 create-nuxt-app（确保安装了 npx（npx 在 NPM 版本 5.2.0 默认安装了））。



```undefined
npx create-nuxt-app nuxtdmo
```

现在运行在 [http://localhost:3000](https://links.jianshu.com/go?to=http%3A%2F%2Flocalhost%3A3000) 上运行

**Nuxt自动生成了项目目录，如下：**。



```java
|-- .nuxt                            // Nuxt自动生成，临时的用于编辑的文件，build
|-- assets                           // 用于组织未编译的静态资源入LESS、SASS 或 JavaScript
|-- components                       // 用于自己编写的Vue组件，比如滚动组件，日历组件，分页组件
|-- layouts                          // 布局目录，用于组织应用的布局组件，不可更改。
|-- middleware                       // 用于存放中间件
|-- pages                            // 用于存放写的页面，我们主要的工作区域
|-- plugins                          // 用于存放JavaScript插件的地方
|-- static                           // 用于存放静态资源文件，比如图片
|-- store                            // 用于组织应用的Vuex 状态管理。
|-- .editorconfig                    // 开发工具格式配置
|-- .eslintrc.js                     // ESLint的配置文件，用于检查代码格式
|-- .gitignore                       // 配置git不上传的文件
|-- nuxt.config.json                 // 用于组织Nuxt.js应用的个性化配置，已覆盖默认配置
|-- package-lock.json                // npm自动生成，用于帮助package的统一性设置的，yarn也有相同的操作
|-- package-lock.json                // npm自动生成，用于帮助package的统一性设置的，yarn也有相同的操作
|-- package.json                     // npm包管理配置文件
```

##### 2.Nuxt常用配置项

**配置IP和端口**

开发中经常会遇到端口被占用或者指定IP的情况。我们需要在根目录下的package.json里对config项进行配置。比如现在我们想把IP配置成127.0.0.1，端口设置1818。



```cpp
//package.json
"config":{
    "nuxt":{
      "host":"127.0.0.1",
      "port":"1818"
    }
  },
```

配置好后，我们在终端中输入npm run dev，然后你会看到服务地址改为了127.0.0.1:1818.

**配置全局CSS**

在开发多页项目时，都会定义一个全局的CSS来初始化我们的页面渲染，比如把padding和margin设置成0，网上也有非常出名的开源css文件normailze.css。要定义这些配置，需要在nuxt.config.js里进行操作。

比如现在我们要把页面字体设置为红色，就可以在assets/css/normailze.css文件，然后把字体设置为红色。



```xml
 <!--assets/css/normailze.css-->
 html{
    color:red;
}
```



```xml
<!--/nuxt.config.js-->
css:['~assets/css/normailze.css'],
```

设置好后，需要在终端输入`npm run dev` 。然后你会发现字体已经变成了红色。

**配置webpack的loader**

在`nuxt.config.js`里是可以对`webpack`的基本配置进行覆盖的，比如现在我们要配置一个`url-loader`来进行小图片的64位打包。就可以在`nuxt.config.js`的`build`选项里进行配置



```tsx
build: {

    loaders:[
      {
        test:/\.(png|jpe?g|gif|svg)$/,
        loader:"url-loader",
        query:{
          limit:10000,
          name:'img/[name].[hash].[ext]'
        }
      }
    ],

    /*
    ** Run ESLint on save
    */
    extend (config, { isDev, isClient }) {
      if (isDev && isClient) {
        config.module.rules.push({
          enforce: 'pre',
          test: /\.(js|vue)$/,
          loader: 'eslint-loader',
          exclude: /(node_modules)/
        })
      }
    }
  }
```

##### 3.Nuxt路由

**Nuxt的路由配置**

简单demo

在about文件夹下新建index.vue文件，并写入下面的代码：



```xml
<template>
  <div>
      <h2>About Index page</h2>
      <ul>
        <li><a href="/">Home</a></li>
      </ul>
  </div>
</template>
```

在news文件夹下新建index.vue文件，并写入下面的代码：



```xml
<template>
  <div>
      <h2>News Index page</h2>
       <ul>
        <li><a href="/">Home</a></li>
      </ul>
  </div>
</template>
```

修改原来的pages文件夹下的index.vue，删除没用的代码，写入下面代码：



```xml
<template>
  <div>
    <ul>
      <li><a href="/">HOME</a></li>
      <li><a href="/about">ABOUT</a></li>
      <li><a href="/news">NEWS</a></li>
    </ul>
  </div>
</template>

<script>

export default {
  components: {

  }
}
</script>

<style>

</style>
```

你现在你打开浏览器，发现都已经ok了，不需要你单独配置路由，因为Nuxt.js都为我们作好了，不用写任何配置代码。

虽然上面的例子跳转已经成功，但是`Nuxt.js`并不推荐这`<a>`标签的作法，它为我们准备了`<nuxt-link>`标签（vue中叫组件）。我们先把首页的`<a>`标签替换成`<nuxt-link>`



```xml
<template>
  <div>
    <ul>
      <li><nuxt-link :to="{name:'index'}">HOME</nuxt-link></li>
      <li><nuxt-link :to="{name:'about'}">ABOUT</nuxt-link></li>
      <li><nuxt-link :to="{name:'news'}">NEWS</nuxt-link></li>
    </ul>
  </div>
</template>

<script>

export default {
  components: {

  }
}
</script>

<style>

</style>
```

我们再次预览页面，也是可以进行正常跳转的，在实际开发中尽量使用标签的方法跳转路由。

**params传递参数**

路由经常需要传递参数，我们可以简单的使用params来进行传递参数，我们现在向新闻页面（news）传递个参数，然后在新闻页面进行简单的接收。

我们先修改pages下的Index.vue文件，给新闻的跳转加上params参数，传递3306ID。



```xml
<template>
  <div>
    <ul>
      <li><nuxt-link :to="{name:'index'}">HOME</nuxt-link></li>
      <li><nuxt-link :to="{name:'about'}">ABOUT</nuxt-link></li>
      <li><nuxt-link :to="{name:'news',params:{newsId:3306}}">NEWS</nuxt-link></li>
    </ul>
  </div>
</template>

<script>

export default {
  components: {

  }
}
</script>

<style>

</style>
```

在news文件夹下的index.vue里用$route.params.newsId进行接收，代码如下:



```xml
<template>
  <div>
      <h2>News Index page</h2>
      <p>NewsID:{{$route.params.newsId}}</p>
       <ul>
        <li><a href="/">Home</a></li>
      </ul>
  </div>
</template>
```

**动态路由**

新闻详细页面： 我在news文件夹下面新建了_id.vue的文件，以下画线为前缀的Vue文件就是动态路由，然后在文件里边有 $route.params.id来接收参数。



```xml
<!--/pages/news/_id.vue-->
<template>
  <div>
      <h2>News-Content [{{$route.params.id}}]</h2>
      <ul>
        <li><a href="/">Home</a></li>
      </ul>
  </div>
</template>
```

修改新闻首页路由:



```xml
<!--/pages/news/index.vue-->
<template>
  <div>
      <h2>News Index page</h2>
      <p>NewsID:{{$route.params.newsId}}</p>
       <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/news/123">News-1</a></li>
        <li><a href="/news/456">News-2</a></li>
      </ul>
  </div>
</template>
```

代码写好后，打开npm run dev 进行查看，我们已经进入了新闻详细页，并在详细页中取得了传递过来的新闻ID.

**动态参数校验**

进入一个页面，对参数传递的正确性校验是必须的，Nuxt.js也贴心的为我们准备了校验方法validate( )。



```xml
<!--/pages/news/_id.vue-->
export default {

  validate ({ params }) {
    // Must be a number
    return /^\d+$/.test(params.id)
  }

}
```

我们使用了validate方法，并把params传递进去，然后用正则进行了校验，如果正则返回了true正常进入页面，如果返回false进入404页面。

##### 4. Nuxt的默认模版和默认布局

**默认模板**
 Nuxt为我们提供了超简单的默认模版订制方法，只要在根目录下创建一个app.html就可以实现了。现在我们希望每个页面的最上边都加入“Hollo Word” 这几个字，我们就可以使用默认模版来完成。



```xml
<!DOCTYPE html>
<html lang="en">
<head>
   {{ HEAD }}
</head>
<body>
    <p>Hollo Word/p>
    {{ APP }}
</body>
```

这里的{{ HEAD }}读取的是nuxt.config.js里的信息，{{APP}} 就是我们写的pages文件夹下的主体页面了。需要注意的是HEAD和APP都需要大写，如果小写会报错的。

这里还有一个小坑需要大家注意，就是如果你建立了默认模板后，记得要重启服务器，否则你的显示不会成功；但是默认布局是不用重启服务器。

**默认布局**
 和默认模板类似的功能还有默认布局，但是从名字上你就可以看出来，默认布局主要针对于页面的统一布局使用。它在位置根目录下的layouts/default.vue。需要注意的是在默认布局里不要加入头部信息，只是关于`<template>`标签下的内容统一订制。

需求，我们在每个页面的最顶部放入“我是默认布局 ”这几个字，看一下在默认布局里的实现。



```xml
<!--/layouts/default.vue-->
<template>
  <div>
    <p>我是默认布局</p>
    <nuxt/>
  </div>
</template>
```

这里的<nuxt/>就相当于我们每个页面的内容，你也可以把一些通用样式放入这个默认布局里，但是个人不建议这样写，会增加页面的复杂程度。

**总结**：要区分默认模版和默认布局的区别，模版可以订制很多头部信息，包括IE版本的判断；模版只能定制<template>里的内容，跟布局有关系。在工作中修改时要看情况来编写代码

##### 5.Nuxt的错误页面和个性meta设置

**建立错误页面**

在根目录下的layouts文件夹下建立一个error.vue文件，它相当于一个显示应用错误的组件。



```xml
<!--/layouts/error.vue--->
<template>
 <div>
     <h2 v-if="error.statusCode==404">404页面不存在</h2>
     <h2 v-else>500服务器错误</h2>
     <ul>
         <li><nuxt-link to="/">HOME</nuxt-link></li>
     </ul>
 </div>
</template>

<script>
export default {
 props:['error'],
}
</script>
```

代码用v-if进行判断错误类型，需要注意的是这个错误是你需要在<script>里进行声明的，如果不声明程序是找不到error.statusCode的。

**个性meta设置**

页面的Meta对于SEO的设置非常重要，比如你现在要作个新闻页面，那为了搜索引擎对新闻的收录，需要每个页面对新闻都有不同的title和meta设置。直接使用head方法来设置当前页面的头部信息就可以了。我们现在要把New-1这个页面设置成个性的meta和title。

1.我们先把pages/news/index.vue页面的链接进行修改一下，传入一个title，目的是为了在新闻具体页面进行接收title，形成文章的标题。



```ruby
<li><nuxt-link :to="{name:'news-id',params:{id:123,title:'jspang.com'}}">News-1</nuxt-link></li>
```

2.第一步完成后，我们修改/pages/news/_id.vue，让它根据传递值变成独特的meta和title标签。



```xml
<template>
  <div>
      <h2>News-Content [{{$route.params.id}}]</h2>
      <ul>
        <li><a href="/">Home</a></li>
      </ul>
  </div>
</template>
<script>
export default {

  validate ({ params }) {
    // Must be a number
    return /^\d+$/.test(params.id)
  },
  data(){
    return{
      title:this.$route.params.title,
    }
  },
//独立设置head信息
  head(){
      return{
        title:this.title,
        meta:[
          {hid:'description',name:'news',content:'This is news page'}
        ]
      }
    }
}

</script>
```

注意：为了避免子组件中的meta标签不能正确覆盖父组件中相同的标签而产生重复的现象，建议利用 hid 键为meta标签配一个唯一的标识编号。

##### 6.静态资源和打包

**直接引入图片**

我们在网上任意下载一个图片，放到项目中的static文件夹下面，然后可以使用下面的引入方法进行引用.



```xml
<div><img src="~static/logo.png" /></div>
```

这种引用方法是不用估计相对路径的，“~”就相当于定位到了项目跟目录，这时候你的图片路径就不会出现错误，就算打包也是正常的。

**CSS引入图片**

如果在CSS中引入图片，方法和html中直接引入是一样的，也是用“~”符号引入。



```xml
<style>
  .diss{
    width: 300px;
    height: 100px;
    background-image: url('~static/logo.png')
  }
</style>
```

这时候在npm run dev 下是完全正常的，那我们看一下打包。

**打包静态HTML并运行**

用Nuxt.js制作完成后，你可以打包成静态文件并放在服务器上，进行运行。

在终端中输入：



```undefined
npm run generate
```







##### 安装sass



```undefined
npm i node-sass sass-loader scss-loader --save-dev
```

vue文件中可直接使用



```xml
<style lang="scss" scoped>
</style>
```

sass文件如需解析，nuxt.config.js中配置css属性



```javascript
css: [
    {
      src: '~/assets/style/reset.scss',
      lang: 'scss'
    }
],
```

##### 使用axios并跨域

1. package.json
    `npm install @nuxtjs/proxy`
    nuxt 项目默认安装axios， 所以只需安装proxy即可



```javascript
"dependencies": {
    "@nuxtjs/axios": "^5.0.0",
    "@nuxtjs/proxy": "^1.2.4",
}
```

1. nuxt.config.js



```javascript
modules: [
    '@nuxtjs/axios',
    '@nuxtjs/proxy'
  ],
  proxy: {
    '/api': {
      target: 'http:www.xxx.com',
      changeOrigin: true,
      pathRewrite: {
        '^/api ': ''
      }
    }
  },
```

1. index.vue



```javascript
import axios from 'axios'
export default {
    data () {
        return {
          page: 0
        }
    },
    async asyncData () {
        let data = await axios.get('http://localhost:3000/api/admin/list')
        return {
          page: data.data.page
        }
  },
}
```

> **注意**
>  采用 `import axios from 'axios'` 方式引入axios时，接口参数前须加baseURL -> http://localhost:3000
>  如果采取 `axios.get('/api/admin/game')` 调用接口返回nuxt服务器错误，如下图
>
> ![img](https:////upload-images.jianshu.io/upload_images/6550096-204b7306b1af184e.jpg?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)
>
> 1540541910156.jpg

封装axios，解决每个请求前加baseURL
 plugins/axios.js



```javascript
import * as axios from 'axios'

let options = {}
// The server-side needs a full url to works
if (process.server) {
  options.baseURL = `http://${process.env.HOST || 'localhost'}:${process.env.PORT || 3000}`
}

export default axios.create(options)
```

index.vue



```javascript
import axios from '~/plugins/axios'
axios.get('/api/admin/game')
```

##### 引入第三方插件(vue-awesome-swiper)

1. `npm install vue-awesome-swiper --save`
2. plugins文件夹下新建awesome-swiper.js



```javascript
import Vue from 'vue'
import VueAwesomeSwiper from 'vue-awesome-swiper/dist/ssr'

Vue.use(VueAwesomeSwiper)
```



swiper的配置，目前版本需要安装 npm install swiper -D

```
import Vue from 'vue'
import 'swiper/css/swiper.css'
import VueAwesomeSwiper from 'vue-awesome-swiper/dist/vue-awesome-swiper.js'
Vue.use(VueAwesomeSwiper)
```



1. nuxt.config.js引入css及js



```javascript
css: [
    'swiper/dist/css/swiper.css',
],
plugins: [
    { src: "~/plugins/awesome-swiper.js", ssr: false },
],
```

1. 页面初始化



```javascript
<div v-swiper:mySwiper="swiperOption">
    <div class="swiper-wrapper">
         <div class="swiper-slide" v-for="(banner, index) in banners" :key="index">
            <img :src="banner">
         </div>
    </div>
    <div class="swiper-pagination swiper-pagination-bullets"></div>
</div>

export default {
  data () {
    return {
      banners: [ 
        require('~/assets/img/1540892214119.jpg'),
        require('~/assets/img/1540892214119.jpg'),
        require('~/assets/img/1540892214119.jpg')
      ],
      swiperOption: {
        autoplay: true,
        loop: true,
        pagination: {
          el: '.swiper-pagination',
        },
      }
    }
  },
}
```

##### 引入第三方模块(moment.js)

1. `npm install moment --save`
2. vue页面



```javascript
import moment from 'moment'
export default {
    mounted() {
      moment.locale('zh-cn') // moment.js 默认为英文，可通过此方法设置中文
      console.log(moment().format('dddd')) // 星期三
    },
}
```

为避免每个页面都引入moment，执行`moment.locale('zh-cn')`，可将其定义为全局方法

1. 在plugins文件夹下新建common.js



```javascript
import Vue from 'vue'
import moment from 'moment'
let common = {
  install (Vue) {
    Vue.prototype.$op = {
      'moment': (date) => {
        let newMoment = new moment(date)
        newMoment.locale('zh-cn')
        return newMoment
      }
    }
  }
}

Vue.use(common)
```

1. nuxt.config.js



```bash
plugins: [
    { src: '~/plugins/common.js', ssr: false }, 
],
```

1. vue页面



```kotlin
this.$op.moment().format('dddd')
```

##### 修改网站icon

icon.png文件存放在static文件夹下，nuxt.config.js中配置head属性



```javascript
head: {
    link: [
      { rel: 'icon', type: 'image/png', href: '/icon.png' }
    ]
  },
```

##### 关于中间件

中间件存放于middleware文件夹下，按使用场景可分为全局中间件和单页面中间件



```javascript
//全局使用
module.exports = {
  router: {
    middleware: '中间件名称'
  }  
}

//页面单独使用
export default {
    middleware: '中间件名称'
}
```

中间件执行流程顺序：
 nuxt.config.js -> 匹配布局 -> 匹配页面

##### PS.关于查看[NUXT 官网插件demo](https://nuxtjs.org/examples/plugins)时遇到的问题

![img](https:////upload-images.jianshu.io/upload_images/6550096-03df2b71d54ae52e.png?imageMogr2/auto-orient/strip|imageView2/2/w/927/format/webp)

屏幕快照 2018-10-26 下午4.58.47.png

按照index.vue通过`require('mini-toastr')`引入miniToastr，运行程序报错如下

![img](https:////upload-images.jianshu.io/upload_images/6550096-f53ce535f38e7a27.jpg?imageMogr2/auto-orient/strip|imageView2/2/w/930/format/webp)

1540544070985.jpg



打印miniToastr发现为一Module对象，init挂载在其default属性上



![img](https:////upload-images.jianshu.io/upload_images/6550096-62d76558fa3fd4d1.jpg?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

1540544125776.jpg

所以修改引入方法为



```php
miniToastr = require('mini-toastr').default
```

[为什么需要require().default](https://stackoverflow.com/questions/46215705/why-need-default-after-require-method-in-vue)

> When using ES6 imports (export default HeaderBar), the exported module is of the format {"default" : HeaderBar}. The import statement handles this assignment for you, however, you have to do the require("./mycomponent").default conversion yourself. The HMR interface code cannot use import as it doesn't work inline.

> If you want to avoid that, use module.exports instead of export default.

关于如上介绍，测试关于两种模块的导出方法
 方式一：export default
 新建test.js文件



```javascript
export default {
  test: function () {
    console.log('test')
  }
}
```

vue页面导入



```javascript
let obj = require('~/plugins/con.js').default
obj.test() // 打印‘test’

let obj = require('~/plugins/con.js')
obj.default.test() // 打印‘test’
```

此时 `require('~/plugins/con.js')` 打印为

![img](https:////upload-images.jianshu.io/upload_images/6550096-8b81d9b56f8da1d8.png?imageMogr2/auto-orient/strip|imageView2/2/w/624/format/webp)

屏幕快照 2018-10-26 下午5.35.24.png



方式二：module.exports



```javascript
const obj = {
  test: function () {
    console.log('test')
  }
}
module.exports = obj
```



```javascript
let obj = require('~/plugins/con.js')
obj.test() // 打印‘test’
```

此时 `require('~/plugins/con.js')` 打印为

![img](https:////upload-images.jianshu.io/upload_images/6550096-2ce4025f8e274251.png?imageMogr2/auto-orient/strip|imageView2/2/w/412/format/webp)



作者：然后呢_
链接：https://www.jianshu.com/p/b0626ba924c9
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。