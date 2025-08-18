<template>
  <v-card>
    <v-card-title>
		 {{ $t('books.db') }}
      <v-row>
        <v-col cols="3">
          <v-text-field
            v-model="searchParams.title"
            :label="$t('books.searchTitle')"
            clearable
            @update:model-value="handleSearch"
          />
        </v-col>
        <v-col cols="3">
          <v-text-field
            v-model="searchParams.author"
            :label="$t('books.searchAuthor')"
            clearable
            @update:model-value="handleSearch"
          />
        </v-col>
        <v-col cols="3">
          <v-text-field
            v-model="searchParams.publisher"
            :label="$t('books.searchPublisher')"
            clearable
            @update:model-value="handleSearch"
          />
        </v-col>
        <v-col cols="3">
          <v-text-field
            v-model="searchParams.serie"
            :label="$t('books.searchSeries')"
            clearable
            @update:model-value="handleSearch"
          />
        </v-col>
      </v-row>
    </v-card-title>

    <v-data-table-server
      v-model:items-per-page="itemsPerPage"
      v-model:page="page"
      v-model:sort-by="sortBy"
      v-model:sort-desc="sortDesc"
      :headers="headers"
      :items="items"
      :items-length="totalItems"
      :loading="loading"
      show-expand
      class="elevation-1"
      @update:options="handleOptionsUpdate"
    >
      <template #item.data-table-expand="{ internalItem, isExpanded, toggleExpand }">
        <v-btn
          :append-icon="isExpanded(internalItem) ? 'mdi-chevron-up' : 'mdi-chevron-down'"
          :text="isExpanded(internalItem) ? 'Collapse' : 'Details'"
          class="text-none"
          color="primary"
          size="small"
          variant="outlined"
          @click="handleExpandToggle(internalItem, toggleExpand)"
        />
      </template>

      <template #expanded-row="{ columns, item }">
        <tr>
          <td :colspan="columns.length" class="pa-4">
            <v-card flat>
              <v-card-text>
                <!-- Loading state -->
                <div v-if="loadingDetails[item.id]" class="text-center py-4">
                  <v-progress-circular indeterminate color="primary" />
                  <p class="mt-2">Loading book details...</p>
                </div>

                <!-- Book details using ExpandableContainer -->
                <div v-else-if="bookDetails[item.id]">
                  <ExpandableContainer
                    :cards="bookDetails[item.id].cards"
                    :long-cards="bookDetails[item.id].longCards"
                    />
                </div>

                <!-- Error state -->
                <div v-else-if="detailsErrors[item.id]" class="text-center py-4">
                  <v-icon color="error" size="48">mdi-alert-circle</v-icon>
                  <p class="mt-2 text-error">Failed to load book details</p>
                  <v-btn
                    color="primary"
                    variant="outlined"
                    @click="fetchBookDetails(item.id)"
                  >
                    Retry
                  </v-btn>
                </div>
              </v-card-text>
            </v-card>
          </td>
        </tr>
      </template>
      <template #item.release_date="{ item }">
        {{ item.release_date }}
      </template>
      
      <template #item.series_name="{ item }">
        {{ item.series_name || 'N/A' }}
      </template>
      
      <template #no-data>
		  {{ $t('books.nobooks') }}
      </template>
    </v-data-table-server>
  </v-card>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import debounce from 'lodash/debounce';
import { useBooks } from '~/composables/useBooks';

const { t } = useI18n();

const {
  items,
  loading,
  totalItems,
  headers,
  fetchBooks,
  searchParams,
} = useBooks();

const page = ref(1);
const itemsPerPage = ref(10);
const sortBy = ref<string[]>([]);
const sortDesc = ref<boolean[]>([]);

// Debounced search function
const handleSearch = debounce(() => {
  page.value = 1; // Reset to first page on new search
  fetchBooks({
    ...searchParams.value,
    page: page.value,
    itemsPerPage: itemsPerPage.value,
    sortBy: sortBy.value,
    sortDesc: sortDesc.value,
  });
}, 300);

