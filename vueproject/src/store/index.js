import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: {
      username: '',
      email: '',
      phone: '',
      id: -1,
      description: ''
    }
  },
  mutations: {
    store_user (state, data) {
      this.state.user.username = data.username
      this.state.user.email = data.email
      this.state.user.phone = data.phone
      this.state.user.id = data.id
      this.state.user.avatar = data.avatar
      this.state.user.description = data.description
    },
    logout (state) {
      this.state.user.username = ''
      this.state.user.email = ''
      this.state.user.phone = ''
      this.state.user.id = -1
      this.state.user.avatar = ''
      this.state.user.description = ''
    }
  },
  actions: {
  },
  modules: {
  }
})
