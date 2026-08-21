<template>
	<div class="dynamic-text-fields">
		<div class="d-flex align-center">
      <!-- Toggle button left of the primary field -->
      <!-- Primary Field (Always Visible) -->
      <v-text-field
        v-model="values[0]"
        :label="getFieldLabel(0)"
        hide-details="auto"
        @update:model-value="emitUpdate"
      ></v-text-field>

      <v-btn
        v-if="maxFields > 1"
        :icon="expanded ? 'mdi-minus' : 'mdi-plus'"
        variant="text"
        color="primary"
        class="mr-2"
        @click="toggleExpanded"
      ></v-btn>
    </div>

    <!-- Additional Fields (Shown only when expanded) -->
    <v-expand-transition>
      <div v-if="expanded">
        <div v-for="index in (values.length - 1)" :key="index" class="d-flex align-center mb-3">
          <v-text-field
            v-model="values[index]"
            :label="getFieldLabel(index)"
            hide-details="auto"
            @update:model-value="emitUpdate"
          ></v-text-field>
        </div>
      </div>
    </v-expand-transition>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'

const props = defineProps({
  // v-model binding for the array of strings
  modelValue: {
    type: Array,
    default: () => ['']
  },
  // Labels for each field position (primary + additional)
  labels: {
    type: Array,
    default: () => []
  },
  // Total number of fields (primary + additional). Values: 2 or 3
  maxFields: {
    type: Number,
    default: 3,
    validator: (val) => [2, 3].includes(val)
  }
})

const emit = defineEmits(['update:modelValue'])

const { t } = useI18n()

// Internal reactive state to hold the field values
const values = ref([...props.modelValue])

// Ensure we always have at least one string to show the first v-text-field
if (values.value.length === 0) {
  values.value.push('')
}

// Whether the additional fields are visible
const expanded = ref(false)

const getFieldLabel = (index) => {
  const label = props.labels[index] || ''
  return index === 0 ? label : t('addBook.additional', { label })
}

const toggleExpanded = () => {
  expanded.value = !expanded.value
}

const emitUpdate = () => {
  // Returns an array containing the field values to the parent component
  emit('update:modelValue', [...values.value])
}

// Sync from parent if modified externally
watch(() => props.modelValue, (newVal) => {
  values.value = newVal.length ? [...newVal] : ['']
}, { deep: true })
</script>
