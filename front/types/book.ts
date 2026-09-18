export interface Book {
  id?: number;
  isbn?: string | null;
  title?: string;
  subtitle?: string | null;
  release_date?: number | string | null;
  first_polish_release_date?: number | string | null;
  format?: 'unknown' | 'hardback' | 'paperback' | 'ebook' | 'jacket' | 'notebook';
  pages?: number | null;
  description?: string | null;
  note?: string | null;
  original_title?: string | null;
  translator?: string | null;
  language_id?: string;
  language?: string | null;
  size?: 'none' | 'mini' | 'normal' | 'scientific' | 'comics' | 'huge' | 'small' | 'unusual' | null;
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

export interface StatsBook {
  id: number;
  title: string;
}

export interface StatsItem {
  id?: string | number;
  name: string;
  count: number;
  books?: StatsBook[];
}

export interface SearchParams {
  title?: string;
  subtitle?: string;
  author?: string;
  publisher?: string;
  serie?: string;
  isbn?: string;
  genres?: string;
  label?: string;
  release_date?: string | number;
  first_polish_release_date?: string | number;
  format?: string;
  original_title?: string;
  translator?: string;
  language_id?: string;
  page?: number;
  itemsPerPage?: number;
  sortBy?: any[]; 
  sortDesc?: any[];
  fields?: string;
}