<template>
  <v-app>
    <v-main class="pa-6 app-background">
      <v-card elevation="1" class="pa-6" rounded="lg">
        <div class="book-title">{{ book.title }}</div>
        <div class="original-title">{{ book.originalTitle }}</div>

        <div class="mt-4">
          <v-chip v-for="author in book.authors" :key="author" color="primary" variant="flat" class="mr-2">
            <v-icon start size="small">mdi-account</v-icon>
            {{ author }}
          </v-chip>
        </div>

        <div class="mt-4">
          <v-chip v-for="publisher in book.publishers" :key="publisher" color="secondary" variant="flat" class="mr-2">
            <v-icon start size="small">mdi-office-building</v-icon>
            {{ publisher }}
          </v-chip>
        </div>

        <div class="section-title">Szczegóły</div>
        <div class="meta-grid">
          <div class="meta-item">
            <div class="meta-label">Rok wydania</div>
            <div class="meta-value">{{ book.releaseDate }}</div>
          </div>
          <div class="meta-item">
            <div class="meta-label">Wydanie PL</div>
            <div class="meta-value">{{ book.firstPolishRelease }}</div>
          </div>
          <div class="meta-item">
            <div class="meta-label">Strony</div>
            <div class="meta-value">{{ book.pages }}</div>
          </div>
          <div class="meta-item">
            <div class="meta-label">ISBN</div>
            <div class="meta-value">{{ book.isbn }}</div>
          </div>
          <div class="meta-item">
            <div class="meta-label">Format</div>
            <div class="meta-value">{{ book.format }}</div>
          </div>
          <div class="meta-item">
            <div class="meta-label">Rozmiar</div>
            <div class="meta-value">{{ book.size }}</div>
          </div>
          <div class="meta-item">
            <div class="meta-label">Język</div>
            <div class="meta-value">{{ book.language }}</div>
          </div>
          <div class="meta-item">
            <div class="meta-label">Tłumacz</div>
            <div class="meta-value">{{ book.translator }}</div>
          </div>
          <div class="meta-item">
            <div class="meta-label">Wydawca</div>
            <div class="meta-value">{{ book.publishers[0] }}</div>
          </div>
          <div class="meta-item">
            <div class="meta-label">Seria</div>
            <div class="meta-value">{{ book.serie }}</div>
          </div>
        </div>

        <div class="section-title">Gatunki</div>
        <div>
          <v-chip v-for="genre in book.genres" :key="genre" size="small" variant="outlined" color="teal" class="mr-2 mb-1">
            {{ genre }}
          </v-chip>
        </div>

        <div class="section-title">Etykiety</div>
        <div>
          <v-chip v-for="label in book.labels" :key="label" size="small" variant="tonal" color="purple" class="mr-2 mb-1">
            <v-icon start size="x-small">mdi-tag</v-icon>
            {{ label }}
          </v-chip>
        </div>

        <div class="section-title">Opis</div>
        <p class="description-text">{{ book.description }}</p>

        <div class="section-title">Notatka</div>
        <v-alert type="info" variant="tonal" density="compact" icon="mdi-note-text">
          {{ book.note }}
        </v-alert>
      </v-card>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref } from 'vue';

// Definiowanie interfejsu dla lepszego typowania w TypeScript
interface Book {
  title: string;
  originalTitle: string;
  authors: string[];
  isbn: string;
  releaseDate: number;
  firstPolishRelease: number;
  format: string;
  pages: number;
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

const activeTab = ref<string>('info');

const book = ref<Book>({
  title: 'Władca Pierścieni: Drużyna Pierścienia',
  originalTitle: 'The Lord of the Rings: The Fellowship of the Ring',
  authors: ['J.R.R. Tolkien'],
  isbn: '9788324154791',
  releaseDate: 1954,
  firstPolishRelease: 1961,
  format: 'hardback',
  pages: 576,
  serie: "qqryq",
  size: 'normal',
  language: 'pol',
  translator: 'Maria Skibniewska',
  publishers: ['Wydawnictwo Amber'],
  genres: ['Fantasy', 'Przygodowa', 'Epika'],
  labels: ['klasyka', 'do przeczytania', 'ulubione'],
  description: 'Pierwsza część trylogii Władca Pierścieni. Frodo Baggins, młody hobbit, dziedziczy po swoim wuju Bilbie tajemniczy pierścień. Okazuje się, że jest to Jedyny Pierścień, wykuty przez Mrocznego Władcę Saurona...',
  note: 'Wydanie ilustrowane przez Alana Lee. Kupione na targach książki 2023.'
});
</script>

<style scoped>
.app-background {
  background: #fafafa;
}

.mockup-title {
  font-size: 1.1rem;
  font-weight: 500;
  color: #666;
  margin-bottom: 16px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

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

.info-row {
  display: flex;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.info-label {
  width: 140px;
  color: #888;
  font-size: 0.85rem;
}

.info-value {
  flex: 1;
  color: #333;
  font-size: 0.95rem;
}
</style>
