<template>
  Counter: {{ counter }}
  <button @click="increase">Increase</button>
  <button @click="decrement">Decrement</button>
</template>

<script setup lang="ts">
import {ref} from 'vue';

let counter = ref(0)

function increase() {
  counter.value++
}

function decrement() {
  counter.value--
}
</script>

<style>
#app {
  margin: 20px;
}
</style>
