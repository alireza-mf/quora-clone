<template>
  <v-container>
      <v-flex>
        <v-card v-if="errMsg" flat class="ma-auto my-2 pa-1 text-h6 text-center" width="480" color="red">
          {{errMsg}}
        </v-card>
        <v-card class="ma-auto" color="indigo" width="480px" height="545px">
        <v-container style="position: relative;top: 5%;" class="ma-auto">
          <v-card class="px-4" flat elevation="6">
            <v-card-title primary-title>
              <h4>Register</h4>
            </v-card-title>
            <v-form>
            <v-text-field prepend-icon="mdi-email" outlined v-model="email" :rules="[val=>!!val||'Required']" label="Email" type="email"></v-text-field>
            <v-text-field prepend-icon="mdi-account" outlined v-model="name" :rules="[val=>!!val||'Required']" label="Name"></v-text-field>
            <v-text-field prepend-icon="mdi-lock" outlined v-model="password" :rules="[val=>!!val||'Required']" label="Password" type="password"></v-text-field>
            <v-card-actions>
              <v-row>
                <v-btn class="mb-5" color="indigo" large block dark @click="register">Register</v-btn>
                <v-btn class="mb-5" color="#4285f4" large block dark>
                  <v-icon>mdi-google</v-icon>{{"\xa0\xa0"}}Register via Google
                </v-btn>
              </v-row>
            </v-card-actions>
            </v-form>
          </v-card>
        </v-container>
        </v-card>
      </v-flex>
      <v-row justify="center" class="ma-3">
        <p>Already have an account? <router-link :to="{ name: 'Login' }">Login</router-link></p>
      </v-row>
  </v-container>
</template>

<script>

import axios from 'axios'

export default {
  name: 'Login',
  data() {
    return {
      email: "",
      name: "",
      password: "",
      errMsg: ""
    };
  },

  methods: {
    login () {
      axios.post(`/user/login`, { email: this.email, password: this.password })
        .then(response => window.localStorage.setItem("jwt", response.data.access_token))
        .then(() => this.$router.push('/'))
        .catch(error => {
          this.errMsg= error
        })
      console.log(window.localStorage.getItem("jwt"))
    },
    register () {
      axios.post(`/user/register`, { email: this.email, name:this.name, password: this.password })
        .then(() => this.login ())
        .catch(error => {
          this.errMsg = error
        })
    }
  },

  created(){
      document.title = "Quora Clone - Register"
      this.getQuestions()
    }
}
</script>