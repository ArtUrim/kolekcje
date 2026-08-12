<template>
	<v-container fluid class="pa-6">
		<BookInfo :book="bookInfoData" @delete-requested="openDeleteDialog" />
		<!-- Custom Card Components with Transitions -->

		<!-- Edit/Clone Buttons positioned in bottom right -->
		<div class="action-buttons">
			<v-btn
					color="secondary"
					variant="flat"
					prepend-icon="mdi-content-copy"
					@click="openCloneDialog"
					>
					{{ $t('books.clone') }}
			</v-btn>
			<v-btn
					color="primary"
					variant="flat"
					prepend-icon="mdi-pencil"
					@click="openEditDialog"
					>
					{{ $t('books.edit') }}
			</v-btn>
		</div>

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
		<!-- Clone Dialog -->
		<v-dialog
				v-model="showCloneDialog"
				max-width="1200"
				persistent
				scrollable
				>
				<v-card>
					<v-card-title class="d-flex justify-space-between align-center">
						<span>{{ $t('books.clone') }}</span>
						<v-btn
								icon="mdi-close"
								variant="text"
								@click="closeCloneDialog"
								/>
					</v-card-title>
					<v-card-text class="pa-0">
						<AddBook
								:initial-book-data="cloneBookData"
								:force-add-mode="true"
								@book-added="onBookCloned"
								@cancel-edit="onCancelClone"
								/>
					</v-card-text>
				</v-card>
		</v-dialog>
		<v-dialog
				v-model="showDeleteDialog"
				max-width="520px"
				>
				<v-card>
					<v-card-title>{{ $t('books.deleteConfirmTitle') }}</v-card-title>
					<v-card-text>
						{{ $t('books.deleteConfirmText', { title: bookInfoData.title || '' }) }}
					</v-card-text>
					<v-card-actions class="justify-end">
						<v-btn
								variant="text"
								:disabled="deletingBook"
								@click="closeDeleteDialog"
								>
								{{ $t('books.cancel') }}
						</v-btn>
						<v-btn
								color="error"
								variant="elevated"
								:loading="deletingBook"
								:disabled="deletingBook"
								@click="confirmDeleteBook"
								>
								{{ $t('books.confirm') }}
						</v-btn>
					</v-card-actions>
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
  emits: ['book-updated', 'edit-cancelled', 'book-deleted', 'book-added'],
 
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
      showCloneDialog: false,
      showDeleteDialog: false,
      deletingBook: false,
      extractedBookData: null,
      cloneBookData: null,
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
      // console.log('Closing the Add Book Dialog');
      this.showEditDialog = false;
    },
    
    openEditDialog() {
      this.extractedBookData = null;
      this.showEditDialog = true;
    },

    openCloneDialog() {
      this.cloneBookData = this.fields?.originalData || null;
      this.showCloneDialog = true;
    },

    closeCloneDialog() {
      this.showCloneDialog = false;
    },

    
    openDeleteDialog() {
      this.showDeleteDialog = true;
    },

    closeDeleteDialog() {
      this.showDeleteDialog = false;
    },

    async confirmDeleteBook() {
      if (!this.bookId) {
        return;
      }

      this.deletingBook = true;

      try {
        await useAPI(`/books/${this.bookId}`, {
          method: 'DELETE'
        });
        this.showDeleteDialog = false;
        this.$emit('book-deleted', {
          bookId: Number(this.bookId)
        });
      } catch (error) {
        console.error('Failed to delete book:', error);
      } finally {
        this.deletingBook = false;
      }
    },

    onBookUpdated(updatedBookData) {
      this.showEditDialog = false;
      this.$emit('book-updated', updatedBookData);
    },

    onCancelEdit() {
      this.showEditDialog = false;
      this.$emit('edit-cancelled');
    },

    onBookCloned(bookData) {
      this.showCloneDialog = false;
      this.$emit('book-added', bookData);
    },

    onCancelClone() {
      this.showCloneDialog = false;
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

.action-buttons {
  position: absolute;
  bottom: 16px;
  right: 16px;
  z-index: 1;
  display: flex;
  gap: 8px;
}
</style>
