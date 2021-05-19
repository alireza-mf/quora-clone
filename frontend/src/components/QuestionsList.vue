<template>
  <v-container>
    <v-skeleton-loader v-show="loadingQuestions" max-width="750" elevation="5" class="mb-7" type="article"></v-skeleton-loader>
    <v-skeleton-loader v-show="loadingQuestions" max-width="750" elevation="5" class="mb-7" type="article"></v-skeleton-loader>
    <v-row>
      <v-col v-for="q in questions" :key="q.id">
        <v-card width="750" elevation="7" color="indigo" dark>
          <router-link style="text-decoration: none; color: white" :to="{ name: 'Question', params: { slug: q.slug } }">
          <v-card-title class="mb-n6 headline font-weight-bold">{{q.title}}
            <v-btn text class="ml-auto">
              <v-icon>mdi-thumb-up</v-icon>
            </v-btn>
           </v-card-title></router-link>
          <v-card-subtitle>{{ q.created_at | moment("dddd, Do MMMM YYYY") }} ({{ q.created_at | moment("from") }})
          </v-card-subtitle>
          <v-divider></v-divider>
          <v-card-text class="text-subtitle-1" style="color: white" v-text="q.content"></v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-list-item-avatar color="grey darken-3">
              <v-img
                alt=""
                src="https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairShortCurly&accessoriesType=Prescription02&hairColor=Black&facialHairType=Blank&clotheType=Hoodie&clotheColor=White&eyeType=Default&eyebrowType=DefaultNatural&mouthType=Default&skinColor=Light"
              ></v-img>
            </v-list-item-avatar>
            <v-list-item-content v-text="q.author"></v-list-item-content>
            <v-btn class="mr-2" text :to="{ name: 'Question', params: { slug: q.slug } }">{{q.answers.length}} Answers{{"\xa0"}}
            <v-icon class="mr-3">mdi-message-text</v-icon>
            </v-btn>
          </v-card-actions>
          </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'

  export default {
    name: 'QuestionsList',

    data: () => ({
      questions: [],
      loadingQuestions: false,
    }),

    methods: {
      async getQuestions() {
        axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';
        // make a GET Request to the questions list endpoint and populate the questions array
        this.loadingQuestions = true;
        axios.get("/api/questions")
        .then(res => this.questions = res.data)
        .then(() => this.loadingQuestions = false)
      }
    },

    created(){
      document.title = "Quora Clone"
      this.getQuestions()
    }
  }
</script>
