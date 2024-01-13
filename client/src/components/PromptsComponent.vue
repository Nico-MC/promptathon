<template>
  <div class="prompts">
    <label
      for="promptCount"
      class="block mb-2 text-sm font-medium text-gray-900"
      >Anzahl der Prompts:</label
    >
    <select
      id="promptCount"
      v-model="promptCount"
      @change="updatePromptCount"
      class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
    >
      <option value="1">1</option>
      <option value="2">2</option>
      <option value="3">3</option>
    </select>

    <div v-for="n in parseInt(promptCount)" :key="n" class="mt-4">
      <textarea
        v-model="prompts[n - 1]"
        :placeholder="'Prompt ' + n"
        class="textarea-resize bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 max-w-[500px]"
        rows="2"
        @input="resizeTextArea($event)"
      ></textarea>
    </div>
  </div>
</template>

<script>
import { mapState, mapMutations } from "vuex";

export default {
  data() {
    return {
      promptCount: "1",
      prompts: ["", "", ""],
    };
  },
  computed: {
    ...mapState(["promptCount", "prompts"]),
  },
  methods: {
    resizeTextArea(event) {
      event.target.style.height = "auto";
      event.target.style.height = event.target.scrollHeight + "px";
    },
    ...mapMutations(["setPromptCount", "setPrompt"]),
    updatePromptCount() {
      this.setPromptCount(this.promptCount);
    },
    updatePrompt(index, value) {
      this.setPrompt({ index, value });
    },
  },
};
</script>
