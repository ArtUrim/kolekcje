<template>
    <v-combobox
        v-model="selectedValueLocal"
        :items="items"
        :loading="loading"
        :search-input.sync="search"
        :label="label"
        :placeholder="placeholder"
        clearable
        :multiple="false"
        :clear-on-select="clearOnSelect"
        @input="handleInput"
        @change="handleChange"
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
    name: 'AutocompleteField',
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
    methods: {
        handleInput(value) {
            this.$emit('input', value);
        },
        handleChange(value) {
            this.$emit('change', value);
        },
        async searchItems(query) {
            if (!query) return

            if (this.searchTimeout) clearTimeout(this.searchTimeout)
            
            this.searchTimeout = setTimeout(async () => {
                try {
                    this.loading = true
                    const response = await fetch(`${this.apiEndpoint}?query=${encodeURIComponent(query)}`)
                    if (!response.ok) throw new Error(`Failed to fetch ${this.label}`)
                    
                    const data = await response.json()
                    this.items = data
                } catch (error) {
                    console.error(`Error fetching ${this.label}:`, error)
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
