export const useBooks = () => {
  const loading = ref(false);
  const items = ref<Book[]>([]);
  const totalItems = ref(0);
  const searchParams = ref<SearchParams>({});
  
  // Options for data table
  const headers = [
    { title: 'Title', key: 'title', sortable: true },
    { title: 'Author(s)', key: 'authors', sortable: true },
    { title: 'Publisher', key: 'publisher', sortable: true },
    { title: 'Release Date', key: 'release_date', sortable: true },
    { title: 'Series', key: 'series_name', sortable: true },
  ];

  const fetchBooks = async (options: SearchParams) => {
    loading.value = true;
    
    try {
      // Build query parameters
      const queryParams = new URLSearchParams();
      
      if (options.title) queryParams.append('title', options.title);
      if (options.author) queryParams.append('author', options.author);
      if (options.publisher) queryParams.append('publisher', options.publisher);
      if (options.serie) queryParams.append('serie', options.serie);

		console.log( 'qqryq', queryParams.toString() )
      
      const { data, error } = await useAPI( `/book?${queryParams.toString()}` )

      if (error.value) {
        throw new Error(error.value.message);
      }

      if (data.value) {
        items.value = data.value.books;
        totalItems.value = data.value.count;
		  console.log( 'Items: ', items.value, ' total: ', totalItems.value )
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

