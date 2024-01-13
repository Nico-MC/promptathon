<template>
  <div class="container">
    <Goae></Goae>
    <Prompts></Prompts>
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
import Prompts from "./components/PromptsComponent.vue";
import Goae from "./components/GoaeComponent.vue";
import { mapState, mapActions } from "vuex";
import ApiOutput from "./components/ApiOutput.vue";

export default {
  name: "PromptathonApp",
  components: {
    Goae,
    Prompts,
    ApiOutput,
  },
  computed: {
    ...mapState(["apiData", "isLoading"]),
  },
  methods: {
    ...mapActions(["fetchApiData"]),
    async submitToFlask() {
      await this.fetchApiData();
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
    max-width: 500px;
    width: 100%;
  }
}
</style>
