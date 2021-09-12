<template>
<div>
  <Navigate_top :str="str"/>
  <el-container>
    <el-aside width="350px">
      <el-card style="margin-top: 100px;margin-left: 30px;height: 200px" class="box-card">
        <el-container>
          <el-header>
            <el-container>
              <el-aside width="60px">
                <el-avatar style="margin-top: 10px" :size="50" :src="user.avatarurl"></el-avatar>
              </el-aside>
              <el-main >
                <div style="font-weight: 600;font-size:15px;text-align: left">
                  {{user.username}}
                </div>
                <div style="text-align: left">
                  <el-button v-if="!ismine" @click="attentioned" type="danger" style="margin-top: 5px" plain round size="mini">{{attention}}</el-button>
                </div>
              </el-main>
            </el-container>
          </el-header>
          <el-main style="text-align: left;">
            <div style="color: darkgrey;font-size: 10px;text-align: left;margin-bottom: 10px">
              邮箱：{{user.email}}
            </div>
            <div style="background-color:#eee;color: darkgrey;font-size: 10px;padding:2px;border:1px solid gainsboro;display:inline-block;border-radius: 5px">
              {{user.description}}
            </div>
          </el-main>
        </el-container>
      </el-card>
    </el-aside>
    <el-main>
      <div style="float: right;margin-left: 500px;margin-right:200px" v-for="item in article" :key="item.index">
        <Article_list style="display: inline;"  :article="item.fields"/>
        <div  style="color: #eee;margin-left: 300px">————————————————————————————————————————————————————————————</div>
      </div>
      <el-empty v-if="article.length===0" :image-size="200"></el-empty>
    </el-main>
  </el-container>

</div>
</template>

<script>
// eslint-disable-next-line camelcase
import Navigate_top from '../components/Navigate_top'
// eslint-disable-next-line camelcase,no-unused-vars
import Article_list from '../components/Article_list'
import store from '../store/index.js'
export default {
  name: 'Mine',
  store,
  components: {
    Navigate_top,
    Article_list
  },
  data () {
    return {
      article: '',
      kind: [
        {
          id: 0,
          name: '技术'
        }, {
          id: 1,
          name: '生活'
        }, {
          id: 2,
          name: '综合'
        }, {
          id: 3,
          name: '其他'
        }
      ],
      str: '0',
      user: '',
      attention: '关注 +',
      ismine: true
    }
  },
  methods: {
    attentioned () {
      var that = this
      if (this.attention === '关注 +') {
        this.$axios.post('http://127.0.0.1:8000/api/attention', {
          liking: store.state.user.id,
          liked: that.user.id
        })
          .then(res => {
            this.attention = '取消关注'
            this.$message.success('关注成功')
          })
      } else {
        this.$axios.post('http://127.0.0.1:8000/api/unattention', {
          liking: store.state.user.id,
          liked: that.user.id
        })
          .then(res => {
            this.attention = '关注 +'
            this.$message.success('您已取关')
          })
      }
    }
  },
  created () {
    var that = this
    let i = 0
    let id = store.state.user.id
    if (this.$route.params.id !== '') {
      id = this.$route.params.id
      this.ismine = false
    }
    this.$axios.get('http://127.0.0.1:8000/api/userarticle', { params: { authorid: id } })
      .then(res => {
        that.user = res.data.user[0].fields
        that.user.id = res.data.user[0].pk
        that.article = res.data.list
        for (i = 0; i < that.article.length; i++) {
          that.article[i].fields.text = res.data.text[i]
          that.article[i].fields.authorname = res.data.author[i]
          that.article[i].fields.id = res.data.list[i].pk
        }
        this.$axios.post('http://127.0.0.1:8000/api/selinattention', {
          liking: store.state.user.id,
          liked: that.user.id
        })
          .then(res => {
            if (res.data.msg === 'Attentioned') that.attention = '取消关注'
          })
      })
  }
}
</script>

<style scoped>

</style>
