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
              <el-input  v-model="user.email" placeholder="请输入邮箱" @keydown.enter.native="doLogin"></el-input>
              <!-- @keydown.enter.native="doLogin"当按下enter键的时候也会执行doLogin方法-->
            </td>
          </tr>
          <tr>
            <td>新密码</td>
            <td>
              <el-input type="password" v-model="user.password1" placeholder="请输入新密码" @keydown.enter.native="doLogin"></el-input>
              <!-- @keydown.enter.native="doLogin"当按下enter键的时候也会执行doLogin方法-->
            </td>
          </tr>
          <tr>
            <td>再次输入密码</td>
            <td>
              <el-input type="password" v-model="user.password2" placeholder="请再次输入密码" @keydown.enter.native="doLogin"></el-input>
            </td>
          </tr>
          <tr>
            <!-- 占两行-->
            <td colspan="2">
              <!-- 点击事件的两种不同的写法v-on:click和 @click-->
              <!--<el-button style="width: 300px" type="primary" v-on:click="doLogin">登录</el-button>-->
              <p></p>
              <el-button type="success" style="width: 350px" @click="open">获取验证码</el-button>
            </td>
          </tr>
        </table>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Forgetpass',
  data () {
    return {
      user: {
        password1: '',
        password2: '',
        email: ''
      },
      code: '',
      error: false
    }
  },
  methods: {
    updatepass () {
      var that = this
      this.$axios.post('http://127.0.0.1:8000/api/userupdate', { username: '', password: that.user.password1, email: that.user.email, description: '' })
    },
    open () {
      var that = this
      if (that.user.username === '' || that.user.password1 === '' || that.user.password2 === '') {
        this.$message({
          type: 'error',
          message: '请把信息填写完整 '
        })
        return
      } else if (this.user.password1.length < 6) {
        this.$message({
          type: 'error',
          message: '输入的密码长度需要大于或等于6位 '
        })
        return
      } else if (this.user.password1.length >= 15) {
        this.$message({
          type: 'error',
          message: '输入的密码长度需要小于15位 '
        })
        return
      } else if (this.user.password1 !== this.user.password2) {
        this.$message({
          type: 'error',
          message: '两次输入密码不一致 '
        })
        return
      }
      this.$axios.post('http://127.0.0.1:8000/api/sendmail', { email: that.user.email })
        .then(res => {
          if (res.data.msg === 'NOTEXIST') {
            this.$message({
              type: 'error',
              message: '该用户不存在！ '
            })
          } else {
            that.code = res.data.code
            this.$prompt('验证码已发送，请查看', '提示', {
              confirmButtonText: '确定',
              cancelButtonText: '取消'
            }).then(({ value }) => {
              if (value === that.code) {
                this.$message({
                  type: 'success',
                  message: '修改成功，3秒后将跳转至首页 '
                })
                that.updatepass()
                this.timer = setTimeout(() => { // 设置延迟执行
                  this.$router.replace('/')
                }, 3500)
              } else {
                this.$message({
                  type: 'error',
                  message: '验证码错误 '
                })
              }
            }).catch(() => {
              this.$message({
                type: 'info',
                message: '取消输入'
              })
            })
          }
        })
    }
  },
  props: {
    msg: String
  },
  watch: {
    user: {
      handler (newuser, olduser) {
        this.error = false
      },
      deep: true

    }
  }
}
</script>
