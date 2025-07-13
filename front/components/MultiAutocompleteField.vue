<template>
  <div class="multi-autocomplete-field">
    <div
      v-for="(field, index) in fields"
      :key="field.id"
      class="field-row"
      :class="{ 'mt-3': index > 0 }"
    >
      <div class="field-container">
        <AutocompleteField
          v-model="field.value"
          :label="getFieldLabel(index)"
          :placeholder="placeholder"
          :api-endpoint="apiEndpoint"
          :clear-on-select="clearOnSelect"
        />
      </div>

      <div class="button-container">
        <!-- Remove button (only show if more than one field) -->
        <v-btn
          v-if="fields.length > 1"
          icon="mdi-minus"
          size="small"
          variant="text"
          color="error"
          @click="removeField(index)"
        />

        <!-- Add button (only show on last field) -->
        <v-btn
          v-if="index === fields.length - 1"
          icon="mdi-plus"
          size="small"
          variant="text"
          color="primary"
          @click="addField"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import AutocompleteField from './AutocompleteField.vue'

// Props
const props = defineProps({
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
  },
  clearOnSelect: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['update:modelValue'])

// Reactive data
const fields = ref([])
let fieldIdCounter = 0
const emitTimeout = ref(null)

// Create a new field object
const createField = (value = null) => ({
  id: ++fieldIdCounter,
  value: value
})

// Initialize fields
const initializeFields = () => {
  if (props.modelValue && props.modelValue.length > 0) {
    fields.value = props.modelValue.map(value => createField(value))
    // Always ensure there's an empty field at the end
    fields.value.push(createField())
  } else {
    fields.value = [createField()]
  }
}

// Get label for field based on index
const getFieldLabel = (index) => {
  return index === 0 ? props.label : `Additional ${props.label}`
}

// Add new field
const addField = () => {
  fields.value.push(createField())
}

// Remove field
const removeField = (index) => {
  if (fields.value.length > 1 && index >= 0 && index < fields.value.length) {
    fields.value.splice(index, 1)

    // Ensure we always have at least one field
    if (fields.value.length === 0) {
      fields.value.push(createField())
    }

    // Emit immediately when removing
    emitValues()
  }
}

// Debounced emit to avoid too frequent updates
const debouncedEmit = () => {
  if (emitTimeout.value) {
    clearTimeout(emitTimeout.value)
  }

  emitTimeout.value = setTimeout(() => {
    emitValues()
  }, 500)
}

// Emit current values to parent
const emitValues = () => {
  const validValues = fields.value
    .map(field => field.value)
    .filter(value => value !== null && value !== undefined && value !== '')
    .map(value => String(value).trim())
    .filter(value => value !== '')

  emit('update:modelValue', validValues)
}

// Watch for changes in field values and emit debounced updates
watch(fields, () => {
  debouncedEmit()
}, { deep: true })

// Watch for external changes to modelValue
watch(() => props.modelValue, (newValue) => {
  const currentVals = fields.value
    .map(field => field.value)
    .filter(value => value !== null && value !== undefined && value !== '')

  const newVals = newValue || []

  if (JSON.stringify(currentVals) !== JSON.stringify(newVals)) {
    initializeFields()
  }
}, { immediate: true, deep: true })

// Initialize on mount
initializeFields()
</script>

<style scoped>
.multi-autocomplete-field {
  width: 100%;
}

.field-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.field-container {
  flex: 1;
}

.button-container {
  display: flex;
  gap: 4px;
  min-width: 80px;
  justify-content: flex-end;
}

.mt-3 {
  margin-top: 12px;
}
</style>