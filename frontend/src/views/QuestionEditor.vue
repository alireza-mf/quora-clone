<template>
  <v-container>
    <v-flex>
      <v-card v-if="errMsg" flat class="mx-auto mt-6 mb-n3 pa-1 text-h6 text-center" width="880" color="red">
      {{errMsg}}
      </v-card>
      <v-card class="mx-auto mt-5 pa-9" flat width="880" color="indigo" dark>
        <v-card-title class="mt-n7">Ask a new Question
        </v-card-title>
        <v-form>
          <v-text-field outlined shaped :rules="[val=>!!val||'Required']" v-model="title" label="Your Question Title">
          </v-text-field>
          <v-textarea
              outlined
              v-model="content"
              label="Your Question Description..."
              :rules="[val=>!!val||'Required']"
          ></v-textarea>
        <v-card-actions>
          <v-btn primary large block light @click="onSubmit">Submit Answer</v-btn>
        </v-card-actions>
        </v-form>
      </v-card>
    </v-flex>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'QuestionEditor',

  data() {
    return {
      title:"",
      content: "",
      errMsg: ""
    };
  },

  methods: {
    onSubmit () {
      const token = window.localStorage.getItem("jwt");
      axios.post(`/api/questions`, { title: this.title, content: this.content }, { headers: { Authorization: `Bearer ${token}` } })
        .then(() => this.$router.push({
              name: "Home" }))
        .catch(error => {
          this.errMsg = error;
        })
    },
  },

  created(){
      document.title = "Quora Clone - Ask a Question"
    }
}
</script>