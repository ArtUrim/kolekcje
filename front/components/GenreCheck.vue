<template>
    <v-combobox
        v-model="selectedValueLocal"
        :items="items"
        :loading="loading"
        :search-input.sync="search"
        :label="label"
        :placeholder="placeholder"
        clearable
        multiple
        :clear-on-select="false"
        @change="handleChange"
        @update:search-input="handleSearchInput"
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
            type: Array, // Changed from String to Array since it's multiple
            default: () => [] // Changed default to return empty array
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
            selectedValueLocal: [],  // Initialize as array
            items: [],
            loading: false,
            search: null,
            searchTimeout: null,
            lastAddedItem: null
        }
    },
    async mounted() {
        await this.fetchGenres()
    },
    watch: {
        selectedValueLocal: {
            handler(newValue) {
                console.log( "handleChange",newValue)
                if (!newValue) return
                console.log( "handleChange2",newValue)

                const uniqueValues = Array.from(new Set(
                    newValue.filter(item => item && typeof item === 'string')
                ))
                console.log( "handleChange3",uniqueValues)

                if (JSON.stringify(uniqueValues) !== JSON.stringify(newValue)) {
                    this.selectedValueLocal = uniqueValues
                }
                console.log( "handleChange4",this.selectedValueLocal)
                this.selectedValueLocal = null

                this.$emit('input', uniqueValues)
            },
            deep: true
        },
        value: {
            immediate: true,
            handler(newValue) {
                // Ensure we don't create a circular update
                if (JSON.stringify(newValue) !== JSON.stringify(this.selectedValueLocal)) {
                    this.selectedValueLocal = newValue
                }
            }
        }
    },
    methods: {
        async fetchGenres() {
            try {
                this.loading = true
                const response = await fetch("/api/genres")
                const data = await response.json()
                this.items = data
            } catch (error) {
                console.error("Error in fetch genres", error)
            } finally {
                this.loading = false
            }
        },
        handleChange(value) {
            if (!Array.isArray(value)) return

            const uniqueValues = Array.from(new Set(
                value.filter(item => item && typeof item === 'string')
            ))

            if (JSON.stringify(uniqueValues) !== JSON.stringify(value)) {
                this.selectedValueLocal = uniqueValues
            }
        },

        handleSearchInput(val) {
            if (this.lastAddedItem === val) {
                this.search = null
                this.lastAddedItem = null
            }
        }
    }
}
</script>