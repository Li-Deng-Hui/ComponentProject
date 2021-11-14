
const stores={
    state:{
        name:'组件管理项目',
        token: window.localStorage.getItem('token'),
        auth: false,
        userInfo: {}
    },
    mutations:{
        setToken (state, token) {
            state.token = token
            window.localStorage.setItem('token', token)
        },
        clearToken (state) {
            state.token = ''
            window.localStorage.setItem('token', '')
        },
        setUserInfo (state, userInfo) {
            state.userInfo = userInfo
            state.auth = true // 获取到用户信息的同时将auth标记为true，当然也可以直接判断userInfo
        }
    },
    actions: {

    }
}
export default stores;