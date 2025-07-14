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
          @update:model-value="debouncedEmit"
        />
      </div>

      <div class="button-container">
        <v-btn
          v-if="fields.length > 1"
          icon="mdi-minus"
          size="small"
          variant="text"
          color="error"
          @click="removeField(index)"
        />
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
import { ref, watch } from 'vue'
import AutocompleteField from './AutocompleteField.vue'

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

const emit = defineEmits(['update:modelValue'])

const fields = ref([])
let fieldIdCounter = 0
const emitTimeout = ref(null)

const createField = (value = null) => ({
  id: ++fieldIdCounter,
  value: value || null
})

const initializeFields = () => {
  if (props.modelValue?.length > 0) {
    fields.value = props.modelValue.map(value => createField(value))
    fields.value.push(createField()) // Empty field at end
  } else {
    fields.value = [createField()]
  }
}

const getFieldLabel = (index) => {
  return index === 0 ? props.label : `Additional ${props.label}`
}

const addField = () => {
  fields.value.push(createField())
}

const removeField = (index) => {
  if (fields.value.length > 1 && index >= 0 && index < fields.value.length) {
    fields.value.splice(index, 1)
    if (fields.value.length === 0) {
      fields.value.push(createField())
    }
    emitValues()
  }
}

const debouncedEmit = () => {
  if (emitTimeout.value) {
    clearTimeout(emitTimeout.value)
  }
  emitTimeout.value = setTimeout(emitValues, 300)
}

const emitValues = () => {
  const validValues = fields.value
    .map(field => field.value)
    .filter(value => value !== null && value.title?.trim() !== '')

  emit('update:modelValue', validValues)
}

watch(() => props.modelValue, (newValue) => {
  const currentVals = fields.value
    .map(field => field.value)
    .filter(value => value !== null)

  const newVals = newValue || []

  if (JSON.stringify(currentVals) !== JSON.stringify(newVals)) {
    initializeFields()
  }
}, { immediate: true, deep: true })

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
  min-width: 0;
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