<template>
  <div class="dynamic-text-fields">
    <!-- Primary Field (Always Visible) -->
    <v-text-field
      v-model="values[0]"
      label="Primary Value"
      variant="outlined"
      hide-details="auto"
      class="mb-3"
      @update:model-value="emitUpdate"
    ></v-text-field>

    <!-- Additional Fields (Shown when buttons are pressed) -->
    <v-expand-transition group>
      <div v-for="index in (values.length - 1)" :key="index" class="d-flex align-center mb-3">
        <v-text-field
          v-model="values[index]"
          :label="`Additional Value ${index}`"
          variant="outlined"
          hide-details="auto"
          append-inner-icon="mdi-close"
          @click:append-inner="removeField(index)"
          @update:model-value="emitUpdate"
        ></v-text-field>
      </div>
    </v-expand-transition>

    <!-- Static Text Buttons to append new fields -->
    <div class="d-flex flex-wrap gap-4 mt-1" v-if="values.length < maxFields">
      <v-btn
        v-if="values.length === 1 && maxFields >= 2"
        variant="text"
        color="primary"
        @click="addField"
      >
        + Add Second Value
      </v-btn>

      <v-btn
        v-if="values.length === 2 && maxFields >= 3"
        variant="text"
        color="primary"
        @click="addField"
      >
        + Add Third Value
      </v-btn>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  // v-model binding for the array of strings
  modelValue: {
    type: Array,
    default: () => [''] 
  },
  // Allows handling "one or two additional buttons" (Values: 2 or 3)
  maxFields: {
    type: Number,
    default: 3, 
    validator: (val) => [2, 3].includes(val)
  }
})

const emit = defineEmits(['update:modelValue'])

// Internal reactive state to hold 1 to 3 strings
const values = ref([...props.modelValue])

// Ensure we always have at least one string to show the first v-text-field
if (values.value.length === 0) {
  values.value.push('')
}

const addField = () => {
  if (values.value.length < props.maxFields) {
    values.value.push('')
    emitUpdate()
  }
}

const removeField = (index) => {
  values.value.splice(index, 1)
  emitUpdate()
}

const emitUpdate = () => {
  // Returns an array containing 1 to 3 strings to the parent component
  emit('update:modelValue', [...values.value])
}

// Sync from parent if modified externally
watch(() => props.modelValue, (newVal) => {
  values.value = newVal.length ? [...newVal] : ['']
}, { deep: true })
</script>

<style scoped>
.gap-4 {
  gap: 16px;
}
</style>
