<template>
<v-flex>
  <v-card v-if="errMsg" flat class="mt-6 mb-n3 pa-1 text-h6 text-center" width="880" color="red">
    {{errMsg}}
  </v-card>
  <v-card class="mt-5 pa-9" flat width="880" color="green darken-4" dark>
    <v-form>
      <v-textarea
            outlined
            :rules="[val=>!!val||'Required']"
            v-model="content"
            label="Your Answer"
      ></v-textarea>
      <v-card-actions>
        <v-btn primary large block light @click="onSubmit">Submit Answer</v-btn>
      </v-card-actions>
    </v-form>
  </v-card>
</v-flex>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AnswerEditor',
  props: {
      slug: {
        type: String,
        required: true
      }
  },

  data() {
    return {
      content: "",
      errMsg: ""
    };
  },

  methods: {
    onSubmit () {
      const token = window.localStorage.getItem("jwt");
      axios.post(`/api/questions/${this.slug}/answer`, { content: this.content }, { headers: { Authorization: `Bearer ${token}` } })
        .then(() => this.$router.push({
                      name: "Question",
                      params: { slug: this.slug }}))
        .catch(error => {
          this.errMsg = error;
        })
    },
  },
}
</script>