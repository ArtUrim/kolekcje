<template>
  <div class="autocomplete-with-more">
    <!-- Base AutocompleteField -->
    <AutocompleteField
      v-model="selectedValue"
      :label="label"
      :placeholder="placeholder"
      :api-endpoint="apiEndpoint"
      :clear-on-select="clearOnSelect"
      @input="updateValue"
    />
    
    <!-- More button -->
    <v-btn
      class="more-button"
      @click="openMoreDialog"
    >
      More
    </v-btn>
    
    <!-- Dialog for additional inputs -->
    <v-dialog
      v-model="dialogOpen"
      max-width="600px"
    >
      <v-card>
        <v-card-title>Additional Inputs</v-card-title>
        <v-card-text>
          <v-container>
            <v-row
              v-for="(item, index) in additionalInputs"
              :key="index"
              class="mb-3"
            >
              <v-col cols="9">
                <v-combobox
                  v-model="item.value"
                  :items="items"
                  :label="label"
                  :placeholder="placeholder"
                  clearable
                />
              </v-col>
              <v-col cols="3">
                <v-btn
                  v-if="index === additionalInputs.length - 1"
                  color="primary"
                  @click="addNewInput"
                >
                  Add
                </v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue darken-1"
            text
            @click="dialogOpen = false"
          >
            Close
          </v-btn>
          <v-btn
            color="blue darken-1"
            text
            @click="saveAdditionalInputs"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
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
      selectedValue: null,
      dialogOpen: false,
      additionalInputs: [],
      items: [] // This would typically be populated from the API
    };
  },
  watch: {
    value: {
      immediate: true,
      handler(newValue) {
        this.selectedValue = newValue;
      }
    }
  },
  methods: {
    updateValue(val) {
      this.$emit('input', val);
    },
    openMoreDialog() {
      // Initialize with at least one input that copies the current value
      this.additionalInputs = [{ value: this.selectedValue || '' }];
      this.dialogOpen = true;
    },
    addNewInput() {
      this.additionalInputs.push({ value: '' });
    },
    saveAdditionalInputs() {
      // Here you can implement logic to save or process the additional inputs
      // For example, emit an event with all values
      const values = this.additionalInputs.map(item => item.value).filter(Boolean);
      this.$emit('additional-inputs', values);
      this.dialogOpen = false;
    }
  }
};
</script>

<style scoped>
.autocomplete-with-more {
  display: flex;
  align-items: center;
}

.more-button {
  margin-left: 8px;
}
</style>
