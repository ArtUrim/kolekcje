<template>
  <v-card elevation="1" class="pa-6 mb-4" rounded="lg">
    <div class="d-flex justify-space-between align-start">
      <div>
        <div class="book-title">{{ book.title || '' }}</div>
        <div v-if="book.originalTitle" class="original-title">{{book.originalTitle}}</div>
      </div>
      <v-btn
        icon="mdi-delete"
        color="error"
        variant="text"
        :aria-label="$t('books.delete')"
        @click="openDeleteDialog"
      />
    </div>

    <div class="mt-4">
      <v-chip v-for="author in displayAuthors" :key="author" color="primary" variant="flat" class="mr-2 mb-2">
        <v-icon start size="small">mdi-account</v-icon>
        {{ author }}
      </v-chip>
    </div>

    <div class="mt-2">
      <v-chip v-for="publisher in displayPublishers" :key="publisher" color="secondary" variant="flat" class="mr-2 mb-2">
        <v-icon start size="small">mdi-office-building</v-icon>
        {{ publisher }}
      </v-chip>
    </div>

    <div class="section-title">{{ $t('bookinfo.details') }}</div>
    <div class="meta-grid">
      <div class="meta-item">
        <div class="meta-label">{{ $t('bookinfo.releaseDate') }}</div>
        <div class="meta-value">{{ book.releaseDate || '' }}</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">{{ $t('bookinfo.firstPolishRelease') }}</div>
        <div class="meta-value">{{ book.firstPolishRelease || '' }}</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">{{ $t('bookinfo.pages') }}</div>
        <div class="meta-value">{{ book.pages || '' }}</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">{{ $t('bookinfo.isbn') }}</div>
        <div class="meta-value">{{ book.isbn || '' }}</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">{{ $t('bookinfo.format') }}</div>
        <div class="meta-value">{{ book.format ? $t('addBook.formats.' + book.format) : '' }}</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">{{ $t('bookinfo.size') }}</div>
        <div class="meta-value">{{ book.size ? $t('addBook.sizes.' + book.size) : '' }}</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">{{ $t('bookinfo.language') }}</div>
        <div class="meta-value">{{ book.language || '' }}</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">{{ $t('bookinfo.translator') }}</div>
        <div class="meta-value">{{ book.translator || '' }}</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">{{ $t('bookinfo.serie') }}</div>
        <div class="meta-value">{{ book.serie || '' }}</div>
      </div>
    </div>

    <div class="section-title">{{ $t('bookinfo.genres') }}</div>
    <div>
      <v-chip v-for="genre in book.genres" :key="genre" size="small" variant="outlined" color="teal" class="mr-2 mb-1">
        {{ genre }}
      </v-chip>
    </div>

    <div class="section-title">{{ $t('bookinfo.labels') }}</div>
    <div>
      <v-chip v-for="label in book.labels" :key="label" size="small" variant="tonal" color="purple" class="mr-2 mb-1">
        <v-icon start size="x-small">mdi-tag</v-icon>
        {{ label }}
      </v-chip>
    </div>

    <div class="section-title">{{ $t('bookinfo.description') }}</div>
    <p class="description-text">{{ book.description || '' }}</p>

    <div class="section-title">{{ $t('bookinfo.note') }}</div>
    <v-alert type="info" variant="tonal" density="compact" icon="mdi-note-text">
      {{ book.note || '' }}
    </v-alert>
  </v-card>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface BookInfoData {
  title: string;
  originalTitle: string;
  authors: string[];
  isbn: string;
  releaseDate: number | string;
  firstPolishRelease: number | string;
  format: string;
  pages: number | string;
  serie: string;
  size: string;
  language: string;
  translator: string;
  publishers: string[];
  genres: string[];
  labels: string[];
  description: string;
  note: string;
}

const props = withDefaults(
  defineProps<{ book?: Partial<BookInfoData> }>(),
  {
    book: () => ({}),
  }
);

const emit = defineEmits<{
  'delete-requested': [];
}>();

const openDeleteDialog = () => {
  emit('delete-requested');
};

const normalizedBook = computed<BookInfoData>(() => ({
  title: props.book.title ?? '',
  originalTitle: props.book.originalTitle ?? '',
  authors: props.book.authors ?? [],
  isbn: props.book.isbn ?? '',
  releaseDate: props.book.releaseDate ?? '',
  firstPolishRelease: props.book.firstPolishRelease ?? '',
  format: props.book.format ?? '',
  pages: props.book.pages ?? '',
  serie: props.book.serie ?? '',
  size: props.book.size ?? '',
  language: props.book.language ?? '',
  translator: props.book.translator ?? '',
  publishers: props.book.publishers ?? [],
  genres: props.book.genres ?? [],
  labels: props.book.labels ?? [],
  description: props.book.description ?? '',
  note: props.book.note ?? '',
}));

const book = normalizedBook;

const displayAuthors = computed(() => (book.value.authors.length ? book.value.authors : null));
const displayPublishers = computed(() => (book.value.publishers.length ?  book.value.publishers : null));
</script>

<style scoped>
.meta-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.meta-item {
  background: #f5f5f5;
  padding: 12px;
  border-radius: 8px;
}

.meta-label {
  font-size: 0.75rem;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.meta-value {
  font-size: 0.95rem;
  color: #333;
  margin-top: 4px;
}

.section-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: #555;
  margin: 20px 0 12px 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.book-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #222;
}

.original-title {
  font-size: 0.9rem;
  color: #888;
  font-style: italic;
  margin-top: 4px;
}

.description-text {
  color: #444;
  line-height: 1.7;
  font-size: 0.95rem;
}
</style>
