<template>
    <v-combobox
      v-model="selectedPublisher"
      :items="publishers"
      :loading="loading"
      :search-input.sync="search"
      label="Publisher"
      placeholder="Select or add a publisher"
      clearable
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
  data() {
    return {
      valid: false,
      selectedPublisher: null,
      publishers: [],
      loading: false,
      search: null,
    }
  },
  methods: {
    async searchPublishers(query) {
		console.log( "Ole" )
      if (!query) return

      // Add debounce to avoid too many requests
      if (this.searchTimeout) clearTimeout(this.searchTimeout)
      
      this.searchTimeout = setTimeout(async () => {
        try {
          this.loading = true
          const response = await fetch(`/api/publisher?query=${encodeURIComponent(query)}`)
          if (!response.ok) throw new Error('Failed to fetch publishers')
          
          const data = await response.json()
          this.publishers = data
        } catch (error) {
          console.error('Error fetching publishers:', error)
          // Handle error appropriately (show notification, etc.)
        } finally {
          this.loading = false
        }
      }, 300) // 300ms debounce
    },
  },
  watch: {
    selectedPublisher(newValue) {
		 if( newValue ) {
			 console.log("is Billy on the line?", newValue.length );
			 if (newValue.length > 2 ) {
				 if (newValue.length  === 3 ) {
					 this.searchPublishers(newValue);
					 console.log( "New query" )
				 }
			 }
			 else
			 {
				 this.publishers = [];
				 console.log( "Clear publishers" )
			 }
		 }
    }
  }
}
</script>
