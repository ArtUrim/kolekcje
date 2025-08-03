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
      
      const { data, error } = await useAPI( `/book?${queryParams.toString()}` )

      if (error.value) {
        throw new Error(error.value.message);
      }

      if (data.value) {
        items.value = data.value.books;
        totalItems.value = data.value.count;
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

