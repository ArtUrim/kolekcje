export const useBooks = () => {
  const { t } = useI18n();
  const loading = ref(false);
  const items = ref<Book[]>([]);
  const totalItems = ref(0);
  const searchParams = ref<SearchParams>({});
  
  // Options for data table
  const headers = computed(() => [
    { title: t('books.headers.title'), key: 'title', sortable: true },
    { title: t('books.headers.authors'), key: 'authors', sortable: true },
    { title: t('books.headers.publisher'), key: 'publisher', sortable: true },
    { title: t('books.headers.releaseDate'), key: 'release_date', sortable: true },
    { title: t('books.headers.seriesName'), key: 'series_name', sortable: true },
    { title: t('books.headers.actions'), key: 'actions', sortable: false },
  ]);

  const fetchBooks = async (options: SearchParams) => {
    loading.value = true;
    
    try {
      // Build query parameters
      const queryParams = new URLSearchParams();
      
      if (options.title) queryParams.append('title', options.title);
      if (options.author) queryParams.append('author', options.author);
      if (options.publisher) queryParams.append('publisher', options.publisher);
      if (options.serie) queryParams.append('serie', options.serie);
		if (options.page) queryParams.append('page', options.page );
		if (options.itemsPerPage) queryParams.append('itemsPerPage', options.itemsPerPage );
	   if (options.sortBy !== undefined && options.sortBy.length) queryParams.append('sortBy', options.sortBy[0]['key'] );
	   if (options.sortBy !== undefined && options.sortBy.length) queryParams.append('sortDesc', options.sortBy[0]['order'] );
      
      const data = await useAPI<{ books: Book[]; count: number }>(`/book?${queryParams.toString()}`)

      if (data) {
        const uniqueBooks = data.books.filter((book, index, source) => {
          if (book?.id === undefined || book?.id === null) {
            return true;
          }

          return source.findIndex((candidate) => candidate?.id === book.id) === index;
        });

        items.value = uniqueBooks;
        totalItems.value = data.count;
      }
    } catch (err) {
      console.error('Error fetching books:', err);
      // Handle error appropriately
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
  };
};

