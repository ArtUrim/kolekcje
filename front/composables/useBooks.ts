// How often to retry a failed /book request.
const RETRY_INTERVAL_MS = 5000;
// Maximum time to keep retrying before giving up.
const MAX_RETRY_DURATION_MS = 10 * 60 * 1000;

export const useBooks = () => {
  const { t } = useI18n();
  const loading = ref(false);
  const items = ref<Book[]>([]);
  const totalItems = ref(0);
  const searchParams = ref<SearchParams>({});
  const isRetrying = ref(false);

  let retryTimeoutId: ReturnType<typeof setTimeout> | null = null;
  let retryStartedAt = 0;

  const stopRetrying = () => {
    if (retryTimeoutId) {
      clearTimeout(retryTimeoutId);
      retryTimeoutId = null;
    }
    retryStartedAt = 0;
    isRetrying.value = false;
  };

  const scheduleRetry = (options: SearchParams) => {
    if (!import.meta.client) {
      return;
    }

    if (!retryStartedAt) {
      retryStartedAt = Date.now();
    }

    if (Date.now() - retryStartedAt >= MAX_RETRY_DURATION_MS) {
      stopRetrying();
      return;
    }

    isRetrying.value = true;
    retryTimeoutId = setTimeout(() => {
      fetchBooks(options);
    }, RETRY_INTERVAL_MS);
  };

  onUnmounted(() => {
    stopRetrying();
  });
  
  // Options for data table
  const headers = computed(() => [
    { title: t('books.headers.title'), key: 'title', sortable: true },
    { title: t('books.headers.authors'), key: 'authors', sortable: true },
    { title: t('books.headers.publisher'), key: 'publisher', sortable: true },
    { title: t('books.headers.releaseDate'), key: 'release_date', sortable: true },
    { title: t('books.headers.seriesName'), key: 'series_name', sortable: true },
  ]);

  const fetchBooks = async (options: SearchParams) => {
    loading.value = true;
    
    try {
      // Build query parameters
      const queryParams = new URLSearchParams();

		// console.log( options );
      
      if (options.title) queryParams.append('title', options.title);
      if (options.author) queryParams.append('author', options.author);
      if (options.publisher) queryParams.append('publisher', options.publisher);
      if (options.serie) queryParams.append('serie', options.serie);
      if (options.isbn) queryParams.append('isbn', options.isbn);
      if (options.genres) queryParams.append('genres', options.genres);
      if (options.labels) queryParams.append('label', options.labels);
      if (options.release_date !== undefined && options.release_date !== '') {
        queryParams.append('release_date', options.release_date.toString());
      }
      if (options.first_polish_release_date !== undefined && options.first_polish_release_date !== '') {
        queryParams.append('first_polish_release_date', options.first_polish_release_date.toString());
      }
      if (options.format) queryParams.append('format', options.format);
      if (options.originalTitle) queryParams.append('original_title', options.originalTitle);
      if (options.translator) queryParams.append('translator', options.translator);
      if (options.language) queryParams.append('language', options.language);

      if (options.page) queryParams.append('page', options.page.toString());
      if (options.itemsPerPage) queryParams.append('itemsPerPage', options.itemsPerPage.toString());
      
      // Handle array-based sorting objects
      if (options.sortBy !== undefined && options.sortBy.length) {
        queryParams.append('sortBy', options.sortBy[0]['key']);
        queryParams.append('sortDesc', options.sortBy[0]['order']);
      }

      // Handle the fields parameter
      if (options.fields) {
        queryParams.append('fields', options.fields);
      }
      
      const data = await useAPI<{ books: Book[]; count: number }>(`/book?${queryParams.toString()}`);

      if (data) {
        // Safe deduplication, accounting for the possibility that 'id' was not requested
        const uniqueBooks = data.books.filter((book, index, source) => {
          if (book?.id === undefined || book?.id === null) {
            return true;
          }

          return source.findIndex((candidate) => candidate?.id === book.id) === index;
        });

        items.value = uniqueBooks;
        totalItems.value = data.count;
      }

      stopRetrying();
    } catch (err) {
      console.error('Error fetching books:', err);
      scheduleRetry(options);
    } finally {
      loading.value = false;
    }
  };

  return {
    items,
    loading,
    totalItems,
    headers,
    fetchBooks,
    searchParams,
    isRetrying,
  };
};
