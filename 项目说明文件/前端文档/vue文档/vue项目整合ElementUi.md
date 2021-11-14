# Vue整合ElementUi

> elementUI官网组件文档 ：[组件 | Element](https://element.eleme.cn/2.15/#/zh-CN/component/installation)

---



1. 在项目目录下使用npm下载elementui

   ```
   npm i element-ui -S
   ```

2. 下载完成之后会在package.json文件中出现引入的组件：
   ![image-20211114100357075](.\image-20211114100357075.png)

​	引入进来就是最新版本的，也可以自己调整版本。

​	***注意：在package.json文件中直接输入element-ui加上版本号，使用npm install 命令也可导入，所有的组件文件都放置在node_modules文件夹下面***

3. 在项目中完整的引入，在main.js中配置：

   ```
   /*引入elementUI*/
   import ElementUI from 'element-ui';
   import 'element-ui/lib/theme-chalk/index.css';
   Vue.use(ElementUI);
   /* --引入elementUI*/
   ```

这样就可以在项目中使用ElementUI组件了。







