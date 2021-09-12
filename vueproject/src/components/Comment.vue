<template>
<div style="text-align: left;">
  <div style="margin-left: 30px">
    <div @click="gotohome" style="float: left;margin-right: 10px">
      <el-avatar size="medium" class="Headportrait" :src="comment.author.avatarurl"></el-avatar>
    </div>
    <div>
      <div v-if="comments.comment.status===0" style="line-height:28px">
        <font color="gray">{{comment.author.username}}</font>： {{comment.comment.value}}
      </div>
      <div v-else style="line-height:28px">
        <font color="gray">{{comment.author.username}} <font color="black">回复</font> {{comment.comment.towhich}}</font>： {{comment.comment.value}}
      </div>
      <div style="margin-left: 200px;font-size: small; ">
        <font color="darkgrey">{{comment.comment.time}}</font>
        <div style="display: inline;margin-left: 100px">
          <el-button type="text" @click="isshow=true" style="margin-right: 50px">回复</el-button>
          <el-button v-if="$store.state.user.id===comments.author.id" @click="deletec" type="text">删除</el-button>
        </div>
      </div>
      <div v-if="isshow" style="margin: 20px">
        <el-input style="width: 700px" placeholder="请发表您的评论 ~" v-model="sentence" class="input-with-select">
          <el-button @click="isshow=false;sentence=''" slot="prepend">关闭</el-button>
        </el-input>
        <el-button @click="addcomment" @keydown.enter.native="addcomment" style="float: right;margin-right: 20px" slot="append" type="success">回复Ta</el-button>
      </div>
    </div>
  </div>

  <div  style="color: #eee;">——————————————————————————————————————————————————————</div>
</div>
</template>

<script>
import store from '../store/index.js'
export default {
  name: 'Comment',
  store,
  props: {
    comments: {
      type: Object
    },
    id: {
      type: Number
    }
  },
  data () {
    return {
      comment: '',
      isshow: false,
      sentence: ''
    }
  },
  methods: {
    gotohome () {
      this.$router.replace({
        name: 'Mine',
        params: { id: this.comments.author.id }
      })
    },
    addcomment () {
      var that = this
      if (this.sentence === '') {
        this.$message.error('请填写评论内容')
      } else if (store.state.user.username === '') {
        this.$message.error('您还未登录')
      } else {
        this.$axios.post('http://127.0.0.1:8000/api/addcomment', {
          userid: store.state.user.id,
          articleid: that.id,
          value: that.sentence,
          status: 1,
          towhich: that.comments.author.username
        })
          .then(res => {
            that.sentence = ''
            that.isshow = false
            this.$emit('childevent', 'change')
          })
      }
    },
    deletec () {
      var that = this
      this.$confirm('您确定要删除这条评论吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$axios.post('http://127.0.0.1:8000/api/delcomment', {
          id: that.comments.comment.id
        })
          .then(res => {
            this.$emit('childevent', 'delete')
          })
      })
    }
  },
  created () {
    setTimeout(() => {
      this.comment = this.comments
    }, 100)
  }
}
</script>

<style scoped>

</style>
