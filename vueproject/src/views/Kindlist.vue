<template>
  <div>
   <Navigate_top :str="str"/>
    <div>
      <el-container >
        <el-aside width="200px">
          <el-menu :default-active="activeIndex" active-text-color="#f56c6c" class="el-menu-vertical-demo" @select="handleSelect">
            <el-menu-item  v-for="item in kind" :key="item.id" :index="item.strid">
              <i class="el-icon-menu"></i>
              <span slot="title">{{ item.name }}</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main v-if="article.length!==0">
          <div style="float: right;margin-right:200px" v-for="item in article" :key="item.index">
            <Article_list style="display: inline;"  :article="item.fields"/>
            <div  style="color: #eee;margin-left: 300px">————————————————————————————————————————————————————————————</div>
          </div>
        </el-main>
        <el-main v-if="article.length===0">
          <el-empty :image-size="200"></el-empty>
        </el-main>
      </el-container>
    </div>

  </div>

</template>

<script>
// eslint-disable-next-line camelcase
import Navigate_top from '../components/Navigate_top'
// eslint-disable-next-line camelcase
import Article_list from '../components/Article_list'

export default {
  name: 'Kindlist',
  components: {
    Article_list,
    // eslint-disable-next-line vue/no-unused-components
    Navigate_top
  },
  data () {
    return {
      activeIndex: '0',
      article: '',
      str: '2',
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
      ]
    }
  },
  created () {
    var that = this
    let i = 0
    this.$axios.get('http://127.0.0.1:8000/api/selectkind', { params: { kind: 0 } })
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
    },
    handleSelect (key, keyPath) {
      var that = this
      let i = 0
      this.$axios.get('http://127.0.0.1:8000/api/selectkind', { params: { kind: key } })
        .then(res => {
          that.article = res.data.list
          for (i = 0; i < that.article.length; i++) {
            that.article[i].fields.text = res.data.text[i]
            that.article[i].fields.authorname = res.data.author[i]
            that.article[i].fields.id = res.data.list[i].pk
          }
        })
    }
  }
}
</script>

<style scoped>
.inputs>>>input{
  border-color: #f56c6c;
}
</style>
