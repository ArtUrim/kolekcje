<template>
  <div>
    <!-- Wybrane chipy: Zmieniono v-if na v-show aby zapobiec skokom DOM -->
    <div v-show="selectedValueLocal.length" class="d-flex flex-wrap gap-1 mb-2">
      <v-chip
        v-for="(val, index) in selectedValueLocal"
        :key="val"
        closable
        @click:close="removeValue(index)" 
      >
        {{ val.title }}
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
      @click="openMenu" 
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
      selectedValueLocal: [],
      items: [],
      loading: false,
      inputText: '',
      menuOpen: false
    }
  },

  watch: {
    modelValue: {
      handler(newValue) {
        const safeValue = Array.isArray(newValue) ? newValue : [];
        if (JSON.stringify(safeValue) !== JSON.stringify(this.selectedValueLocal)) {
          this.selectedValueLocal = [...safeValue];
        }
      },
      immediate: true 
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
        
        const data = await response.json()
        
        this.items = data.map((item, index) => {
          if (typeof item === 'string') {
            return { 
              id: `genre-${index}`, 
              title: item, 
              value: item 
            }
          }
          return item
        })
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
      const exact = this.filteredItems.find(
        item => this.normalize(item.value) === this.normalize(this.inputText)
      )
      if (exact) {
        this.selectItem(exact)
        return
      }

      if (this.filteredItems.length === 1) {
        this.selectItem(this.filteredItems[0])
        return
      }

      if (this.filteredItems.length === 0 && this.inputText.trim()) {
        this.addNewValue()
      }
    },

    selectItem(item) {
      if (this.isSelected(item.value)) { 
        this.inputText = ''; 
        this.menuOpen = false; 
        return 
      }
      const next = [...this.selectedValueLocal, item]
      this.selectedValueLocal = next
      this.$emit('update:modelValue', next) 
      this.inputText = ''
      this.menuOpen = false
    },

    addNewValue() {
      const newVal = this.inputText.trim()
		 console.log( "Add value: ", newVal );
      if (!newVal) return
      if (this.isSelected(newVal)) { 
			console.log( "is selected" );
        this.inputText = ''; 
        this.menuOpen = false; 
        return 
      }
  	   const newObj = { 'id': null, 'title': newVal, 'value': newVal };
      const next = [...this.selectedValueLocal, newObj]
      this.selectedValueLocal = next
      this.$emit('update:modelValue', next) 
      this.inputText = ''
      this.menuOpen = false
    },

    // Zmodyfikowana funkcja: Usuwanie na podstawie indeksu
    removeValue(index) {
      const next = [...this.selectedValueLocal]
      next.splice(index, 1) // Bezpiecznie usuwa dokładnie 1 element pod tym indeksem
      this.selectedValueLocal = next
      this.$emit('update:modelValue', next)
    }
  }
}
</script>
