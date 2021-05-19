<template>
  <v-app>
    <v-app-bar
      app
      color="indigo darken-2"
      elevation="2"
      dark
    >
      <div class="d-flex align-center">
        <v-btn class="ml-2"
        :to="{ name: 'Home' }" text>Quora Clone
        </v-btn>
      </div>

      <v-spacer></v-spacer>

      <v-btn
        v-if="isAuthenticated"
        :to="{ name: 'QuestionEditor'}"
        text
      >
        <span class="mr-2">Ask a Question</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
      <v-btn
        v-if="isAuthenticated"
        text
        @click="logout"
      >
        <span class="mr-2">Logout</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
      <v-btn
        v-if="!isAuthenticated"
        :to="{ name: 'Login'}"
        text
      >
        <span class="mr-2">Login</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
      <v-btn
        v-if="!isAuthenticated"
        :to="{ name: 'Register'}"
        text
      >
        <span class="mr-2">Register</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>
import { isValidJwt } from '@/utils/jwtValidator'
import axios from 'axios'

export default {
  name: 'App',
  data: () => ({
    isAuthenticated: false
  }),

  methods: {
    isAuthenticate () {
      const token = window.localStorage.getItem("jwt");
      console.log(token)
      this.isAuthenticated = isValidJwt(token)
      return this.isAuthenticated
    },
    logout () {
      const token = window.localStorage.getItem("jwt");
      axios.post(`/user/logout`, {}, { headers: { Authorization: `Bearer ${token}` } })
        .then(() => window.localStorage.removeItem("jwt"))
        .then(() => this.isAuthenticate())
        .then(() => this.$router.push('/'))
        .catch(error => {
          console.log(error)
        })
    },
  },

  created(){
    this.isAuthenticate()
  },
  beforeUpdate(){
    this.isAuthenticate()
  }
};
</script>
