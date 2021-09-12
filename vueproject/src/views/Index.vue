<template>
  <div>
    <Navigate_top :str="str"/>
    <el-empty v-if="article.length===0" :image-size="200"></el-empty>
    <div v-for="item in article" :key="item.index">
      <Article_list style=""  :article="item.fields"/>
      <div  style="color: #eee;">————————————————————————————————————————————————————————————</div>
    </div>
  </div>
</template>
<script>
// eslint-disable-next-line camelcase
import Article_list from '../components/Article_list'
// eslint-disable-next-line camelcase
import Navigate_top from '../components/Navigate_top'
export default {
  name: 'Index',
  // eslint-disable-next-line vue/no-unused-components
  components: { Article_list, Navigate_top },
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
      str: '1'
    }
  },
  created () {
    var that = this
    let i = 0
    this.$axios.get('http://127.0.0.1:8000/api/getarticle')
      .then(res => {
        that.article = res.data.list
        for (i = 0; i < that.article.length; i++) {
          that.article[i].fields.text = res.data.text[i]
          that.article[i].fields.authorname = res.data.author[i]
          that.article[i].fields.id = res.data.list[i].pk
        }
      })
  },
  methods: {
    gotoLogin () {
      this.$router.push({
        name: 'Home',
        params: {}
      })
    }
  }
}
</script>
