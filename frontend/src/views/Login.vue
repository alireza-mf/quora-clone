<template>
  <v-container>
      <v-flex>
        <v-card v-if="errMsg" flat class="ma-auto my-2 pa-1 text-h6 text-center" width="480" color="red">
          {{errMsg}}
        </v-card>
        <v-card class="ma-auto" color="indigo" width="480px" height="460px">
        <v-container style="position: relative;top: 6%;" class="ma-auto">
          <v-card class="px-4" flat elevation="6">
            <v-card-title primary-title>
              <h4>Login</h4>
            </v-card-title>
            <v-form>
            <v-text-field prepend-icon="mdi-email" outlined v-model="email" :rules="[val=>!!val||'Required']" label="Email" type="email"></v-text-field>
            <v-text-field prepend-icon="mdi-lock" outlined v-model="password" :rules="[val=>!!val||'Required']" label="Password" type="password"></v-text-field>
            <v-card-actions>
              <v-row>
                <v-btn class="mb-5" color="indigo" large block dark @click="login">Login</v-btn>
                <v-btn class="mb-5" color="#4285f4" large block dark>
                  <v-icon>mdi-google</v-icon>{{"\xa0\xa0"}}Login via Google
                </v-btn>
              </v-row>
            </v-card-actions>
            </v-form>
          </v-card>
        </v-container>
        </v-card>
      </v-flex>
      <v-row justify="center" class="ma-3">
        <p>Don't have an account? <router-link :to="{ name: 'Register' }">Register Now</router-link></p>
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
          this.errMsg = error;
          window.localStorage.removeItem("jwt")
        })
    }
  },
  created(){
      document.title = "Quora Clone - Login"
      this.getQuestions()
    }
}
</script>
