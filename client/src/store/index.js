import { createStore } from "vuex";

export default createStore({
  state: {
    promptCount: "1",
    prompts: ["", "", ""],
    numbers: [],
    apiData: null,
  },
  mutations: {
    setPromptCount(state, count) {
      state.promptCount = count;
    },
    setPrompt(state, { index, value }) {
      state.prompts[index] = value;
    },
    addNumber(state, number) {
      state.numbers.push(number);
    },
    removeNumber(state, index) {
      state.numbers.splice(index, 1);
    },
    setApiData(state, newData) {
      state.apiData = newData;
    },
  },
  actions: {
    async fetchApiData({ commit, state }) {
      try {
        const dataToSend = { ...state };
        delete dataToSend.apiData;

        const response = await fetch(
          "http://localhost:5000/getCategoriesForGoaeNumber",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(dataToSend),
          }
        );

        if (!response.ok) {
          throw new Error("Fehler beim Abrufen der API-Daten");
        }
        const data = await response.json();
        commit("setApiData", data);
      } catch (error) {
        console.error("Fehler:", error);
      }
    },
  },
});
