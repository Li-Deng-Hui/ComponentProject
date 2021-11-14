<template>
  <div id="componentIndex">
    <h1>登录</h1>
    <h2>stores输出:{{getStores}}</h2>
    <h2>routers输出:{{getRoutes}}</h2>
    <el-button @click="goBack">回退</el-button>
  </div>
</template>
<script>
export default {
  name:'Login',
  data(){
    return{
      getStores:this.$store.state.name,
      getRoutes:this.$router.url,
    };
  },
  methods:{
    goBack () {
      window.history.length > 1 ? this.$router.go(-1) : this.$router.push('/')
    }
  }
}
</script>