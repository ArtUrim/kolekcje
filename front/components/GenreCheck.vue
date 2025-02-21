<template>
    <v-combobox
        v-model="selectedValueLocal"
        :items="items"
        :loading="loading"
        :search-input.sync="search"
        :label="label"
        :placeholder="placeholder"
        clearable
        @input="updateValue"
		  :multiple="true"
		  :clear-on-select="false"
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
    props: {
        value: {
            type: String,
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
            searchTimeout: null
        }
    },
	 async mounted() {
		 await this.fetchGenres()
	 },
    methods: {
        updateValue(val) {
            this.$emit('input', val)
        },
		 async fetchGenres() {
			 try {
				 this.loading = true
				 const response = await fetch( "/api/genres" )
				 const data = await response.json()
			 	 this.items = data
				 } catch (error) {
					 console.error( "Error in fetch genres", error )
				 } finally {
					 this.loading = false
				 }
		 }
    },
		
    watch: {
        value: {
            immediate: true,
            handler(newValue) {
                this.selectedValueLocal = newValue
            }
        }
    }
}
</script>
