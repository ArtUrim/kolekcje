<template>
    <v-container fluid class="pa-6">
        <!-- Custom Card Components with Transitions -->
        <v-row class="mb-2">
            <v-col v-for="(card, index) in cards"
                :key="index" cols="12" md="6" lg="3" >
                <expandable-text :card="card"
                @toggle-expanded="handleToggleExpanded" />
            </v-col>
        </v-row>
        <v-row class="mb-2 position-relative">
            <v-col v-for="(card, index) in longCards"
                :key="index" cols="12" md="6" lg="9" >
                <expandable-text :card="card"
                @toggle-expanded="handleToggleExpanded" />
            </v-col>

            <!-- Edit Button positioned in bottom right -->
            <v-btn
            color="primary"
            variant="flat"
            prepend-icon="mdi-pencil"
            class="edit-button"
            @click="openEditDialog"
            >
            {{ $t('books.edit') }}
            </v-btn>
        </v-row>

        <!-- Edit Dialog -->
        <v-dialog
            v-model="showEditDialog"
            max-width="1200"
            persistent
            scrollable
        >
            <v-card>
                <v-card-title class="d-flex justify-space-between align-center">
                    <span>{{ $t('books.edit') }}</span>
                    <v-btn
                        icon="mdi-close"
                        variant="text"
                        @click="closeAddBookDialog"
                    />
                </v-card-title>
                <v-card-text class="pa-0">
                    <AddBook
                        :book-id="bookId"
                        :initial-book-data="extractedBookData"
                        @book-updated="onBookUpdated"
                        @cancel-edit="onCancelEdit"
                    />
                </v-card-text>
            </v-card>
        </v-dialog>
    </v-container>
</template>

<script>
export default {
  emits: ['book-updated', 'edit-cancelled'],
 
  props: {
    fields: {
      type: Object,
      required: true
    },
    bookId: {
      type: [String, Number],
      default: null
    }
  },
  
  data() {
    return {
      showEditDialog: false,
      extractedBookData: null,
      cards: [],
      longCards: []
    }
  },
  
  mounted() {
    // Decompose fields prop into cards and longCards
    this.cards = this.fields.cards || [];
    this.longCards = this.fields.longCards || [];
  },
  
  watch: {
    fields: {
      handler(newFields) {
        // Update cards when fields prop changes
        this.cards = newFields.cards || [];
        this.longCards = newFields.longCards || [];
      },
      deep: true
    }
  },
  
  methods: {
    handleToggleExpanded(card) {
      card.expanded = !card.expanded;
    },

    closeAddBookDialog() {
      console.log('Closing the Add Book Dialog');
      this.showEditDialog = false;
    },
    
    openEditDialog() {
      this.extractedBookData = null;
      this.showEditDialog = true;
    },
    
    onBookUpdated(updatedBookData) {
      this.showEditDialog = false;
      this.$emit('book-updated', updatedBookData);
    },

    onCancelEdit() {
      this.showEditDialog = false;
      this.$emit('edit-cancelled');
    }
  }
}
</script>

<style scoped>
.v-expansion-panel-title {
  font-weight: 500;
}

h1, h2 {
  font-weight: 700;
}

.edit-button {
  position: absolute;
  bottom: 16px;
  right: 16px;
  z-index: 1;
}
</style>