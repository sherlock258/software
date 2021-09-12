<template>
  <div>
    <Navigate_top :str="str" />
    <div class="home">
      <Login msg="Welcome to Your Vue.js App"/>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import Login from '@/components/Login.vue'
// eslint-disable-next-line camelcase
import Navigate_top from '../components/Navigate_top'
import store from '../store/index.js'
export default {
  name: 'Home',
  store,
  data () {
    return {
      str: '0'
    }
  },
  components: {
    Login, Navigate_top
  }
}
</script>
