<template>
  <div class="hello">
    <div style="display: flex;justify-content: center;margin-top: 100px">
      <el-card style="width: 400px">
        <div slot="header" class="clearfix">
          <span>Welcome!!</span>
        </div>
        <table>
          <tr>
            <td>邮箱</td>
            <td>
              <el-input v-model="user.email" placeholder="请输入邮箱" @keydown.enter.native="doLogin"></el-input>
            </td>
          </tr>
          <tr>
            <td>密码</td>
            <td>
              <el-input type="password" v-model="user.password" placeholder="请输入密码" @keydown.enter.native="doLogin"></el-input>
              <!-- @keydown.enter.native="doLogin"当按下enter键的时候也会执行doLogin方法-->
            </td>
          </tr>
          <tr>
            <!-- 占两行-->
            <td colspan="2">
              <!-- 点击事件的两种不同的写法v-on:click和 @click-->
              <!--<el-button style="width: 300px" type="primary" v-on:click="doLogin">登录</el-button>-->
              <div  align="right">
                <el-button style="width: 100px;color:dimgrey" type="text"  @click="forget">忘记密码？</el-button>
              </div>
              <el-button style="width: 350px " type="success" @click="doLogin">登录</el-button>
              <p></p>
              <el-button style="width: 350px " @click="register">注册</el-button>
            </td>
          </tr>
        </table>
      </el-card>
    </div>
  </div>
</template>

<script>
import store from '../store/index.js'
export default {
  name: 'Login',
  store,
  data () {
    return {
      user: {
        email: '',
        password: ''
      }
    }
  },
  methods: {
    doLogin: function () {
      var that = this
      if (this.user.email === '' || this.user.password === '') {
        this.$message.error('邮箱或密码不能为空！')
        return
      }
      this.$axios.post('http://127.0.0.1:8000/api/login', {
        email: that.user.email,
        password: that.user.password
      })
        .then(res => {
          if (res.data.msg === 'OK') {
            store.commit('store_user', { username: res.data.user[0], email: res.data.user[1], phone: res.data.user[2], id: res.data.user[3], avatar: res.data.user[4], description: res.data.user[5] })
            this.$message.success('登录成功！')
            this.$router.replace({
              name: 'Index',
              params: {}
            })
          } else {
            this.$message({
              type: 'error',
              message: '邮箱或密码错误 '
            })
          }
        })
    },
    forget () {
      this.$router.replace({ name: 'Forgetpass', params: {} })
    },
    register () {
      this.$router.replace({ name: 'Register', params: {} })
    }
  },
  props: {
    msg: String
  }
}
</script>
