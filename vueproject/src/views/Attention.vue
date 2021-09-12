<template>
<div>
  <Navigate_top :str="str" :router="router"/>
    <el-container style="background-color: white;margin: 0 500px 0 300px ">
      <el-header style="text-align: left;margin-top: 50px">
        <el-container>
          <el-aside width="180px">
            <el-avatar style="margin-left: 70px;margin-top: 10px" :size="100" :src="avatar"></el-avatar>
          </el-aside>
          <el-main >
            <div style="font-weight: 600;font-size: 30px;text-align: left">
              {{$store.state.user.username}}
            </div>
            <div style="color: darkgrey;font-size: 10px;text-align: left;margin-bottom: 10px">
              邮箱：{{$store.state.user.email}}
            </div>
            <el-tag size="mini" type="info">{{$store.state.user.description}}</el-tag>
          </el-main>
        </el-container>
      </el-header>
      <el-main style="margin-left: 100px;margin-top: 50px">
        <el-tabs v-model="activeIndex">
          <el-tab-pane name="liking" >
            <span slot="label" style="color: dimgrey;font-weight: 600;margin: 0 50px;text-align: center"> 关注</span>
            <el-empty v-if="liking.length===0" :image-size="200"></el-empty>
            <div @click.stop="gotohome(item)" v-for="item in liking" :key="item.index">
              <el-container>
                <el-aside width="80px">
                  <el-avatar style="margin-top: 10px" :size="80" :src="item.fields.avatarurl"></el-avatar>
                </el-aside>
                <el-main style="text-align: left">
                  <div style="font-weight: 500;font-size: 25px;text-align: left">
                    {{item.fields.username}}
                  </div>
                  <div style="color: darkgrey;font-size: 10px;text-align: left;margin-bottom: 10px">
                    邮箱：{{item.fields.email}}
                  </div>
                  <el-tag size="mini" type="info">{{item.fields.description}}</el-tag>
                </el-main>
              </el-container>
            </div>
          </el-tab-pane>
          <el-tab-pane  name="liked">
            <span slot="label" style="color: dimgrey;font-weight: 600;margin: 0 50px;text-align: center"> 粉丝</span>
            <el-empty v-if="liked.length===0" :image-size="200"></el-empty>
            <div @click.stop="gotohome(item)" v-for="item in liked" :key="item.index">
              <el-container>
                <el-aside width="80px">
                  <el-avatar style="margin-top: 10px" :size="80" :src="item.fields.avatarurl"></el-avatar>
                </el-aside>
                <el-main style="text-align: left">
                  <div style="font-weight: 500;font-size: 25px;text-align: left">
                    {{item.fields.username}}
                  </div>
                  <div style="color: darkgrey;font-size: 10px;text-align: left;margin-bottom: 10px">
                    邮箱：{{item.fields.email}}
                  </div>
                  <el-tag size="mini" type="info">{{item.fields.description}}</el-tag>
                </el-main>
              </el-container>
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-main>
    </el-container>
</div>
</template>

<script>
// eslint-disable-next-line camelcase
import Navigate_top from '../components/Navigate_top'
import store from '../store/index.js'
export default {
  name: 'Attention',
  store,
  components: {
    Navigate_top
  },
  data () {
    return {
      str: '0',
      router: 'attention',
      liking: '',
      liked: '',
      avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
      activeIndex: 'liking'
    }
  },
  methods: {
    gotohome (item) {
      this.$router.replace({
        name: 'Mine',
        params: { id: item.pk }
      })
    }
  },
  created () {
    // eslint-disable-next-line no-unused-vars
    var that = this
    this.$axios.get('http://127.0.0.1:8000/api/getattention', { params: { userid: store.state.user.id } })
      .then(res => {
        that.liked = res.data.liked
        that.liking = res.data.liking
      })
    if (store.state.user.avatar !== '') this.avatar = store.state.user.avatar
  }
}
</script>

<style scoped>
.el-tabs__item{
  font-size:18px !important;
}
</style>
