<template>
  <v-dialog v-model="dialogModel" max-width="500px">
    <!-- Remove the activator slot since the dialog is controlled externally -->
    <v-card>
      <v-card-title class="headline grey lighten-2">
        Add New Author
      </v-card-title>
      <v-card-text>
        <v-combobox
          v-for="(author, index) in authors"
          :key="index"
          :label="index === 0 ? 'Select or type author name' : 'Additional author'"
          :items="availableAuthors"
          v-model="authors[index]"
          clearable
          :class="{ 'mt-2': index > 0 }"
        >
          <template v-slot:append>
            <v-btn
              v-if="index > 0"
              icon="mdi-minus"
              size="small"
              variant="text"
              @click="removeAuthorField(index)"
            ></v-btn>
            <v-btn
              v-if="index === authors.length - 1"
              icon="mdi-plus"
              size="small"
              variant="text"
              @click="addAuthorField"
            ></v-btn>
          </template>
        </v-combobox>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="closeDialog">
          Close
        </v-btn>
        <v-btn color="blue darken-1" text @click="saveAuthor">
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref } from 'vue';

// Define emits for the component
const emit = defineEmits(['save']);

// Define the v-model prop
const dialogModel = defineModel({ default: false });

const availableAuthors = ref(['Author A', 'Author B', 'Author C']);
const authors = ref([null]);

function addAuthorField() {
  authors.value.push(null);
}

function removeAuthorField(index) {
  authors.value.splice(index, 1);
}

function closeDialog() {
  console.log('Closing dialog');
  dialogModel.value = false;
  // Reset state
  authors.value = [null];
}

function saveAuthor() {
  const validAuthors = authors.value.filter(author => author && author.trim());

  if (validAuthors.length === 0) {
    emit('save', null);
  } else {
    const authorsWithIds = validAuthors.map((authorName, index) => ({
      id: `${Date.now()}-${index}`, // Simple unique ID generation
      name: authorName,
    }));
    emit('save', authorsWithIds);
  }
  closeDialog();
}
</script>

<style scoped>
/* Add any component-specific styles here */
</style>