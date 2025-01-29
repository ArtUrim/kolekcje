<template>
    <v-combobox
        v-model="selectedPublisherLocal"
        :items="publishers"
        :loading="loading"
        :search-input.sync="search"
        label="Publisher"
        placeholder="Select or add a publisher"
        clearable
        @input="updateValue"
    >
        <template v-slot:no-data>
            <v-list-item>
                <v-list-item-title>
                    No results found. Press <kbd>enter</kbd> to create "{{ search }}"
                </v-list-item-title>
            </v-list-item>
        </template>
    </v-combobox>
</template>

<script>
export default {
  name: 'Publisher',
  props: {
    value: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      valid: false,
      selectedPublisherLocal: null,
      publishers: [],
      loading: false,
      search: null,
    }
  },
  methods: {
    updateValue(val) {
      this.$emit('input', val)
    },
    async searchPublishers(query) {
      if (!query) return

      if (this.searchTimeout) clearTimeout(this.searchTimeout)
      
      this.searchTimeout = setTimeout(async () => {
        try {
          this.loading = true
          const response = await fetch(`/api/publishers?query=${encodeURIComponent(query)}`)
          if (!response.ok) throw new Error('Failed to fetch publishers')
          
          const data = await response.json()
          this.publishers = data
        } catch (error) {
          console.error('Error fetching publishers:', error)
        } finally {
          this.loading = false
        }
      }, 300)
    },
  },
  watch: {
    value: {
      immediate: true,
      handler(newValue) {
        this.selectedPublisherLocal = newValue
      }
    },
    selectedPublisherLocal(newValue) {
      if (newValue) {
        if (newValue.length > 2) {
          if (newValue.length === 3) {
            this.searchPublishers(newValue)
          }
        } else {
          this.publishers = []
        }
      }
    }
  }
}
</script>
