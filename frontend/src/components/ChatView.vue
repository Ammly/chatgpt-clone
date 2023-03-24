<template>
  <div class="" :class="{ 'bg-gray-700 text-white': isDarkMode }">
    <div class="container mx-auto flex flex-col h-screen">
    <div class="flex-1 overflow-y-auto px-4 py-2">
      <div v-for="(response, index) in responses" :key="index" class="flex flex-col">
        <div class="flex justify-end m-2">
          <div class="bg-gray-200 p-2 rounded-md shadow-sm max-w-full flex-grow" :class="{ 'bg-gray-600 text-white': isDarkMode }" v-html="response.input"></div>
        </div>
        <div class="flex justify-start m-2">
          <div class="bg-blue-500 p-2 rounded-md shadow-sm max-w-full flex-grow" :class="{ 'bg-blue-500 text-white': isDarkMode }" v-html="response.response"></div>
        </div>
      </div>
    </div>
    <form class="p-4" @submit.prevent="handleSubmit">
      <div class="flex space-x-2">
        <textarea
          class="flex-1 border border-gray-300 p-2 rounded-md shadow-sm"
          v-model="input"
          placeholder="Type something..."
          required
          @keydown.enter.prevent="shiftEnter ? null : handleSubmit()"
          @keydown.enter.shift="shiftEnter = true"
          @keydown.enter.shift.prevent="input += '\n'"
          @keyup.enter.shift="shiftEnter = false"
          :disabled="isLoading"
          :class="{ 'bg-gray-700 text-white': isDarkMode }"
        ></textarea>
        <button
          type="submit"
          class="px-4 py-2 text-white bg-blue-500 rounded-md shadow-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          :disabled="isLoading"
          :class="{ 'bg-gray-700': isDarkMode }"
        >
          <span v-if="!isLoading">Send</span>
          <span v-else>
            <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm12 0a8 8 0 100-16 8 8 0 000 16z"></path>
            </svg>
          </span>
        </button>
        <button
          type="button"
          class="px-4 py-2 rounded-md shadow-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-400"
          @click="toggleDarkMode"
        >
          {{ isDarkMode ? 'Light' : 'Dark' }} Mode
        </button>
      </div>
    </form>
  </div>
  </div>
</template>


<script>
import axios from 'axios';
import * as marked from 'marked'; // import marked library to parse markdown to HTML

export default {
  data() {
    return {
      input: '',
      responses: [],
      isLoading: false, // Add isLoading property
      isDarkMode: false, // Add isDarkMode property
    };
  },
  methods: {
    async handleSubmit() {
      this.isLoading = true; // Set isLoading to true
      const { data } = await axios.post('http://127.0.0.1:5000/api/chat', { input: this.input });
      this.responses.push({ input: this.input, response: marked.parse(data.message) }); // use marked to parse markdown to HTML
      this.input = '';
      this.isLoading = false; // Set isLoading back to false
    },
    toggleDarkMode(){
      this.isDarkMode = !this.isDarkMode
    }
  },
};
</script>
