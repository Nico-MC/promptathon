import { createStore } from "vuex";

export default createStore({
  state: {
    promptCount: "1",
    prompts: [
      "Bitte gib mir 3 1-Wort Kategorien, die für den folgenden Kommentar passend sind und ärztliche Fachbegriffe sind.\n\n$comments\n\n" +
        'Die 3 am besten passenden Kategorien sind: ["',
      "Bitte gib mir 2 1-Wort Kategorien, die für alle der folgenden Kommentare passend sind und ärztliche Fachbegriffe sind.\n\n$comments\n\n" +
        'Die 2 am besten passenden Kategorien sind: ["',
    ],
    promptDescription: [
      // title over prompt textfield
      "Kommentar-Prompt",
      "Prefix-Prompt",
    ],
    promptHints: [
      "Jedes Kommentar, wird in einem <strong>einzelnen</strong> Prompt abgeschickt.",
      "Die - in einem Prefix befindlichen Kommentare - werden als ein <strong>gemeinsamer Prompt</strong> abgeschickt.",
    ],
    // schnell für Assistant copy paste
    promptCount2: "1",
    prompts2: [
      "You are an AI assistant that helps people find categories for a given text. Categories that have already been used for other comments and are therefore ignored = ['Abrechnung', 'GOÄ', 'Behandlungsfall', 'Beratungsleistung']",
    ],
    promptDescription2: [
      // title over prompt textfield
      "Kommentar-Prompt",
    ],
    promptHints2: [
      "Jedes Kommentar, wird in einem <strong>einzelnen</strong> Prompt abgeschickt. Im JSON <i>group_comments_after_prefix</i> werden alle <strong>prefered_categories</strong> als Beispiele an den Prompt angehängt.",
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
    setPromptCount2(state, count) {
      state.promptCount2 = count;
    },
    setPrompt2(state, { index, value }) {
      state.prompts2[index] = value;
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
    async fetchApiData({ commit, state }, url) {
      try {
        commit("setLoading", true);
        commit("setApiData", null);
        const dataToSend = { ...state };
        delete dataToSend.apiData;

        const response = await fetch("http://localhost:5000/" + url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(dataToSend),
        });

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
