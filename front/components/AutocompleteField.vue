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
    return-object
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
    type: [String, Object],
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
    let emitValue = null

    if (value === null || value === undefined || value === '') {
      emitValue = null
    } else if (typeof value === 'string') {
      // Handle custom input (not selected from dropdown)
      emitValue = {
        id: null,
        title: value.trim(),
        value: value.trim(),
        isCustom: true
      }
    } else if (typeof value === 'object' && value !== null) {
      // Handle selected items from dropdown or existing object
      emitValue = {
        id: value.id || null,
        title: value.title || value.value || value.text || value.name,
        value: value.value || value.title || value.text || value.name,
        isCustom: value.isCustom || false
      }
    }

    emit('update:modelValue', emitValue)

    // Clear on select if enabled
    if (props.clearOnSelect && emitValue) {
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

    // Ensure items have the expected format
    items.value = data.map(item => {
      if (typeof item === 'string') {
        return {
          id: null,
          title: item,
          value: item,
          isCustom: false
        }
      }
      return {
        id: item.id || null,
        title: item.title || item.value || item.text || item.name,
        value: item.value || item.title || item.text || item.name,
        isCustom: false
      }
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
    searchInput.value = typeof newValue === 'object' ? newValue?.title || '' : newValue || ''
  }
}, { immediate: true })
</script>