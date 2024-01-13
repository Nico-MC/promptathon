<template>
  <div class="accordion space-y-4">
    <div
      v-for="(details, goaeNumber) in apiData"
      :key="goaeNumber"
      class="mb-2"
    >
      <button
        @click="toggle(goaeNumber)"
        class="accordion-header bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 w-full text-left rounded"
      >
        GOÄ Nummer {{ goaeNumber }}
      </button>

      <div
        v-if="openPanels.includes(goaeNumber)"
        class="accordion-content mt-2 p-4 border border-blue-300 rounded bg-white"
      >
        <div v-for="(value, prefix) in details" :key="prefix" class="mb-4">
          <button
            @click="togglePrefix(goaeNumber, prefix)"
            class="font-semibold text-lg mb-2 text-blue-600 hover:text-blue-800"
          >
            {{ prefix }}
          </button>

          <div v-if="openPrefixes[goaeNumber]?.includes(prefix)">
            <div class="pl-4">
              <p class="text-sm font-semibold">Kategorien:</p>
              <ul class="list-disc pl-5 mb-4">
                <li
                  v-for="kategorie in value.kategorien"
                  :key="kategorie"
                  class="text-gray-600"
                >
                  {{ kategorie }}
                </li>
              </ul>

              <p class="text-sm font-semibold">Kommentare:</p>
              <ul class="list-disc pl-5">
                <li
                  v-for="comment in value.kommentare"
                  :key="comment.id"
                  class="mb-1"
                >
                  <p class="font-semibold">{{ comment.title }}</p>
                  <p class="text-gray-600">{{ comment.text }}</p>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      openPanels: [],
      openPrefixes: {}, // Hält den Zustand der geöffneten Prefixe
    };
  },
  computed: {
    apiData() {
      return this.$store.state.apiData;
    },
  },
  methods: {
    toggle(goaeNumber) {
      const index = this.openPanels.indexOf(goaeNumber);
      if (index > -1) {
        this.openPanels.splice(index, 1);
      } else {
        this.openPanels.push(goaeNumber);
      }
    },
    togglePrefix(goaeNumber, prefix) {
      if (!this.openPrefixes[goaeNumber]) {
        this.openPrefixes[goaeNumber] = [];
      }
      const index = this.openPrefixes[goaeNumber].indexOf(prefix);
      if (index > -1) {
        this.openPrefixes[goaeNumber].splice(index, 1);
      } else {
        this.openPrefixes[goaeNumber].push(prefix);
      }
    },
  },
};
</script>