// Handle data table options changes
const bookDetails = ref<Record<number, any>>({});
const loadingDetails = ref<Record<number, boolean>>({});
const detailsErrors = ref<Record<number, boolean>>({});

const transformBookDataToCards = (bookData: any) => {
  const book = bookData.book;

  return [
    // Row 1: Title, Author, Publisher
    {
      title: t('addBook.title'),
      headerColor: 'blue-grey-darken-2',
      icon: 'mdi-book',
      shortText: book.title || 'N/A',
      expandedText: '',
      tags: [],
      progress: 100,
      expanded: false
    },
    {
      title: t('addBook.author'),
      headerColor: 'blue-grey-darken-2',
      icon: 'mdi-book',
      shortText: book.authors || 'N/A',
      expandedText: '',
      tags: [],
      progress: 100,
      expanded: false
    },
    {
      title: t('addBook.publisher'), // Use t() function
      headerColor: 'blue-grey-darken-2',
      icon: 'mdi-domain',
      shortText: book.publishers || 'N/A',
      expandedText: book.publishers_details?.map(pub => 
        `${pub.name}${pub.webpage ? ` (${pub.webpage})` : ''}`
      ).join(', ') || '',
      tags: [],
      progress: 100,
      expanded: false
    },
    {
      title: t('addBook.series'), // Use t() function
      headerColor: 'blue-grey-darken-2',
      icon: 'mdi-book-multiple',
      shortText: book.series_name || 'N/A',
      expandedText: '',
      tags: book.series_id ? [`ID: ${book.series_id}`] : [],
      progress: 100,
      expanded: false
    },
    {
      title: t('addBook.genre'), // Use t() function
      headerColor: 'blue-grey-darken-1',
      icon: 'mdi-tag-multiple',
      shortText: book.genres || 'N/A',
      expandedText: book.genres_details?.map(genre => genre.name).join(', ') || '',
      tags: book.genres_details?.map(genre => `#${genre.name}`) || [],
      progress: 100,
      expanded: false
    },
    {
      title: t('addBook.etykieta'), // Use t() function
      headerColor: 'blue-grey-darken-1',
      icon: 'mdi-label',
      shortText: book.labels || 'N/A',
      expandedText: book.labels_details?.map(label => label.name).join(', ') || '',
      tags: book.labels_details?.map(label => `#${label.name}`) || [],
      progress: 100,
      expanded: false
    },
    {
      title: t('addBook.format'), // Use t() function
      headerColor: 'blue-grey-darken-1',
      icon: 'mdi-book-variant',
      shortText: book.format || 'N/A',
      expandedText: '',
      tags: [book.format].filter(Boolean),
      progress: 100,
      expanded: false
    },
    {
      title: t('addBook.size'), // Add this to i18n if needed
      headerColor: 'blue-grey-darken-1',
      icon: 'mdi-ruler',
      shortText: book.size || 'N/A',
      expandedText: '',
      tags: [],
      progress: 100,
      expanded: false
    },
    {
      title: 'ISBN', // This one doesn't need translation
      headerColor: 'blue-grey',
      icon: 'mdi-barcode',
      shortText: book.isbn || 'N/A',
      expandedText: '',
      tags: [],
      progress: 100,
      expanded: false
    },
    {
      title: t('addBook.pages'), // Use t() function
      headerColor: 'blue-grey',
      icon: 'mdi-file-document',
      shortText: book.pages?.toString() || 'N/A',
      expandedText: '',
      tags: [],
      progress: book.pages ? Math.min((book.pages / 500) * 100, 100) : 0,
      expanded: false
    },
    {
      title: t('addBook.publishYear'), // Use t() function
      headerColor: 'blue-grey',
      icon: 'mdi-calendar',
      shortText: book.release_date?.toString() || 'N/A',
      expandedText: '',
      tags: [],
      progress: 100,
      expanded: false
    },
    {
      title: t('addBook.firstPublishYear'), // Use t() function
      headerColor: 'blue-grey',
      icon: 'mdi-calendar-star',
      shortText: book.first_polish_release_date?.toString() || 'N/A',
      expandedText: 'Pierwsze polskie wydanie',
      tags: [],
      progress: 100,
      expanded: false
    },
    {
      title: t('addBook.language'), // Use t() function
      headerColor: 'blue-grey-lighten-1',
      icon: 'mdi-translate',
      shortText: book.language_name || 'N/A',
      expandedText: `Kod języka: ${book.language_id || 'N/A'}`,
      tags: book.language_id ? [book.language_id] : [],
      progress: 100,
      expanded: false
    },
    {
      title: t('addBook.originalTitle'), // Use t() function
      headerColor: 'blue-grey-lighten-1',
      icon: 'mdi-book-open-variant',
      shortText: book.original_title || 'N/A',
      expandedText: '',
      tags: [],
      progress: 100,
      expanded: false
    },
    {
      title: t('addBook.translator'), // Use t() function
      headerColor: 'blue-grey-lighten-1',
      icon: 'mdi-account-convert',
      shortText: book.translator || 'N/A',
      expandedText: '',
      tags: [],
      progress: 100,
      expanded: false
    }
  ];
};


