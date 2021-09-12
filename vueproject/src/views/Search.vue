<template>
<div>
  <el-container>
    <el-header style="margin-top: 50px;margin-bottom: 100px">
      <img  height="150" width="450" src="../assets/myblog1.png">
    </el-header>
    <el-header>
      <el-input style="width: 500px" clearable placeholder="请输入内容" v-model="key" class="input-with-select">
        <el-button slot="append" @click="serach" icon="el-icon-search"></el-button>
        <el-button slot="prepend" @click="gotoindex" icon="el-icon-house"></el-button>
      </el-input>
    </el-header>
    <el-main >
      <el-empty v-if="length===0" :image-size="200"></el-empty>
      <div v-else  v-for="item in article" :key="item.index">
        <Article_list style="display: inline;"  :article="item.fields"/>
        <div  style="color: #eee">————————————————————————————————————————————————————————————</div>
      </div>
    </el-main>
  </el-container>
</div>
</template>

<script>
// eslint-disable-next-line camelcase
import Navigate_top from '../components/Navigate_top'
// eslint-disable-next-line camelcase
import Article_list from '../components/Article_list'
import store from '../store/index.js'
export default {
  name: 'Search',
  components: {
    // eslint-disable-next-line vue/no-unused-components
    Navigate_top, Article_list
  },
  store,
  data () {
    return {
      str: '0',
      router: 'search',
      article: '',
      kind: [
        {
          id: 0,
          strid: '0',
          name: '技术'
        }, {
          id: 1,
          strid: '1',
          name: '生活'
        }, {
          id: 2,
          strid: '2',
          name: '综合'
        }, {
          id: 3,
          strid: '3',
          name: '其他'
        }
      ],
      key: '',
      length: 0
    }
  },
  methods: {
    serach () {
      var that = this
      let i = 0
      this.$axios.get('http://127.0.0.1:8000/api/search', { params: { key: that.key } })
        .then(res => {
          that.article = res.data.list
          for (i = 0; i < that.article.length; i++) {
            that.article[i].fields.text = res.data.text[i]
            that.article[i].fields.authorname = res.data.author[i]
            that.article[i].fields.id = res.data.list[i].pk
            that.length = that.article.length
          }
        })
    },
    gotoindex () {
      this.$router.replace({
        name: 'Index'
      })
    }
  },
  created () {
    this.article = this.$route.params.article
  },
  watch: {
    key (newkey, oldkey) {
      if (newkey === '') {
        this.article = ''
        this.length = 0
      }
    }
  }
}
</script>

<style scoped>
.input-with-select>>>input{
  border-color: #eee;
  background-color: #fff;
}
</style>
