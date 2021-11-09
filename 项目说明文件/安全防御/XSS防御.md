防御XSS的一些原理和思想，对输入进行过滤，对输出进行编码。那么OWASP组织中项目 AntiSamy 和 ESAPI 就恰恰能够帮助我们。其中 AntiSamy 提供了 XSS Filter 的实现，而 ESAPI 则提供了对输出进行编码的实现。(samy是一个人名，他第一次在MySpace上实现第一个*XSS*工具蠕虫，所以AntiSamy项目就是反XSS攻击的意思; ESAPI就是enterprise security api的意思；owasp: Open Web Application Securtiy Project)

[XSS 防御方法总结 - 茄子_2008 - 博客园 (cnblogs.com)](https://www.cnblogs.com/xd502djj/p/10786865.html)



### **XSS介绍**

跨站脚本攻击指的是自己的网站运行了别的网站里面的代码
攻击原理是原本需要接受数据但是一段脚本放置在了数据中：

![img](https://pic1.zhimg.com/80/v2-b72619a29189bed5544cefd048a94ec0_720w.jpg)

该攻击方式能做什么？

- 获取页面数据
- 获取Cookies
- 劫持前端逻辑
- 发送请求到攻击者自己的网站实现资料的盗取
- 偷取网站任意数据
- 偷取用户密码和登陆状态
- 改变按钮的逻辑

### **XSS攻击类型**

其实XSS的种类非常的多尤其是变种的特别多，大致可以分为两种
**反射型：是通过URL参数直接注入，一般是使用alert来探测站点是否防御，直接攻击的使用src来引入自己的脚本**

```text
http://localhost:1521/?from=<script>alert(1)</script>bing
```

**存储型：存储到DB后读取时注入（危害很大）**
**在评论的时候写script标签，这样数据就是存储在数据库中的，如果该页面要读取出这条有script标签的信息那么将这个网址发给别人别人也会中招。**

XSS攻击注入点：

html节点内容：如果一个节点是动态生成的，有可能这个节点的数据有脚本（用户输入信息）

html属性：某个html的属性是由用户输入的，输入的内容可能有脚本

```text
<img src="1" onerror="alert(1)"/>
1" onerror="alert(1) // src被提前关闭
```

js代码：js代码中存在后台注入的变量或者用户输入的信息

```text
localhost:1521/?from=google";alert(1);"
```

富文本：其实是一大段的html，我们需要保留格式又要去掉script标签，这是比较麻烦的

富文本得保留HTML，HTML有XSS就有攻击风险
实际上浏览器有着XSS的部分防御机制，可以通过

```text
ctx.set('X-XSS-Protection',0); // 0-disable 1-enable
```

来进行关闭，浏览器的防御很有限，只能是反射型的参数并且出现在html节点和属性中才会进行防御，在js和富文本中是不会拦截的。

### **五种防御方式**

**HTML节点内容的XSS防御**
转义掉<<和>> 即转义掉<>即可，转义的时机有两种，一种是写入数据库的时候进行转义，另一种实在解析的时候进行转义。

这里是在显示的时候转义

```text
var escapeHtml = function(str){
  str = str.replace(/>/g, '&lt;');
  str = str.replace(/>/g, '&gt;');
  return str;
}

escapeHtml(content);
```

**HTML属性的XSS防御**
转义”&quto; 即转义掉双引号，'转义掉单引号，(另一个要注意的是实际上html的属性可以不包括引号，因此严格的说我们还需要对空格进行转义，但是这样会导致渲染的时候空格数不对，因此我们不转义空格，然后再写html属性的时候全部带上引号)这样属性就不会被提前关闭了

```text
var escapeHtmlProperty = function(str){
  str = str.replace(/"/g, '&quto;');
  str = str.replace(/'/g, '&#39;');
  str = str.replace(/ /g, '&#32;');
  return str;
}

escapeHtml(content);
```

其实以上这两个函数可以合并成一个函数，这样不管是内容还是属性都可以使用一个函数来过滤了：

**HTML转义函数**

```text
var escapeHtmlProperty = function(str){
  if(!str) return '';
  str = str.replace(/&/g, '&amp;');
  str = str.replace(/>/g, '&lt;'); 
  str = str.replace(/>/g, '&gt;');
  str = str.replace(/"/g, '&quto;');
  str = str.replace(/'/g, '&#39;');
  return str;
}

escapeHtml(content);
```

**js转义**

转义”\”或者替换成json

```text
var escapeForJs = function(str){
 if(!str) return '';
 str = str.replace(/\\/g,'\\\\');
 str = str.replace(/"/g,'\\"');
}
```

这里的解决方式并不完整，因为还有可能是单引号或者其他形势包裹的，这里最保险的方法其实很简单，就是对数据做一次JSON.stringify即可

**富文本**

由于需要完整的HTML因此不太容易过滤，一般是按照白名单进行保留部分标签和属性来进行过滤，除了允许的标签和属性，其他的全部不允许（也有黑名单的方式，但是由于html复杂效果比较差，原理就是之前的正则替换）

其实可以用别人写好的XSS组件就叫做xss，直接

```text
npm install xss
```

白名单-使用第三方库XSS，支持指定白名单

```text
var xssFilter = function(html){
    if(!html) return '';

    var xss = require('xss');
    var ret = xss(html, {
        whiteList:{
            img: ['src'],
            a: ['href'],
            font: ['size', 'color']
        },
        onIgnoreTag: function(){
            return '';
        }
    });


    console.log(html, ret);

    return ret;
};
```