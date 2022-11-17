<template>
  <v-container>
    <v-row>
      <v-col cols="12" sm="6" lg="3">
        <v-text-field type="text" label="Todo" v-model="input" />
      </v-col>
      <v-col cols="12" sm="6" lg="3">
        <v-btn @click="addTodo">Add</v-btn>
      </v-col>
    </v-row>
    <v-list>
      <v-list-item v-for="todo in todos" :key="todo.id">
        {{ todo.title }}

        <template v-slot:append>
          <v-checkbox v-model="todo.completed" />
        </template>

      </v-list-item>
    </v-list>
  </v-container>
</template>

<script setup lang="ts">
import {ref} from "vue"

type Todo = {
  userId: number
  id: number
  title: string
  completed: boolean
}

const input = ref("")
const todos = ref<Todo[]>([])

function addTodo() {
  const newTodo: Todo = {
    userId: 0,
    id: todos.value.length + 1,
    title: input.value,
    completed: false
  }
  todos.value.push(newTodo)
}

async function fetchTodos() {
  const response = await fetch('https://jsonplaceholder.typicode.com/todos')
  todos.value = await response.json()
}

fetchTodos()

</script>
