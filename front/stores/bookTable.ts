// stores/bookTable.ts
// Pinia store that controls which columns are visible in the book table
// and which fields are used as search/filter inputs (max 4).
// Works correctly after `nuxt build --prerender` when pinia-plugin-persistedstate is installed.

import { defineStore } from 'pinia'

// ---------------------------------------------------------------------------
// Column / field metadata
// ---------------------------------------------------------------------------

export interface BookColumnDef {
  key: string
  titleI18n: string   // i18n key resolved at component level with $t() / t()
  sortable: boolean
  align: 'start' | 'center' | 'end'
}

/** All columns that CAN appear in the table (derived from KatalogMariaDB.sql). */
export const ALL_BOOK_COLUMNS: BookColumnDef[] = [
  { key: 'title',                     titleI18n: 'books.colTitle',              sortable: true,  align: 'start'  },
  { key: 'author',                    titleI18n: 'books.colAuthor',             sortable: true,  align: 'start'  },
  { key: 'release_date',              titleI18n: 'books.colYear',               sortable: true,  align: 'center' },
  { key: 'first_polish_release_date', titleI18n: 'books.colFirstPolishYear',    sortable: true,  align: 'center' },
  { key: 'series_name',               titleI18n: 'books.colSeries',             sortable: true,  align: 'start'  },
  { key: 'publisher',                 titleI18n: 'books.colPublisher',          sortable: true,  align: 'start'  },
  { key: 'format',                    titleI18n: 'books.colFormat',             sortable: true,  align: 'center' },
  { key: 'pages',                     titleI18n: 'books.colPages',              sortable: true,  align: 'center' },
  { key: 'isbn',                      titleI18n: 'books.colIsbn',               sortable: false, align: 'start'  },
  { key: 'original_title',            titleI18n: 'books.colOriginalTitle',      sortable: true,  align: 'start'  },
  { key: 'translator',                titleI18n: 'books.colTranslator',         sortable: true,  align: 'start'  },
  { key: 'language',                  titleI18n: 'books.colLanguage',           sortable: true,  align: 'center' },
  { key: 'size',                      titleI18n: 'books.colSize',               sortable: true,  align: 'center' },
  { key: 'genres',                    titleI18n: 'books.colGenres',             sortable: false, align: 'start'  },
  { key: 'labels',                    titleI18n: 'books.colLabels',             sortable: false, align: 'start'  },
]

/**
 * Subset of column keys that make sense as free-text search inputs.
 * These are the only columns that appear in BookFilterSelector.
 */
export const FILTERABLE_KEYS: string[] = [
  'title', 'author', 'publisher', 'series_name',
  'isbn', 'original_title', 'translator',
  'genres', 'labels', 'language',
]

/**
 * Maps a column key → the corresponding key in `searchParams`
 * (returned by the useBooks() composable).
 */
export const COLUMN_TO_SEARCH_KEY: Record<string, string> = {
  title:         'title',
  author:        'author',
  publisher:     'publisher',
  series_name:   'serie',
  isbn:          'isbn',
  original_title:'originalTitle',
  translator:    'translator',
  genres:        'genres',
  labels:        'labels',
  language:      'language',
}

// ---------------------------------------------------------------------------
// Preset definitions
// ---------------------------------------------------------------------------

export interface BookPreset {
  id: string
  labelI18n: string
  columns: string[]
  filterFields: string[]
}

export const DEFAULT_PRESETS: BookPreset[] = [
  {
    id: 'standard',
    labelI18n: 'books.presetStandard',
    columns: ['title', 'author', 'release_date', 'series_name'],
    filterFields: ['title', 'author', 'publisher', 'series_name'],
  },
  {
    id: 'publishing',
    labelI18n: 'books.presetPublishing',
    columns: ['title', 'author', 'release_date', 'publisher'],
    filterFields: ['title', 'author', 'publisher', 'series_name'],
  },
  {
    id: 'edition',
    labelI18n: 'books.presetEdition',
    columns: ['title', 'isbn', 'format', 'pages'],
    filterFields: ['title', 'isbn', 'original_title', 'translator'],
  },
  {
    id: 'full',
    labelI18n: 'books.presetFull',
    columns: ['title', 'author', 'release_date', 'series_name', 'publisher', 'format'],
    filterFields: ['title', 'author', 'publisher', 'series_name'],
  },
]

// ---------------------------------------------------------------------------
// Store
// ---------------------------------------------------------------------------

export const useBookTableStore = defineStore(
  'bookTable',
  () => {
    const activePresetId = ref<string>('standard')
    const isCustom       = ref<boolean>(false)
    const customColumns  = ref<string[]>([])
    const customFilters  = ref<string[]>([])

    /** Always the full preset list (currently read-only, can be extended). */
    const presets = readonly(DEFAULT_PRESETS)

    const activePreset = computed<BookPreset>(
      () => presets.find(p => p.id === activePresetId.value) ?? presets[0]
    )

    /** Currently visible column keys. */
    const activeColumns = computed<string[]>(() =>
      isCustom.value ? customColumns.value : activePreset.value.columns
    )

    /** Currently active filter-field keys (max 4, always ⊆ activeColumns ∩ FILTERABLE_KEYS). */
    const activeFilterFields = computed<string[]>(() =>
      isCustom.value ? customFilters.value : activePreset.value.filterFields
    )

    /**
     * Raw column definitions for the active columns, in schema order.
     * Translate `titleI18n` in the component with `t(col.titleI18n)`.
     */
    const activeColumnDefs = computed<BookColumnDef[]>(() =>
      ALL_BOOK_COLUMNS.filter(c => activeColumns.value.includes(c.key))
    )

    // -----------------------------------------------------------------------
    // Actions
    // -----------------------------------------------------------------------

    function applyPreset(presetId: string) {
      activePresetId.value = presetId
      isCustom.value = false
    }

    /**
     * Store a custom column + filter selection.
     * filterFields is automatically capped at 4 and trimmed to FILTERABLE_KEYS ∩ columns.
     */
    function applyCustom(columns: string[], filterFields: string[]) {
      customColumns.value = [...columns]
      customFilters.value = filterFields
        .filter(f => columns.includes(f) && FILTERABLE_KEYS.includes(f))
        .slice(0, 4)
      isCustom.value = true
      activePresetId.value = ''
    }

    return {
      presets,
      activePresetId,
      isCustom,
      activePreset,
      activeColumns,
      activeFilterFields,
      activeColumnDefs,
      applyPreset,
      applyCustom,
    }
  },
  { persist: true },
)
