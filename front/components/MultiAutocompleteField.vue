<template>
  <div>
    <div v-for="(field, index) in fieldValues" :key="index" class="d-flex align-center" :class="{ 'mt-2': index > 0 }">
      <AutocompleteField
        :value="field"
        @input="updateFieldValue(index, $event)"
        @change="handleFieldChange(index, $event)"
        :label="index === 0 ? label : `Additional ${label}`"
        :placeholder="placeholder"
        :api-endpoint="apiEndpoint"
        :clear-on-select="clearOnSelect"
        class="flex-grow-1 mr-2"
      />
      <v-btn
        v-if="index > 0"
        icon="mdi-minus"
        size="small"
        variant="text"
        @click="removeField(index)"
      ></v-btn>
      <v-btn
        v-if="index === fieldValues.length - 1"
        icon="mdi-plus"
        size="small"
        variant="text"
        @click="addField"
      ></v-btn>
    </div>
  </div>
</template>

<script>
import AutocompleteField from './AutocompleteField.vue';

export default {
  name: 'MultiAutocompleteField',
  components: {
    AutocompleteField,
  },
  props: {
    value: {
      type: Array,
      default: () => [],
    },
    label: {
      type: String,
      required: true,
    },
    placeholder: {
      type: String,
      required: true,
    },
    apiEndpoint: {
      type: String,
      required: true,
    },
    clearOnSelect: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      fieldValues: [null],
      committedValues: [null], // Track only committed/selected values
    };
  },
  watch: {
    value: {
      immediate: true,
      handler(newValue) {
        console.log('value watch:', newValue);
        if (newValue && newValue.length > 0) {
          this.fieldValues = [...newValue, null];
          this.committedValues = [...newValue, null];
        } else {
          this.fieldValues = [null];
          this.committedValues = [null];
        }
      },
    },
  },
  methods: {
    updateFieldValue(index, value) {
      // This handles typing/input events - update display but don't emit
      console.log('updateFieldValue (typing):', { index, value, type: typeof value });

      let actualValue = this.extractActualValue(value);
      console.log('Processed actualValue (typing):', actualValue);

      // Update the field value for display
      this.fieldValues[index] = actualValue || null;

      // Don't emit here - wait for selection/change event
    },

    handleFieldChange(index, value) {
      // This handles selection/blur events - commit the value and emit
      console.log('handleFieldChange (selection):', { index, value, type: typeof value });

      let actualValue = this.extractActualValue(value);
      console.log('Processed actualValue (selection):', actualValue);

      // Update both display and committed values
      this.fieldValues[index] = actualValue || null;
      this.committedValues[index] = actualValue || null;

      // Auto-add new field if this field has content and it's the last field
      if (actualValue && actualValue.trim() !== '' && index === this.fieldValues.length - 1) {
        this.fieldValues.push(null);
        this.committedValues.push(null);
      }

      // Emit the committed values
      this.emitValidValues();
    },

    extractActualValue(value) {
      // Handle different types of values that might be received
      if (value === null || value === undefined) {
        return null;
      }

      if (typeof value === 'string') {
        return value;
      }

      if (typeof value === 'object') {
        // Handle InputEvent objects
        if (value.target && value.target.value !== undefined) {
          return value.target.value;
        }
        // Handle composition events
        if (value.data !== undefined) {
          return value.data;
        }
        // Handle other event-like objects
        if (value.inputType && value.target) {
          return value.target.value;
        }
        // Fallback for objects
        if (typeof value.toString === 'function' && value.toString() !== '[object Object]') {
          return value.toString();
        }

        console.warn('Unexpected object value:', value);
        return null;
      }

      // For numbers or other primitive types
      return String(value);
    },

    emitValidValues() {
      // Filter out null/empty values from committed values only
      const validValues = this.committedValues
        .filter(v => v !== null && v !== undefined && v !== '')
        .map(v => String(v).trim())
        .filter(v => v !== '');

      console.log('Emitting committed values:', validValues);
      this.$emit('input', validValues);
    },

    addField() {
      this.fieldValues.push(null);
      this.committedValues.push(null);
    },

    removeField(index) {
      if (this.fieldValues.length > 1) {
        this.fieldValues.splice(index, 1);
        this.committedValues.splice(index, 1);

        // Ensure we always have at least one field
        if (this.fieldValues.length === 0) {
          this.fieldValues.push(null);
          this.committedValues.push(null);
        }
        this.emitValidValues();
      }
    },
  },
};
</script>

<style scoped>
.d-flex {
  display: flex;
}
.align-center {
  align-items: center;
}
.flex-grow-1 {
  flex-grow: 1;
}
.mr-2 {
  margin-right: 8px;
}
.mt-2 {
  margin-top: 8px;
}
</style>