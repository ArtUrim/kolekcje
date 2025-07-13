<template>
  <div class="autocomplete-with-more">
      <v-combobox
          v-model="selectedValueLocal"
          :items="items"
          :loading="loading"
          :search-input.sync="search"
          :label="label"
          :placeholder="placeholder"
          clearable
          @input="updateValue"
          :multiple="clearOnSelect"
          :clear-on-select="false"
      >
      <v-btn @click="openDialog" class="mt-2">Open Multi-Select Window</v-btn>
    <!-- More button -->
    <v-btn
      class="more-button"
      @click="openDialog"
    >
      More
    </v-btn>

          <template v-slot:no-data>
              <v-list-item>
                  <v-list-item-title>
                      No results found. Press <kbd>enter</kbd> to create "{{ search }}"
                  </v-list-item-title>
              </v-list-item>
          </template>
      </v-combobox>

      <v-dialog v-model="modalOpen" max-width="600">
          <v-card>
              <v-card-title>
                  Add Multiple {{ label }}
              </v-card-title>
              <v-card-text>
                  <div v-for="(item, index) in modalComboboxes" :key="index" class="mb-4">
                      <v-combobox
                          v-model="item.value"
                          :items="item.items"
                          :loading="item.loading"
                          :search-input.sync="item.search"
                          :label="`${label} #${index + 1}`"
                          :placeholder="placeholder"
                          clearable
                          @input="updateModalValue(index)"
                          :multiple="clearOnSelect"
                          :clear-on-select="false"
                      >
                          <template v-slot:no-data>
                              <v-list-item>
                                  <v-list-item-title>
                                      No results found. Press <kbd>enter</kbd> to create "{{ item.search }}"
                                  </v-list-item-title>
                              </v-list-item>
                          </template>
                      </v-combobox>
                  </div>
                  <v-btn @click="addCombobox" color="primary" class="mb-4">
                      Add Another
                  </v-btn>
              </v-card-text>
              <v-card-actions class="justify-end">
                  <v-btn text @click="modalOpen = false">Cancel</v-btn>
                  <v-btn color="primary" @click="saveModalValues">Save</v-btn>
              </v-card-actions>
          </v-card>
      </v-dialog>
  </div>
</template>

<script>
export default {
  name: 'AutocompleteField',
  props: {
      value: {
          type: [String, Array],
          default: null
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
      },
      clearOnSelect: {
          type: Boolean,
          default: false
      }
  },
  data() {
      return {
          valid: false,
          selectedValueLocal: null,
          items: [],
          loading: false,
          search: null,
          searchTimeout: null,
          modalOpen: false,
          modalComboboxes: []
      }
  },
  methods: {
      updateValue(val) {
          this.$emit('input', val)
      },
      async searchItems(query, isModal = false, index = null) {
          if (!query) return

          if (this.searchTimeout) clearTimeout(this.searchTimeout)
          
          this.searchTimeout = setTimeout(async () => {
              try {
                  if (isModal) {
                      this.modalComboboxes[index].loading = true
                  } else {
                      this.loading = true
                  }
                  
                  const response = await fetch(`${this.apiEndpoint}?query=${encodeURIComponent(query)}`)
                  if (!response.ok) throw new Error(`Failed to fetch ${this.label}`)
                  
                  const data = await response.json()
                  
                  if (isModal) {
                      this.$set(this.modalComboboxes[index], 'items', data)
                  } else {
                      this.items = data
                  }
              } catch (error) {
                  console.error(`Error fetching ${this.label}:`, error)
              } finally {
                  if (isModal) {
                      this.modalComboboxes[index].loading = false
                  } else {
                      this.loading = false
                  }
              }
          }, 300)
      },
      openModal() {
          this.modalComboboxes = [this.createNewCombobox()]
          this.modalOpen = true
      },
      createNewCombobox() {
          return {
              value: null,
              items: [],
              loading: false,
              search: null
          }
      },
      addCombobox() {
          this.modalComboboxes.push(this.createNewCombobox())
      },
      updateModalValue(index) {
          const value = this.modalComboboxes[index].value
          if (value && value.length > 2 && value.length === 3) {
              this.searchItems(value, true, index)
          } else if (!value || value.length <= 2) {
              this.modalComboboxes[index].items = []
          }
      },
      saveModalValues() {
          const allValues = this.modalComboboxes
              .map(combobox => combobox.value)
              .filter(value => value !== null && value !== '')
          
          if (this.clearOnSelect) {
              // If multiple is enabled, combine all values into one array
              const combined = allValues.reduce((acc, val) => {
                  if (Array.isArray(val)) {
                      return [...acc, ...val]
                  }
                  return [...acc, val]
              }, [])
              this.$emit('input', combined)
          } else {
              // For single values, take the last non-empty value
              const lastValue = allValues.length > 0 ? allValues[allValues.length - 1] : null
              this.$emit('input', lastValue)
          }
          
          this.modalOpen = false
      }
  },
  watch: {
      value: {
          immediate: true,
          handler(newValue) {
              this.selectedValueLocal = newValue
          }
      },
      selectedValueLocal(newValue) {
          if (newValue) {
              if (newValue.length > 2) {
                  if (newValue.length === 3) {
                      this.searchItems(newValue)
                  }
              } else {
                  this.items = []
              }
          }
      }
  }
}
</script>


<style scoped>
.autocomplete-with-more {
  display: flex;
  align-items: center;
}

.more-button {
  margin-left: 8px;
}
</style>
