<template>
  <div class="container">
    <div class="flex items-center justify-center my-4">
      <span class="mr-3 text-blue-700">Completions</span>
      <div
        @click="showAssistant = !showAssistant"
        class="relative inline-block w-12 mr-2 align-middle select-none transition duration-200 ease-in"
      >
        <input
          type="checkbox"
          v-model="showAssistant"
          class="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer"
        />
        <label
          for="toggle"
          class="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"
        ></label>
      </div>
      <span class="text-blue-700">Assistant</span>
    </div>
    <Goae></Goae>
    <Assistant v-if="showAssistant"></Assistant>
    <Completions v-else></Completions>
    <button
      @click="submitToFlask"
      class="my-2 bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded"
    >
      Prompt!
    </button>
    <div class="api-output">
      <div v-if="apiData">
        <ApiOutput :data="apiData" />
      </div>
      <div v-else-if="isLoading">
        <p>Kategorien werden erstellt...</p>
      </div>
    </div>
  </div>
</template>

<script>
import Completions from "./components/CompletionsComponent.vue";
import Assistant from "./components/AssistantComponent.vue";
import Goae from "./components/GoaeComponent.vue";
import { mapState, mapActions } from "vuex";
import ApiOutput from "./components/ApiOutput.vue";

export default {
  name: "PromptathonApp",
  components: {
    Goae,
    Completions,
    Assistant,
    ApiOutput,
  },
  data() {
    return {
      showAssistant: true,
    };
  },
  computed: {
    ...mapState(["apiData", "isLoading"]),
  },
  methods: {
    ...mapActions(["fetchApiData"]),
    async submitToFlask() {
      let url = this.showAssistant
        ? "getCategoriesForGoaeNumberFromAssistant"
        : "getCategoriesForGoaeNumber";
      await this.fetchApiData(url);
    },
  },
};
</script>

<style lang="scss">
.container {
  max-width: 640px;
  margin: 30px auto;
  display: flex;
  align-items: center;
  flex-direction: column;
  .prompts {
    max-width: 560px;
    width: 100%;
  }
  .toggle-checkbox:checked {
    right: 0;
    border-color: #3182ce; /* Blau, entsprechend der Tailwind-Klasse border-blue-500 */
  }

  .toggle-checkbox:checked + .toggle-label {
    background-color: #3182ce; /* Blau, entsprechend der Tailwind-Klasse bg-blue-500 */
  }

  .toggle-label {
    display: block;
    overflow: hidden;
    height: 1.5rem; /* 6 Einheiten in Tailwind */
    border-radius: 9999px; /* Vollständig gerundet in Tailwind */
    background-color: #d1d5db; /* Grau, entsprechend der Tailwind-Klasse bg-gray-300 */
  }
}
</style>
