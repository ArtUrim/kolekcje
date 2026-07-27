<template>
  <div>
    <!-- Wybrane chipy -->
    <div v-if="selectedValueLocal.length" class="d-flex flex-wrap gap-1 mb-2">
      <v-chip
        v-for="val in selectedValueLocal"
        :key="val"
        closable
        @click:close="removeValue(val)"
      >
        {{ val }}
      </v-chip>
    </div>

    <!-- Pole tekstowe -->
    <v-text-field
      ref="inputField"
      v-model="inputText"
      :label="label"
      :placeholder="placeholder"
      :loading="loading"
      autocomplete="off"
      @input="onInput"
      @keydown.enter.prevent="onEnter"
      @keydown.esc="closeMenu"
      @focus="openMenu"
      @blur="onBlur"
    />

    <!-- Dropdown -->
    <v-menu
      v-model="menuOpen"
      :activator="$refs.inputField"
      :close-on-content-click="false"
      :open-on-click="false"
      max-height="300"
      width="auto"
    >
      <v-list density="compact">
        <template v-if="filteredItems.length">
          <v-list-item
            v-for="item in filteredItems"
            :key="item.id"
            :title="item.title"
            :disabled="isSelected(item.value)"
            @mousedown.prevent="selectItem(item)"
          />
        </template>

        <template v-else-if="inputText.trim()">
          <v-list-item
            :title="`Dodaj: &quot;${inputText.trim()}&quot;`"
            prepend-icon="mdi-plus"
            @mousedown.prevent="addNewValue"
          />
        </template>

        <template v-else>
          <v-list-item title="Zacznij pisać..." disabled />
        </template>
      </v-list>
    </v-menu>
  </div>
</template>

<script>
export default {
  props: {
    modelValue: {
      type: Array,
      default: () => []
    },
    label: {
      type: String,
      required: true
    },
    placeholder: {
      type: String,
      required: true
    },
    apiEndpoint: {
      type: String,
      required: true
    }
  },

  emits: ['update:modelValue'],

  data() {
    return {
      // Inicjalizacja z props — BEZ watchera który by to nadpisywał
      selectedValueLocal: Array.isArray(this.modelValue) ? [...this.modelValue] : [],
      items: [],
      loading: false,
      inputText: '',
      menuOpen: false
    }
  },

  computed: {
    filteredItems() {
      const query = this.normalize(this.inputText)
      if (!query) return this.items
      return this.items.filter(
        item =>
          this.normalize(item.title).includes(query) ||
          this.normalize(item.value).includes(query)
      )
    }
  },

  async mounted() {
    await this.fetchGenres()
  },

  methods: {
    async fetchGenres() {
      try {
        this.loading = true
        const response = await fetch(this.apiEndpoint)
        if (!response.ok) throw new Error(`HTTP ${response.status}`)
        this.items = await response.json()
      } catch (err) {
        console.error('Error fetching genres:', err)
      } finally {
        this.loading = false
      }
    },

    normalize(val) {
      return String(val || '').trim().toLocaleLowerCase()
    },

    isSelected(value) {
      return this.selectedValueLocal.some(
        v => this.normalize(v) === this.normalize(value)
      )
    },

    onInput() {
      this.menuOpen = true
    },

    openMenu() {
      this.menuOpen = true
    },

    closeMenu() {
      this.menuOpen = false
    },

    onBlur() {
      setTimeout(() => {
        this.menuOpen = false
      }, 150)
    },

    onEnter() {
      // Dokładne dopasowanie — wybierz z listy
      const exact = this.filteredItems.find(
        item => this.normalize(item.value) === this.normalize(this.inputText)
      )
      if (exact) {
        this.selectItem(exact)
        return
      }

      // Jedno dopasowanie — wybierz je
      if (this.filteredItems.length === 1) {
        this.selectItem(this.filteredItems[0])
        return
      }

      // Brak dopasowań — dodaj nową wartość
      if (this.filteredItems.length === 0 && this.inputText.trim()) {
        this.addNewValue()
      }
    },

	  selectItem(item) {
		  if (this.isSelected(item.value)) { this.inputText = ''; this.menuOpen = false; return }
		  const next = [...this.selectedValueLocal, item.value]
		  this.selectedValueLocal = next
		  this.$emit('update:modelValue', next)   // <-- zmiana
		  this.inputText = ''
		  this.menuOpen = false
	  },

	  addNewValue() {
		  const newVal = this.inputText.trim()
		  if (!newVal) return
		  if (this.isSelected(newVal)) { this.inputText = ''; this.menuOpen = false; return }
		  const next = [...this.selectedValueLocal, newVal]
		  this.selectedValueLocal = next
		  this.$emit('update:modelValue', next)   // <-- zmiana
		  this.inputText = ''
		  this.menuOpen = false
	  },

	  removeValue(val) {
		  const next = this.selectedValueLocal.filter(v => this.normalize(v) !== this.normalize(val))
		  this.selectedValueLocal = next
		  this.$emit('update:modelValue', next)   // <-- zmiana
	  }
  }
}
</script>
