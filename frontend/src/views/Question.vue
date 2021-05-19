<template>
  <v-container>
    <v-skeleton-loader v-show="loadingQuestion" max-width="750" elevation="5" class="mb-7" type="article"></v-skeleton-loader>
    <v-skeleton-loader v-show="loadingQuestion" max-width="750" elevation="5" class="mb-7" type="article"></v-skeleton-loader>
    <v-row>
      <v-col>
        <v-card width="750" elevation="7" color="indigo" dark>
          <v-card-title class="headline font-weight-bold">{{question.title}}
            <v-btn class="ml-auto" icon>
              <v-icon>mdi-thumb-up</v-icon>
            </v-btn>
          </v-card-title>
          <v-card-subtitle>{{ question.created_at | moment("dddd, Do MMMM YYYY") }} ({{ question.created_at | moment("from") }})</v-card-subtitle>
          <v-divider class="mx-4"></v-divider>
          <v-card-text class="text-subtitle-1" style="color: white" v-text="question.content"></v-card-text>
          <v-divider class="mx-4"></v-divider>
          <v-card-actions>
            <v-list-item-avatar color="grey darken-3">
              <v-img
                alt=""
                src="https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairShortCurly&accessoriesType=Prescription02&hairColor=Black&facialHairType=Blank&clotheType=Hoodie&clotheColor=White&eyeType=Default&eyebrowType=DefaultNatural&mouthType=Default&skinColor=Light"
              ></v-img>
            </v-list-item-avatar>
            <v-list-item-content v-text="question.author"></v-list-item-content>
            <v-btn class="mr-2" text rounded disabled>{{question.answers.length}} Answers{{"\xa0"}}
            <v-icon class="mr-3">mdi-message-text</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>

        <v-card v-for="a in question.answers" :key="a.id" class="mt-5" flat width="880" color="green darken-3" dark>
          <v-card-text class="pa-6 text-subtitle-1" style="color: white" v-text="a.content"></v-card-text>
          <v-divider class="mx-4 mb-n2"></v-divider>
          <v-card-actions>
            <v-list-item-avatar color="grey darken-3">
              <v-img
                alt=""
                src="https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairShortCurly&accessoriesType=Prescription02&hairColor=Black&facialHairType=Blank&clotheType=Hoodie&clotheColor=White&eyeType=Default&eyebrowType=DefaultNatural&mouthType=Default&skinColor=Light"
              ></v-img>
            </v-list-item-avatar>
            <v-card-subtitle class="mx-n4" v-text="a.author"></v-card-subtitle>
            <v-spacer></v-spacer>
            <v-card-subtitle>
            {{ a.created_at | moment("dddd, Do MMMM YYYY") }} ({{ a.created_at | moment("from") }})
            </v-card-subtitle>
          </v-card-actions>
        </v-card>
        <AnswerEditor v-if="isAuthenticated"
        :slug="slug"
        />
      </v-col>
    </v-row>
    <v-btn v-if="!isAuthenticated" large block dark class="mb-8" color="green darken-3" :to="{ name: 'Login'}">Login to Answer</v-btn>
  </v-container>
</template>

<script>
import axios from 'axios'
import { isValidJwt } from '@/utils/jwtValidator'
import AnswerEditor from "@/components/AnswerEditor.vue";

  export default {
    name: 'Question',
    props: {
      slug: {
        type: String,
        required: true
      }
    },
    components: {
      AnswerEditor
    },

    data: () => ({
      question: {},
      loadingQuestion: false,
      isAuthenticated: false
    }),

    methods: {
      getQuestions() {
        this.loadingQuestion = true;
        axios.get(`/api/questions/${this.slug}`)
        .then(res => this.question = res.data)
        .then(() => this.loadingQuestion = false)
      },

      isAuthenticate () {
        const token = window.localStorage.getItem("jwt");
        console.log(token)
        this.isAuthenticated = isValidJwt(token)
        return this.isAuthenticated
      },
    },

    created(){
      document.title = "Quora Clone - " + this.question.title
      this.getQuestions()
      this.isAuthenticate()
    }
  }
</script>
