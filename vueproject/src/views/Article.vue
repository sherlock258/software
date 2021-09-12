<template>
  <div>
    <Navigate_top :str="str"/>
    <el-container style="background-color: #eee;min-height: 800px">
      <el-aside width="300px" style="background-color: #eeeeee;">
        <el-tooltip v-if="!iscollect&&article.status==1" class="item" effect="dark" content="点赞" :open-delay=opendelay :hide-after=hideAfter placement="left">
          <el-button  @click="collect" icon="el-icon-star-off" circle style="position: fixed;left: 250px;top: 200px"></el-button>
        </el-tooltip>
        <el-tooltip v-if="iscollect&&article.status==1" class="item" effect="dark" content="取消点赞" :open-delay=opendelay :hide-after=hideAfter placement="left">
          <el-button @click="uncollect" type="danger" icon="el-icon-star-on" circle style="position: fixed;left: 250px;top: 200px"></el-button>
        </el-tooltip>
        <span v-if="article.status==1" style="position: fixed;left: 256px;top: 242px" >{{article.count}} 赞</span>
        <el-tooltip v-if="ismine" class="item" effect="dark" content="编辑" :open-delay=opendelay :hide-after=hideAfter placement="left">
          <el-button @click="gotoedit" icon="el-icon-edit" circle style="position: fixed;left: 250px;top: 280px"></el-button>
        </el-tooltip>
        <el-tooltip v-if="ismine" class="item" effect="dark" content="删除" :open-delay=opendelay :hide-after=hideAfter placement="left">
          <el-button @click="article_del" icon="el-icon-delete" circle style="position: fixed;left: 240px;top: 340px"></el-button>
        </el-tooltip>
      </el-aside>
      <el-container style=";background-color: white;margin-top: 10px;margin-right: 300px">
          <el-header style="margin-top: 30px;text-align: left;font-size: 35px;font-weight: 900">
            {{article.title}}
          </el-header>
          <el-container style="margin-left: 30px;margin-top: 20px;text-align: left">
            <el-aside width="80px">
              <div  @click="gotoauthor">
                <el-avatar :size="size" class="Headportrait" :src="avatar"></el-avatar>
              </div>
            </el-aside>
            <div style="margin-top: 10px">
              <div>
                <div style="display: inline;">{{article.authorname}}</div>
                <div style="display: inline;">
                  <el-button v-if="!ismine" @click="attentioned" type="danger" style="margin-left: 10px;" plain round size="mini">{{attention}}</el-button>
                  <el-button v-else @click="gotomine" type="info" style="margin-left: 10px;" plain round size="mini"> 我的主页</el-button>
                </div>
              </div>
              <div style="margin-top: 10px">
                <div style="font-size:10px; display: inline;color: darkgrey;margin-top: 5px;margin-left: 10px">
                  {{article.time}}
                </div>
                <div style="font-size:10px;display: inline;color: darkgrey;margin-top: 5px;margin-left: 10px">
                  字数：{{length}}
                </div>
              </div>
            </div>
          </el-container>
          <el-main v-html="article.html" style="text-align: left" ></el-main>
          <div style="background-color: #eeeeee;height: 10px"></div>
          <div style="margin: 20px">
            <el-input style="width: 700px" placeholder="请发表您的评论 ~" v-model="sentence" @keydown.enter.native="addcomment" class="input-with-select"></el-input>
            <el-button @click="addcomment" style="float: right;margin-right: 20px" slot="append"  type="success">发表评论</el-button>
          </div>
          <div v-if="comments.length>0">
            <div style="margin-top: 10px" v-for="item in comments" :key="item.index">
              <Comment :comments="item" :id="article.id" @childevent="ischange" />
            </div>
            <div style="height: 40px"></div>
          </div>
        </el-container>
    </el-container>
  </div>

</template>

