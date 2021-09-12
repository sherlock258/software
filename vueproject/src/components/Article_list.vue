<template>
  <div>
    <div style="margin: 20px 300px 0px 300px">
      <div style="text-align: left">
        <el-button type="text" @click="gotoarticle()" style="font-size: 25px;font-weight: 600;color: #2c3e50" round> {{ article.title }}</el-button>
      </div>
      <div style="color: lightslategrey;text-align: left;margin-left: 25px;margin-bottom: 5px;font-size: 15px">摘要： {{ article.text }}</div>
      <div style="text-align: left;">
        <div style="display: inline;margin-left:100px" >
          <el-button type="text" style="font-size: 13px;color: grey;height: 10px" round> {{article.authorname}}</el-button>
          <el-button v-if="article.status==2" @click="gotoedit" type="text" style="font-size: 13px;color: grey;height: 10px" round> <u>编辑</u> </el-button>
        </div>
        <div style="display: inline;margin-left: 100px;font-size: 13px;color: grey;"><i  class="el-icon-star-off"></i>{{article.count}}</div>
        <div style="display: inline;margin-left:40px" >
          <el-tag v-if="article.status==2" type="info" size="mini">草稿</el-tag>
          <el-tag v-else type="info" size="mini">{{kind[article.kind].name}}</el-tag>
        </div>
      </div>
    </div>

  </div>

</template>

<style>

</style>

<script>
export default {
  name: 'Artilce_list',
  props: {
    article: Object
  },
  data () {
    return {
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
      ]
    }
  },
  mounted () {

  },
  methods: {
    gotoarticle () {
      var that = this
      this.$router.replace({
        name: 'Article',
        params: { Article_list: that.article.id }
      })
    },
    gotoedit () {
      this.$router.replace({
        name: 'Write',
        params: { article: this.article }
      })
    }
  }
}
</script>

<style scoped>

</style>
