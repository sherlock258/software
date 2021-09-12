<template>
<div>
  <Navigate_top :str="str" :router="router"/>
  <el-container style=" height:800px;background-color: #eeeeee">
    <el-main style=" margin:0 250px;background-color: white">
        <el-form style="margin-left: 100px;width: 700px;" label-position="left" label-width="80px">
          <el-form-item  style="text-align: left">
            <el-avatar style="float: left" :size="100" :src="avatar"></el-avatar>
            <el-button  size="small" @click="dialogTableVisible = true" type="primary" plain round style="margin-bottom: 50px;margin-top: 30px;margin-right: 370px;float: right">更换头像 </el-button>
          </el-form-item>
          <el-dialog title="请选择图片" :visible.sync="dialogTableVisible">
            <input type="file" id="pic">
            <span slot="footer" class="dialog-footer">
          <el-button @click="dialogTableVisible = false">取 消</el-button>
          <el-button type="primary" @click="upload">确 定</el-button>
      </span>
          </el-dialog>
          <el-form-item  label="用户名">
            <el-input  maxlength="15" show-word-limit v-model="username" style="width: 200px;margin-right: 400px"></el-input>
          </el-form-item>
          <el-divider></el-divider>
          <el-form-item label="手机号">
            <span style="margin-right: 300px" >{{ $store.state.user.phone.slice(0,3)+'****'+ $store.state.user.phone.slice(-4)}}</span>
          </el-form-item>
          <el-divider></el-divider>
          <el-form-item label="电子邮箱">
            <span style="margin-right: 300px" >{{ $store.state.user.email }}</span>
          </el-form-item>
          <el-divider></el-divider>
          <el-form-item  label="个人简介">
            <el-input maxlength="50" show-word-limit v-model="description" rows="5" type="textarea" style="width: 400px;height: 100px;margin-right: 400px"></el-input>
          </el-form-item>
          <el-divider></el-divider>
          <el-form-item label="修改密码">
            <el-button @click="forget" type="text" style="margin-right: 380px;float: right;color: dimgrey">点击修改 </el-button>
          </el-form-item>
          <el-divider></el-divider>
        </el-form>
      <el-button type="success" @click="save" round>保存</el-button>
    </el-main>
  </el-container>

</div>
</template>

<script>
// eslint-disable-next-line camelcase
import Navigate_top from '../components/Navigate_top'
import store from '../store/index.js'
export default {
  name: 'Setting',
  components: {
    Navigate_top
  },
  store,
  data () {
    return {
      str: '0',
      router: 'setting',
      username: '1',
      avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
      dialogTableVisible: false,
      description: ''
    }
  },
  methods: {
    forget () {
      this.$router.replace({ name: 'Forgetpass', params: {} })
    },
    upload () {
      var that = this
      var data = new FormData()
      data.append('id', store.state.user.id)
      var image = document.getElementById('pic').files[0]
      data.append('pic', image)
      this.$axios({
        url: 'http://127.0.0.1:8000/api/uploadpic',
        data: data,
        method: 'post'
      }).then((res) => {
        that.avatar = 'http://127.0.0.1:8000' + res.data.url
        store.state.user.avatar = 'http://127.0.0.1:8000' + res.data.url
      })
      this.dialogTableVisible = false
    },
    save () {
      var that = this
      if (this.username === '') {
        this.$message.error('请填写用户名')
        return
      }
      if (this.description === '') {
        this.description = '这位博主有点懒，还没有写个人介绍哦 ~'
      }
      this.$axios.post('http://127.0.0.1:8000/api/userupdate', {
        username: that.username,
        password: '',
        email: store.state.user.email,
        description: that.description
      })
        .then(res => {
          store.state.user.username = that.username
          store.state.user.description = that.description
          this.$message.success('保存成功！')
        })
    }
  },
  created () {
    this.username = store.state.user.username
    this.description = store.state.user.description
    if (store.state.user.avatar !== '') { this.avatar = store.state.user.avatar }
  }
}
</script>

<style>
.el-form-item__label{color:darkgrey}
</style>