<script>
// eslint-disable-next-line camelcase
import Navigate_top from '../components/Navigate_top'
import Comment from '../components/Comment'
import store from '../store/index.js'
export default {
  name: 'Article',
  store,
  components: {
    // eslint-disable-next-line vue/no-unused-components
    Navigate_top,
    // eslint-disable-next-line vue/no-unused-components
    Comment
  },
  data () {
    // eslint-disable-next-line no-unused-expressions,no-labels
    return {
      article: '',
      str: '0',
      iscollect: false,
      size: 70,
      ismine: false,
      opendelay: 500,
      hideAfter: 1500,
      length: 0,
      avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
      attention: '关注',
      comments: [],
      sentence: ''
    }
  },
  methods: {
    uncollect () {
      var that = this
      this.$axios.post('http://127.0.0.1:8000/api/uncollect', {
        userid: store.state.user.id,
        articleid: that.article.id
      })
        .then(res => {
          this.$notify({
            position: 'top-left',
            type: 'success',
            message: '已取消',
            duration: 1000
          })
        })
      this.iscollect = false
      this.article.count--
    },
    collect () {
      var that = this
      this.$axios.post('http://127.0.0.1:8000/api/collect', {
        userid: store.state.user.id,
        articleid: that.article.id
      })
        .then(res => {
          this.$notify({
            position: 'top-left',
            type: 'success',
            message: '点赞成功',
            duration: 1000
          })
        })
      this.iscollect = true
      this.article.count++
    },
    gotomine () {
      this.$router.replace({
        name: 'Mine',
        params: { id: '' }
      })
    },
    ischange (data) {
      var that = this
      let i = 0
      that.comments = []
      this.$axios.get('http://127.0.0.1:8000/api/getcomment', { params: { articleid: that.article.id } })
        .then(res => {
          for (i = 0; i < res.data.comment.length; i++) {
            that.comments.push({})
            that.comments[i].comment = res.data.comment[i].fields
            that.comments[i].comment.time = res.data.time[i]
            that.comments[i].author = res.data.author[i].fields
            that.comments[i].comment.id = res.data.comment[i].pk
            that.comments[i].author.id = res.data.author[i].pk
          }
          if (data === 'change') {
            this.$message.success('评论成功')
            that.sentence = ''
          } else {
            this.$message.success('删除成功')
            console.log(that.comments)
          }
        })
    },
    gotoauthor () {
      this.$router.replace({
        name: 'Mine',
        params: { id: this.article.author }
      })
    },
    // eslint-disable-next-line vue/no-dupe-keys
    attentioned () {
      var that = this
      if (this.attention === '关注') {
        this.$axios.post('http://127.0.0.1:8000/api/attention', {
          liking: store.state.user.id,
          liked: that.article.author
        })
          .then(res => {
            this.attention = '取消关注'
            this.$message.success('关注成功')
          })
      } else {
        this.$axios.post('http://127.0.0.1:8000/api/unattention', {
          liking: store.state.user.id,
          liked: that.article.author
        })
          .then(res => {
            this.attention = '关注'
            this.$message.success('您已取关')
          })
      }
    },
    gotoedit () {
      this.$router.replace({
        name: 'Write',
        params: { article: this.article }
      })
    },
    article_del () {
      var that = this
      this.$confirm('此操作将永久删除文章, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$axios.post('http://127.0.0.1:8000/api/articledel', { id: that.article.id })
          .then(res => {
            this.$message.success('删除成功！')
            this.timer = setTimeout(() => { // 设置延迟执行
              this.$router.replace('/')
            }, 2000)
          })
      })
    },
    addcomment () {
      var that = this
      let i = 0
      if (this.sentence === '') {
        this.$message.error('请填写评论内容')
      } else if (store.state.user.username === '') {
        this.$message.error('您还未登录')
      } else {
        this.$axios.post('http://127.0.0.1:8000/api/addcomment', {
          userid: store.state.user.id,
          articleid: that.article.id,
          value: that.sentence,
          status: 0
        })
          .then(res => {
            that.comment = []
            this.$axios.get('http://127.0.0.1:8000/api/getcomment', { params: { articleid: that.article.id } })
              .then(res => {
                for (i = 0; i < res.data.comment.length; i++) {
                  that.comments.push({})
                  that.comments[i].comment = res.data.comment[i].fields
                  that.comments[i].comment.time = res.data.time[i]
                  that.comments[i].author = res.data.author[i].fields
                  that.comments[i].comment.id = res.data.comment[i].pk
                  that.comments[i].author.id = res.data.author[i].pk
                }
                this.$message.success('评论成功')
                that.sentence = ''
              })
          })
      }
    }
  },
  beforeCreate () {
    // eslint-disable-next-line no-unused-vars
    var that = this
    // eslint-disable-next-line no-unused-vars
    let i = 0
    const id = this.$route.params.Article_list
    this.$axios.get('http://127.0.0.1:8000/api/articleid', { params: { id: id } })
      .then(res => {
        that.article = res.data.list
        for (i = 0; i < that.article.length; i++) {
          that.article[i].fields.authorname = res.data.author
          that.article[i].fields.time = res.data.time
          that.article[i].fields.text = res.data.text
          that.article[i].fields.id = res.data.list[i].pk
          if (res.data.avatar !== '') { that.avatar = res.data.avatar }
        }
        that.article = that.article[0].fields
        that.ismine = that.article.author === store.state.user.id
        that.length = that.article.text.length
        this.$axios.post('http://127.0.0.1:8000/api/selinlike', {
          userid: store.state.user.id,
          articleid: that.article.id
        })
          .then(res => {
            that.iscollect = res.data.msg === 'Liked'
          })
        this.$axios.post('http://127.0.0.1:8000/api/selinattention', {
          liking: store.state.user.id,
          liked: that.article.author
        })
          .then(res => {
            if (res.data.msg === 'Attentioned') that.attention = '取消关注'
          })
        this.$axios.get('http://127.0.0.1:8000/api/getcomment', { params: { articleid: that.article.id } })
          .then(res => {
            for (i = 0; i < res.data.comment.length; i++) {
              that.comments.push({})
              that.comments[i].comment = res.data.comment[i].fields
              that.comments[i].comment.time = res.data.time[i]
              that.comments[i].author = res.data.author[i].fields
              that.comments[i].comment.id = res.data.comment[i].pk
              that.comments[i].author.id = res.data.author[i].pk
            }
          })
      })
  },
  watch: {
    ischange () {
      console.log('change')
    }
  }
}
</script>

<style scoped>

</style>
