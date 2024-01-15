import { createStore } from "vuex";

export default createStore({
  state: {
    promptCount: "1",
    prompts: [
      "Bitte gib mir 2 1-Wort Kategorien, die für alle der folgenden Kommentare passend sind und ärztliche Fachbegriffe sind.\n\n$comments\n\n" +
        'Die 2 am besten passenden Kategorien sind: ["',
      "",
      "",
    ],
    promptDescription: [
      // title over prompt textfield
      "Prefix-Prompt",
      "Kommentar-Prompt",
      "3. Testprompt",
    ],
    promptHints: [
      "Die - in einem Prefix befindlichen Kommentare - werden als ein <strong>gemeinsamer Prompt</strong> abgeschickt.",
      "Jedes Kommentar, wird in einem <strong>einzelnen</strong>, <strong>seperaten Prompt</strong> abgeschickt.",
      "",
    ],
    numbers: [],
    apiData: null,
    isLoading: false,
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
    setLoading(state, isLoading) {
      state.isLoading = isLoading;
    },
  },
  actions: {
    async fetchApiData({ commit, state }) {
      try {
        commit("setLoading", true);
        commit("setApiData", null);
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
        commit("setLoading", false);
      } catch (error) {
        commit("setLoading", false);
        console.error("Fehler:", error);
      }
    },
  },
});
