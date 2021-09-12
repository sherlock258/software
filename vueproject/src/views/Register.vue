<template>
  <div class="hello">
    <div style="display: flex;justify-content: center;margin-top: 60px">
      <el-card style="width: 400px">
        <div slot="header" class="clearfix">
          <span>Welcome!!</span>
        </div>
        <table>
          <tr>
            <td>用户名</td>
            <td>
              <el-input v-model="user.username" placeholder="请输入用户名" @keydown.enter.native="register"></el-input>
            </td>
          </tr>
          <tr>
            <td>密码</td>
            <td>
              <el-input type="password" v-model="user.password1" placeholder="请输入密码" @keydown.enter.native="register"></el-input>
              <!-- @keydown.enter.native="doLogin"当按下enter键的时候也会执行doLogin方法-->
            </td>
          </tr>
          <tr>
            <td>再次输入密码</td>
            <td>
              <el-input type="password" v-model="user.password2" placeholder="请再次输入密码" @keydown.enter.native="register"></el-input>
              <!-- @keydown.enter.native="doLogin"当按下enter键的时候也会执行doLogin方法-->
            </td>
          </tr>
          <tr>
            <td>电子邮箱</td>
            <td>
              <el-input v-model="user.email" placeholder="请输入电子邮箱" @keydown.enter.native="register"></el-input>
              <!-- @keydown.enter.native="doLogin"当按下enter键的时候也会执行doLogin方法-->
            </td>
          </tr>
          <tr>
            <td>电话号码</td>
            <td>
              <el-input v-model="user.phone" placeholder="请输入电话号码" @keydown.enter.native="register"></el-input>
              <!-- @keydown.enter.native="doLogin"当按下enter键的时候也会执行doLogin方法-->
            </td>
          </tr>
          <tr>
            <!-- 占两行-->
            <td colspan="2">
              <el-button style="width: 350px " type="success" @click="register" :loading="success">注册</el-button>
            </td>
          </tr>
        </table>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Register',
  data () {
    return {
      user: {
        username: '',
        password1: '',
        password2: '',
        email: '',
        phone: ''
      },
      success: false
    }
  },
  methods: {
    register: function () {
      var that = this
      if (this.user.username === '' || this.user.password1 === '' || this.user.password2 === '' || this.user.email === '' || this.user.phone === '') {
        this.$message.error('注册信息请填写完整！')
      } else if (this.user.password1 !== this.user.password2) {
        this.$message.error('两次密码不一致！')
      } else if (this.user.password1.length < 6) {
        this.$message.error('输入的密码长度需要大于6位！')
      } else if (this.user.username.length > 15) {
        this.$message.error('用户名过长！')
      } else if (this.user.password1.length > 20) {
        this.$message.error('密码应小于20位！')
      } else if (this.user.email.length > 30) {
        this.$message.error('请输入正确的邮箱！')
      } else if (this.user.phone.length !== 11) {
        this.$message.error('请输入正确的电话号码!')
      } else {
        this.$axios.post('http://127.0.0.1:8000/api/register', {
          username: that.user.username,
          password: that.user.password1,
          email: that.user.email,
          phone: that.user.phone
        })
          .then(res => {
            if (res.data.msg === 'OK') {
              that.success = true
              this.timer = setTimeout(() => {
                this.$message.success('注册成功')// 设置延迟执行
                this.$router.replace('/login')
              }, 1000)
            } else if (res.data.msg === 'EXIST') {
              that.error = true
              that.message = '该邮箱已被注册！'
            }
          })
      }
    }
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
