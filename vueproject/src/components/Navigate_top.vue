<template>
  <el-menu :default-active="str" active-text-color="#f56c6c" class="el-menu-demo" mode="horizontal" @select="handleSelect">
    <img style="float: left ;margin-left: 50px" src="../assets/myblog.png">
    <el-menu-item style="margin-left: 150px ;margin-right: 50px" index="1">首页</el-menu-item>
    <el-menu-item index="2" style="margin-left: 50px">分类</el-menu-item>
    <el-menu-item style="margin-left: 150px" index="3" >
      <el-button @click="searched" type="text " style="color: darkgrey" icon="el-icon-search">搜索</el-button>
    </el-menu-item>
    <el-menu-item style="margin-left: 50px ;margin-right: 50px" index="4">
      <el-button v-if="!islogin" @click="gotoLogin" type="text" style="color: #2c3e50;" round>登录/注册</el-button>
      <el-dropdown  v-else style="color: #2c3e50;" @command="handleCommand">
      <span>
          <el-avatar size="large" :fit="fit" class="Headportrait" :src="avatar"></el-avatar>
          <i  class="el-icon-arrow-down el-icon--right"></i>
      </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item command="Mine"><i class="el-icon-s-home el-icon--right"></i>我的主页</el-dropdown-item>
          <el-dropdown-item command="Setting"><i class="el-icon-s-tools el-icon--right"></i> 设置 </el-dropdown-item>
          <el-dropdown-item command="Attention"><i class="el-icon-s-custom el-icon--right"></i>我的关注</el-dropdown-item>
          <el-dropdown-item command="Like"><i class="el-icon-star-on el-icon--right"></i>我的喜欢</el-dropdown-item>
          <el-dropdown-item command="Draft"><i class="el-icon-s-open el-icon--right"></i>草稿箱</el-dropdown-item>
          <el-dropdown-item command="Exit"><i class="el-icon-caret-left el-icon--right"></i>退出登录</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </el-menu-item>
    <el-menu-item index="5" >
      <el-button @click="gotowrite" type="danger" round>写文章</el-button>
    </el-menu-item>
  </el-menu>
</template>

<script>
import store from '../store/index.js'
export default {
  name: 'Navigate_top',
  store,
  props: {
    str: String,
    router: String
  },
  data () {
    return {
      // eslint-disable-next-line vue/no-dupe-keys
      search: '',
      islogin: false,
      avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
      fit: 'fill'
    }
  },
  created () {
    if (store.state.user.username !== '') { this.islogin = true }
    if (store.state.user.avatar !== '') { this.avatar = store.state.user.avatar }
  },
  methods: {
    handleSelect (key, keyPath) {
      if (key === '1') {
        this.$router.replace({
          name: 'Index'
        })
      }
      if (key === '2') {
        this.$router.replace({
          name: 'Kindlist'
        })
      }
      if (key === '4') { this.str = '0' }
    },
    searched () {
      this.$router.replace({
        name: 'Search'
      })
    },
    gotoLogin () {
      this.$router.replace({
        name: 'login',
        params: {}
      })
    },
    handleCommand (command) {
      if (command === 'Exit') {
        this.$confirm('您确定要退出登录吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          store.commit('logout')
          this.islogin = false
          this.$message({
            type: 'success',
            message: '已退出登录!'
          })
          this.timer = setTimeout(() => { // 设置延迟执行
            this.$router.replace('/')
          }, 1000)
        })
      } else if (command === 'Mine') {
        this.$router.replace({
          name: 'Mine',
          params: { id: '' }
        })
      } else {
        this.$router.replace({
          name: command,
          params: {}
        })
      }
    },
    gotowrite () {
      if (store.state.user.username === '') {
        this.$router.replace({
          name: 'Index',
          params: { }
        })
        this.$message.error('您还没有登录！')
      } else {
        this.$router.replace({
          name: 'Write',
          params: { article: '' }
        })
      }
    }
  }
}
</script>

<style scoped>

</style>
