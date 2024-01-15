<template>
  <div class="p-4">
    <div class="flex items-center space-x-2 mb-4">
      <input
        type="number"
        v-model.number="newNumber"
        @keyup.enter="addNumber"
        class="border border-gray-300 p-2 rounded"
        placeholder="GOÄ-Ziffern"
      />
      <button
        @click="addNumber"
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      >
        Hinzufügen
      </button>
    </div>

    <ul class="list-disc pl-5">
      <li v-for="(number, index) in numbers" :key="index" class="mb-2">
        <span class="mr-2">{{ number }}</span>
        <button
          @click="removeNumber(index)"
          class="bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-3 rounded text-xs"
        >
          Entfernen
        </button>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      inputNumber: "",
      newNumber: "",
    };
  },
  computed: {
    numbers() {
      return this.$store.state.numbers;
    },
  },
  methods: {
    addNumber() {
      if (this.newNumber !== "") {
        this.$store.commit("addNumber", this.newNumber);
        this.newNumber = "";
      }
    },
    removeNumber(index) {
      this.$store.commit("removeNumber", index);
    },
  },
};
</script>