const transformBookDataToBigCards = (bookData: any) => {
  const book = bookData.book;

  return [
    {
      title: t('addBook.description'), // Use t() function
      headerColor: 'grey-darken-1',
      icon: 'mdi-text-long',
      shortText: book.description ? 
        (book.description.length > 100 ? book.description.substring(0, 100) + '...' : book.description) : 
        'Brak opisu',
      expandedText: book.description || 'Brak szczegółowego opisu książki.',
      tags: [],
      progress: book.description ? 100 : 0,
      expanded: false
    },
    {
      title: t('addBook.notes'), // Use t() function
      headerColor: 'grey',
      icon: 'mdi-note-text',
      shortText: book.note ? 
        (book.note.length > 100 ? book.note.substring(0, 100) + '...' : book.note) : 
        'Brak notatek',
      expandedText: book.note || 'Brak dodatkowych notatek.',
      tags: [],
      progress: book.note ? 100 : 0,
      expanded: false
    }
  ];
};

const fetchBookDetails = async (bookId: number) => {
  if (bookDetails.value[bookId]) {
    return; // Already loaded
  }

  loadingDetails.value[bookId] = true;
  detailsErrors.value[bookId] = false;

  try {
    const { data, error } = await useAPI(`/bookinfo?id=${bookId}`);
    if (error.value) {
      throw new Error('Error fetching book details');
    }

    const transformedCards = transformBookDataToCards(data.value);
    const transformedBigCards = transformBookDataToBigCards(data.value);
    bookDetails.value[bookId] = {
      originalData: data.value,
      cards: transformedCards,
      longCards: transformedBigCards
    };
  } catch (error) {
    console.error('Failed to fetch book details:', error);
    detailsErrors.value[bookId] = true;
  } finally {
    loadingDetails.value[bookId] = false;
  }
};

const handleExpandToggle = async (internalItem: any, toggleExpand: Function) => {
  const bookId = internalItem.value;

  if (!bookDetails.value[bookId] && !loadingDetails.value[bookId]) {
    await fetchBookDetails(bookId);
  }

  toggleExpand(internalItem);
};

const handleOptionsUpdate = (options: any) => {
  page.value = options.page;
  itemsPerPage.value = options.itemsPerPage;
  sortBy.value = options.sortBy;
  sortDesc.value = options.sortDesc;
  
  fetchBooks({
    ...searchParams.value,
    page: page.value,
    itemsPerPage: itemsPerPage.value,
    sortBy: sortBy.value,
    sortDesc: sortDesc.value,
  });
};

// Initial fetch
onMounted(() => {
  fetchBooks({
 	page: page.value,
 	itemsPerPage: itemsPerPage.value,
  });
});
</script>

<style scoped>
.book-details .v-card {
  min-height: 80px;
}

.book-details .v-card-subtitle {
  font-weight: 600;
  color: rgba(0, 0, 0, 0.6);
  padding-bottom: 4px;
}

.book-details .v-card-text {
  padding-top: 8px;
  font-size: 0.9rem;
}
</style>
