<template>
  <div class="prompts">
    <label
      for="promptCount"
      class="block mb-2 text-sm font-medium text-gray-900"
      >Anzahl der Prompts:</label
    >
    <select
      id="promptCount"
      v-model="localPromptCount"
      @change="updatePromptCount"
      class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
    >
      <option
        v-for="(prompt, index) in prompts2"
        :key="index"
        :value="index + 1"
      >
        {{ index + 1 }}
      </option>
    </select>

    <div v-for="n in parseInt(promptCount2)" :key="n" class="mt-4">
      <label
        :for="'prompt' + n"
        class="block text-sm font-medium text-gray-900"
      >
        {{ promptDescription2[n - 1] }}
      </label>
      <p class="mb-3 text-xs text-gray-500" v-html="promptHints2[n - 1]"></p>
      <!-- Vergrößerter Abstand -->
      <textarea
        :value="prompts2[n - 1]"
        @input="
          updatePrompt(n - 1, $event.target.value);
          resizeTextArea($event);
        "
        :placeholder="'Prompt ' + n"
        class="textarea-resize bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 max-w-[560px]"
        rows="2"
      ></textarea>
    </div>
  </div>
</template>

<script>
import { mapState, mapMutations } from "vuex";

export default {
  data() {
    return {
      localPromptCount: "",
    };
  },
  computed: {
    ...mapState([
      "promptCount2",
      "prompts2",
      "promptDescription2",
      "promptHints2",
    ]),
  },
  methods: {
    ...mapMutations(["setPromptCount2", "setPrompt2"]),
    updatePromptCount() {
      this.setPromptCount2(this.localPromptCount);
    },
    updatePrompt(index, value) {
      this.setPrompt2({ index, value });
    },
    resizeTextArea(event) {
      event.target.style.height = "auto";
      event.target.style.height = event.target.scrollHeight + "px";
    },
    resizeAllTextAreas() {
      this.$nextTick(() => {
        const textAreas = document.querySelectorAll(".textarea-resize");
        textAreas.forEach((textarea) => {
          textarea.style.height = "auto";
          textarea.style.height = textarea.scrollHeight + "px";
        });
      });
    },
  },
  watch: {
    promptCount2(newValue) {
      this.localPromptCount = newValue;
    },
    prompts2() {
      this.resizeAllTextAreas();
    },
  },
  mounted() {
    this.resizeAllTextAreas();
    this.localPromptCount = this.promptCount2;
  },
};
</script>
