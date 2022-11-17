
<template>
  <v-container>
    <div class="bg-orange-accent-3">
      <label class="font-weight-black">
        HackerNews |
      </label>
      <label>
        welcome | new | threads | past | comments | ask | show | jobs | submit 
      </label>
      <label class="float-right">
        login
      </label>
    </div>
    <br>
    <v-row>
      <v-col>
        <v-text-field type="text" label="Name"
        v-model="input_name"
        hint="Enter your name"
        counter="10"
        :rules="rules2"
        required/>
      </v-col>
      <v-col cols="12" sm="6">
        <v-text-field type="text" label="Title"
        v-model="input_title"
         :rules="rules1"
         hint="Enter a title"
         counter="25"
         required>
      </v-text-field>
      </v-col>
      <v-col>
        <v-btn color="orange" @click="addpost()">Submit</v-btn>
      </v-col>
    </v-row>


    <ol class="mx-16" :start="a">
      <li v-for="new_ in sortedArray.slice(a, a + 10)" :key="new_.id" v-show="new_.a">
        <v-row>
          <v-col sm="1" cols="1" class="arrow">
            <v-icon icon="mdi-arrow-up" small @click="upvote(new_.id) "></v-icon>
          </v-col>
          <v-col>
            <div class="title"><a :href="new_.link"  class="link">{{ new_.title }}</a></div>
            <div>{{ new_.votes }} votes posted by {{ new_.name }} | {{ new_.hour }} hours ago | <button @click="new_.a = false">hide</button> | {{  new_.comment }} comments 
            <button class="downv" v-if="new_.controler === true" @click="downvote(new_.id)">| unvote</button></div>
          </v-col>
        </v-row>
      </li>
    </ol>



    <div>
      <v-btn v-for="(pagenum, index) in 10" :key="index" color="black" @click="changepage(pagenum)" class="buttons"> {{ pagenum }} </v-btn>
    </div>
  </v-container>
</template>

<script>
  export default {
    data () {
      return {
        rules1: [v => v.length <= 25 || 'Max 25 characters' , v => v.length > 0 || "No empty"] ,
        rules2: [v => v.length <= 10 || 'Max 10 characters' , v => v.length > 0 || "No empty"] ,
      }
    },
  }
</script>


<script setup>
  import hackernews from './hackernews.json'
  import {ref, computed, watch} from "vue"

  const names = [
    "AquaticChosen",
    "Bobri",
    "Briefingka",
    "Callya",
    "ChampionSuave",
    "Chiquitareiv",
    "Crojacklo",
    "Digiops",
    "Drudgware",
    "Enjoy",
    "Farerre",
    "Firellemc",
    "Freerjoy",
    "GotWicked",
    "Hotsion",
    "KaptainMajor",
    "Loglenn",
    "Partsmar",
    "Proceeded",
    "Raideteau",
    "Reveredit",
    "Screwed",
    "Storminie",
    "Strippery",
    "Takintr",
    "Taleni",
    "Targeteria",
    "Tearch",
    "Topicsva",
    "Turnquert",
  ]
  
  const votes = ref(null)
  const name = ref(null)
  const hour = ref(null)
  const comment = ref(null)
  const link = ref(null)
  const controler = ref(null)
  

  const hnews  = ref(null)

  async function fetchpost(){
    const response = await fetch('https://jsonplaceholder.typicode.com/posts')
    hnews.value = await response.json()

    hnews.value.forEach(element => {

      element.a = true;
      element.controler = false;
      element.link = hackernews[element.id]
      element.name = names[Math.ceil(Math.random() * (30))]
      element.votes = Math.ceil(Math.random() * (100)) + 1
      element.hour = Math.ceil(Math.random() * (10)) + 1
      element.comment = Math.ceil(Math.random() * (200)) + 1
    });
    page.value = sortedArray.value.slice(0, 10);
    // console.log(sortedArray.value);
  }
  
  fetchpost()
  
  const sortedArray = computed(() => [...hnews.value].sort((a, b) => b.votes - a.votes))

  let a = ref(1)
  const k = ref(1)
  let x = 1
  let page = ref(null)
  function changepage(i){
    k.value = i
    x = parseInt(k.value)
    a.value = (i - 1) * 10 + 1
  }


  function upvote(newId){
    console.log(newId)
    if(hnews.value[newId-1].controler == 1){
      return 0
    }
    else{
      hnews.value[newId-1].controler = true
      hnews.value[newId-1].votes = hnews.value[newId-1].votes + 1
      
    } 

  }

  function downvote(newId){
    hnews.value[newId-1].controler = false
    hnews.value[newId-1].votes = hnews.value[newId-1].votes - 1
  }


  const input_title = ref("")
  const input_name = ref("")

  function addpost() {
    let   new_hackernew = {userId: 1, id: 1, title: input_title.value, body: 'not imp', controler: 0, votes: 0, comment: 0, hours: 0, name: input_name.value, a: true }
    sortedArray.value.push(new_hackernew)
  }

</script>

<style>
  .title{
    font-weight: bold;
  }
  .link{
    color: black;
    text-decoration: none;
  }
  .link:active{
    text-decoration: none;
    color: black;
  }
  .downv{
    border: none;
  }
  .arrow{
    padding-right: 0px;
  }
  .hidetime{
    display: none;
  }
</style>