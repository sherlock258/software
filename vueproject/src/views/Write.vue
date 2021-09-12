<template>
  <div style="background-color: #eeeeee">
    <div style="margin-bottom: 5px;">
      <el-button type="text" @click="gotomine" style="color: grey;font-size: 20px;margin-left: 10px;" round> {{ msg }}</el-button>
      <el-input class="inputs" v-model="title" style="width: 900px;margin-right: 50px;margin-left: 100px;border-radius: 5px" placeholder="请输入标题"></el-input>
      <el-button v-if="isnew||$route.params.article.status===2" type="danger" @click="drafts" plain round style="margin:0 20px">保存草稿</el-button>
      <el-button v-if="!isnew&&$route.params.article.status!==2" type="danger" @click="dialogTableVisible = true" style="margin-right: 50px" round>更新文章</el-button>
      <el-button v-else type="danger" @click="dialogTableVisible = true" style="margin-right: 50px" round>发布文章</el-button>
    </div>
    <el-dialog title="请选择文章的类型" :visible.sync="dialogTableVisible">
      <el-radio-group v-model="kind">
        <el-radio-button label=0>技术</el-radio-button>
        <el-radio-button label=1>生活</el-radio-button>
        <el-radio-button label=2>综合</el-radio-button>
        <el-radio-button label=3>其他</el-radio-button>
      </el-radio-group>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogTableVisible = false">取 消</el-button>
        <el-button type="primary" @click="publish">确 定</el-button>
      </span>
    </el-dialog>
    <mavon-editor v-model="content" :imageFilter = "uploadBefore" ref="md" @change="change" @imgAdd="$imgAdd" style="min-height: 600px; max-height: 650px" />
  </div>

</template>
<script>
import { mavonEditor } from 'mavon-editor'
import 'mavon-editor/dist/css/index.css'
import store from '../store'
export default {
  name: 'Write',
  components: {
    mavonEditor
  },
  store,
  data () {
    return {
      content: '',
      html: '',
      msg: '<    首页',
      title: '',
      dialogTableVisible: false,
      kind: 0,
      isnew: true
    }
  },
  methods: {
    gotomine () {
      this.$router.replace({
        name: 'Index'
      })
    },
    uploadBefore (f) {
      if (f.size > 2097152) {
        this.$message.error('图片限制大小为2M')
        return false
      } else {
        return true
      }
    },
    drafts () {
      var that = this
      if (this.title === '') {
        this.$message.error('标题不可以为空！')
      } else if (this.isnew) {
        this.$axios.post('http://127.0.0.1:8000/api/draft', {
          id: -1,
          title: that.title,
          content: that.content,
          html: that.html,
          authorid: store.state.user.id
        })
          .then(res => {
            this.$message.success('保存成功！')
            this.timer = setTimeout(() => { // 设置延迟执行
              this.$router.replace({
                name: 'Draft'
              })
            }, 2000)
          })
      } else {
        this.$axios.post('http://127.0.0.1:8000/api/draft', {
          id: this.$route.params.article.id,
          title: that.title,
          content: that.content,
          html: that.html
        })
          .then(res => {
            this.$message.success('保存成功！')
            this.timer = setTimeout(() => { // 设置延迟执行
              this.$router.replace({
                name: 'Draft'
              })
            }, 2000)
          })
      }
    },
    change (value, render) {
      this.content = value
      this.html = render
    },
    $imgAdd (pos, $file) {
      var data = new FormData()
      data.append('id', '')
      data.append('pic', $file)
      this.$axios({
        url: 'http://127.0.0.1:8000/api/uploadpic',
        data: data,
        method: 'post'
      }).then((res) => {
        var url = 'http://127.0.0.1:8000' + res.data.url
        this.$refs.md.$imglst2Url([[pos, url]])
      })
    },
    publish () {
      // eslint-disable-next-line no-unused-vars
      var that = this
      var kind = parseInt(this.kind)
      if (this.title === '') {
        this.$message.error('标题不可以为空！')
        this.dialogTableVisible = false
      } else if (this.content === '') {
        this.$message.error('文章不可以为空！')
        this.dialogTableVisible = false
      } else if (this.isnew) {
        this.$axios.post('http://127.0.0.1:8000/api/publish', {
          id: -1,
          title: that.title,
          content: that.content,
          html: that.html,
          authorid: store.state.user.id,
          kind: kind
        })
          .then(res => {
            this.$message.success('发布成功！')
            this.timer = setTimeout(() => { // 设置延迟执行
              this.$router.replace({
                name: 'Mine',
                params: { id: '' }
              })
            }, 2000)
          })
      } else {
        this.$axios.post('http://127.0.0.1:8000/api/publish', {
          id: this.$route.params.article.id,
          title: that.title,
          content: that.content,
          html: that.html,
          kind: kind
        })
          .then(res => {
            this.$message.success('更新成功！')
            this.timer = setTimeout(() => { // 设置延迟执行
              this.$router.replace({
                name: 'Mine',
                params: { id: '' }
              })
            }, 2000)
          })
      }
    }
  },
  created () {
    if (this.$route.params.article !== '') {
      this.title = this.$route.params.article.title
      this.content = this.$route.params.article.content
      this.isnew = false
    }
  }
}
</script>

<style scoped>
.inputs>>>input{
  border-color: #eeeeee;
}
</style>
