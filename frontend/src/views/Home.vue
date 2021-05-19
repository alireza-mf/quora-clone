<template>
  <v-container>
    <QuestionsList msg="Welcome to Your Vue.js App"/>
  </v-container>
</template>

<script>
// @ is an alias to /src
import QuestionsList from '@/components/QuestionsList.vue'

export default {
  name: 'Home',
  components: {
    QuestionsList
  }
}
</script>
