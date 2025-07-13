<template>
  <v-combobox
    v-model="internalValue"
    :items="items"
    :loading="loading"
    :label="label"
    :placeholder="placeholder"
    :clearable="true"
    :multiple="false"
    :hide-no-data="false"
    :search="searchInput"
    item-title="title"
    item-value="value"
    @update:search="onSearchInput"
  >
    <template #no-data>
      <v-list-item>
        <v-list-item-title>
          Wprowadź co najmniej 3 litery, aby uzyskać podpowiedź
        </v-list-item-title>
      </v-list-item>
    </template>
  </v-combobox>
</template>

<script setup>
import { ref, watch, computed, nextTick } from 'vue'

// Props
const props = defineProps({
  modelValue: {
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
})

// Emits
const emit = defineEmits(['update:modelValue'])

// Reactive data
const items = ref([])
const loading = ref(false)
const searchInput = ref('')
const searchTimeout = ref(null)

// Internal value that syncs with modelValue
const internalValue = computed({
  get: () => props.modelValue,
  set: (value) => {
    // Extract string value from various formats
    let cleanValue = null

    if (value === null || value === undefined || value === '') {
      cleanValue = null
    } else if (typeof value === 'string') {
      cleanValue = value.trim() || null
    } else if (typeof value === 'object' && value !== null) {
      // Handle selected items from dropdown
      cleanValue = value.title || value.value || value.text || value.name || null
    }

    emit('update:modelValue', cleanValue)

    // Clear on select if enabled
    if (props.clearOnSelect && cleanValue) {
      nextTick(() => {
        searchInput.value = ''
      })
    }
  }
})

// Search functionality
const onSearchInput = (query) => {
  searchInput.value = query

  if (!query || query.length < 3) {
    items.value = []
    return
  }

  // Debounce search requests
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value)
  }

  searchTimeout.value = setTimeout(async () => {
    await searchItems(query)
  }, 300)
}

const searchItems = async (query) => {
  try {
    loading.value = true
    const response = await fetch(`${props.apiEndpoint}?query=${encodeURIComponent(query)}`)

    if (!response.ok) {
      throw new Error(`Failed to fetch ${props.label}`)
    }

    const data = await response.json()

    data.forEach((item, index) => {
      console.log(`Item ${index}:`, JSON.stringify(item, null, 2))
      console.log(`Item ${index} fields:`, Object.keys(item))
    })

    // Ensure items have the expected format
    items.value = data.map(item => {
      if (typeof item === 'string') {
        return { title: item, value: item }
      }
      return item
    })
  } catch (error) {
    console.error(`Error fetching ${props.label}:`, error)
    items.value = []
  } finally {
    loading.value = false
  }
}

// Watch for external value changes
watch(() => props.modelValue, (newValue) => {
  if (newValue !== internalValue.value) {
    searchInput.value = newValue || ''
  }
}, { immediate: true })
  </script>