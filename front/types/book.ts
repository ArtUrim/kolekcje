export interface Book {
  id?: number;
  isbn?: string | null;
  title?: string;
  release_date?: number | string | null;
  first_polish_release_date?: number | string | null;
  format?: 'unknown' | 'hardback' | 'paperback' | 'ebook';
  pages?: number | null;
  description?: string | null;
  note?: string | null;
  original_title?: string | null;
  translator?: string | null;
  language_id?: string;
  size?: 'none' | 'mini' | 'normal' | 'scientific' | 'comics' | 'huge' | null;
  authors?: string | null;
  publisher?: string | null;
  series_name?: string | null;
  genres?: string | null;
  labels?: string | null;
}

export interface BookResponse {
  status: string;
  count: number;
  books: Book[];
}

export interface SearchParams {
  title?: string;
  author?: string;
  publisher?: string;
  serie?: string;
  page?: number;
  itemsPerPage?: number;
  sortBy?: any[]; 
  sortDesc?: any[];
  fields?: string; // Added to support dynamic sparse fieldsets
}
