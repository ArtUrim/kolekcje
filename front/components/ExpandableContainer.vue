<template>
	<v-container fluid class="pa-6">
		<!-- Page Header    <v-row class="mb-6">
			<v-col cols="12">
			<h1 class="text-h3 text-center mb-4">Expandable Text Components</h1>
			<p class="text-h6 text-center text-medium-emphasis">
			Compare different Vuetify expandable text component variations
			</p>
			</v-col>
			</v-row>
		-->

		<!-- Custom Card Components with Transitions -->
		<v-row class="mb-2">
			<v-col v-for="(card, index) in processedCards"
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
    cards: {
      type: Array,
      required: true
    },
    longCards: {
      type: Array,
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
      extractedBookData: {}
    }
  },
  computed: {
    processedCards() {
    return this.cards.map(card => ({
    title: card.title || 'Untitled',
    headerColor: card.headerColor || 'lightblue',
    icon: card.icon || 'mdi-book-open-variant',
    shortText: card.shortText || card.description || `${card.authors || 'Unknown Author'} - ${card.genres || 'No genre specified'}`,
    expandedText: card.expandedText || '',
    tags: card.tags || [],
    progress: card.progress !== undefined ? card.progress : 100,
    expanded: card.expanded || false,
    ...card
    }))
    }
  },
  methods: {
    handleToggleExpanded(card) {
      card.expanded = !card.expanded
    },

    closeAddBookDialog() {
      console.log('Closing the Add Book Dialog');
      this.showEditDialog = false;
    },
    
    extractBookDataFromCards() {
      const bookData = {}
      
      // Extract data from cards
      this.processedCards.forEach(card => {
        const shortText = card.shortText
        if (shortText && shortText !== 'N/A' && shortText.trim() !== '') {
          switch(card.title) {
            case 'Tytuł':
            case 'Title':
              bookData.title = shortText
              break
            case 'Autor':
            case 'Author':
              // Convert comma-separated string to array format expected by AddBook
              if (shortText.includes(',')) {
                bookData.author = shortText.split(',').map(author => ({
                  title: author.trim(),
                  isCustom: true
                }))
              } else {
                bookData.author = [{
                  title: shortText.trim(),
                  isCustom: true
                }]
              }
              break
            case 'Wydawca':
            case 'Publisher':
              bookData.publisher = [{
                title: shortText,
                isCustom: true
              }]
              break
            case 'Seria':
            case 'Series':
              bookData.series = {
                title: shortText,
                isCustom: true
              }
              break
            case 'Gatunek':
            case 'Genre':
              if (shortText.includes(',')) {
                bookData.genre = shortText.split(',').map(genre => ({
                  title: genre.trim(),
                  isCustom: true
                }))
              } else {
                bookData.genre = [{
                  title: shortText.trim(),
                  isCustom: true
                }]
              }
              break
            case 'Etykieta':
            case 'Label':
              if (shortText.includes(',')) {
                bookData.label = shortText.split(',').map(label => ({
                  title: label.trim(),
                  isCustom: true
                }))
              } else {
                bookData.label = [{
                  title: shortText.trim(),
                  isCustom: true
                }]
              }
              break
            case 'Format':
              bookData.format = shortText
              break
            case 'Rozmiar':
            case 'Size':
              bookData.booksize = shortText
              break
            case 'ISBN':
              bookData.isbn = shortText
              break
            case 'Strony':
            case 'Pages':
              bookData.pages = parseInt(shortText) || ''
              break
            case 'Rok wydania':
            case 'Publish Year':
              bookData.publishYear = parseInt(shortText) || ''
              break
            case 'Pierwsze polskie wydanie':
            case 'First Publish Year':
              bookData.firstPublishYear = parseInt(shortText) || ''
              break
            case 'Język':
            case 'Language':
              bookData.language = shortText
              break
            case 'Tytuł oryginalny':
            case 'Original Title':
              bookData.originalTitle = shortText
              break
            case 'Tłumacz':
            case 'Translator':
              bookData.translator = shortText
              break
          }
        }
      })
      
      // Extract data from longCards
      this.longCards.forEach(card => {
        const shortText = card.shortText
        const expandedText = card.expandedText
        
        if ((shortText && shortText !== 'N/A' && shortText !== 'Brak opisu' && shortText !== 'Brak notatek' && shortText.trim() !== '') ||
            (expandedText && expandedText !== 'Brak szczegółowego opisu książki.' && expandedText !== 'Brak dodatkowych notatek.' && expandedText.trim() !== '')) {
          switch(card.title) {
            case 'Opis':
            case 'Description':
              bookData.description = expandedText || shortText
              break
            case 'Notatki':
            case 'Notes':
              bookData.notes = expandedText || shortText
              break
          }
        }
      })
      
      return bookData
    },
    
    openEditDialog() {
      this.extractedBookData = this.extractBookDataFromCards()
      console.log( 'ExtractBookData', this.extractedBookData)
      this.showEditDialog = true
    },
    
    onBookUpdated(updatedBookData) {
      this.showEditDialog = false
      this.$emit('book-updated', updatedBookData)
    },

    onCancelEdit() {
      this.showEditDialog = false
      this.$emit('edit-cancelled')
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
