<template>
    <v-container fluid class="pa-6">
        <BookInfo :book="bookInfoData" />
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
import BookInfo from './BookInfo.vue'

const toArray = (value) => {
  if (Array.isArray(value)) {
    return value.filter(Boolean)
  }

  if (typeof value === 'string' && value.trim()) {
    return value.split(',').map((item) => item.trim()).filter(Boolean)
  }

  return []
}

const normalizeFieldValue = (value) => {
  if (value == null) {
    return ''
  }

  if (Array.isArray(value)) {
    return value.join(', ')
  }

  return String(value)
}

const getCardValue = (cards = [], title, valueKey = 'shortText') => {
  const card = cards.find((item) => item?.title === title)
  return normalizeFieldValue(card?.[valueKey])
}

export default {
  components: {
    BookInfo
  },
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

  computed: {
    bookInfoData() {
      const source = this.fields?.originalData || {}

      if (Object.keys(source).length) {
        return {
          title: source?.title || '',
          originalTitle: source?.original_title || '',
          authors: toArray(source?.authors_details?.map((author) => author?.name) || source?.authors),
          isbn: source?.isbn || '',
          releaseDate: source?.release_date || '',
          firstPolishRelease: source?.first_polish_release_date || '',
          format: source?.format || '',
          pages: source?.pages || '',
          serie: source?.series_name || '',
          size: source?.size || '',
          language: source?.language_name || '',
          translator: source?.translator || '',
          publishers: toArray(source?.publishers_details?.map((publisher) => publisher?.name) || source?.publishers),
          genres: toArray(source?.genres_details?.map((genre) => genre?.name) || source?.genres),
          labels: toArray(source?.labels_details?.map((label) => label?.name) || source?.labels),
          description: source?.description || '',
          note: source?.note || ''
        }
      }

      return {
        title: getCardValue(this.cards, 'Title'),
        originalTitle: getCardValue(this.cards, 'Title', 'expandedText'),
        authors: toArray(getCardValue(this.cards, 'Authors')),
        isbn: getCardValue(this.longCards, 'Details').match(/ISBN:\s*([^|]+)/)?.[1]?.trim() || '',
        releaseDate: getCardValue(this.longCards, 'Details').match(/Year:\s*([^|]+)/)?.[1]?.trim() || '',
        firstPolishRelease: getCardValue(this.longCards, 'Details', 'expandedText').match(/First Polish Release:\s*([^|]+)/)?.[1]?.trim() || '',
        format: getCardValue(this.longCards, 'Details', 'expandedText').match(/Format:\s*([^|]+)/)?.[1]?.trim() || '',
        pages: getCardValue(this.longCards, 'Details').match(/Pages:\s*([^|]+)/)?.[1]?.trim() || '',
        serie: getCardValue(this.cards, 'Series'),
        size: getCardValue(this.longCards, 'Details', 'expandedText').match(/Size:\s*([^|]+)/)?.[1]?.trim() || '',
        language: getCardValue(this.longCards, 'Details', 'expandedText').match(/Language:\s*([^|]+)/)?.[1]?.trim() || '',
        translator: getCardValue(this.longCards, 'Details', 'expandedText').match(/Translator:\s*([^|]+)/)?.[1]?.trim() || '',
        publishers: toArray(getCardValue(this.cards, 'Publisher')),
        genres: toArray(this.longCards.find((card) => card?.title === 'Details')?.tags || []),
        labels: toArray(this.longCards.find((card) => card?.title === 'Notes')?.tags || []),
        description: getCardValue(this.longCards, 'Description'),
        note: getCardValue(this.longCards, 'Notes')
      }
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