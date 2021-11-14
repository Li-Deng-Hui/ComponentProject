import ComponentIndex from '../pages/index';
import UserLogin from '../pages/user/Login/index'

const routers=[
    {path:'/',name:'componentIndex',component:ComponentIndex},
    {path: '/user/login',name:'userLogin',component: UserLogin}
]

export default routers;