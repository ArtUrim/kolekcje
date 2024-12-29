interface Book {
  title: string;
  authors: string;
  publisher: string;
  release_date: string;
  series_name: string | null;
}

interface BookResponse {
  status: string;
  count: number;
  books: Book[];
}

interface SearchParams {
  title?: string;
  author?: string;
  publisher?: string;
  serie?: string;
  page?: number;
  itemsPerPage?: number;
  sortBy?: string[];
  sortDesc?: boolean[];
}
