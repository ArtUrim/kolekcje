<template>
  <v-card>
    <v-card-title>
      Books Database
      <v-row>
        <v-col cols="3">
          <v-text-field
            v-model="searchParams.title"
            label="Search Title"
            clearable
            @update:model-value="handleSearch"
          />
        </v-col>
        <v-col cols="3">
          <v-text-field
            v-model="searchParams.author"
            label="Search Author"
            clearable
            @update:model-value="handleSearch"
          />
        </v-col>
        <v-col cols="3">
          <v-text-field
            v-model="searchParams.publisher"
            label="Search Publisher"
            clearable
            @update:model-value="handleSearch"
          />
        </v-col>
        <v-col cols="3">
          <v-text-field
            v-model="searchParams.serie"
            label="Search Series"
            clearable
            @update:model-value="handleSearch"
          />
        </v-col>
      </v-row>
    </v-card-title>

    <v-data-table-server
      v-model:items-per-page="itemsPerPage"
      v-model:page="page"
      v-model:sort-by="sortBy"
      v-model:sort-desc="sortDesc"
      :headers="headers"
      :items="items"
      :items-length="totalItems"
      :loading="loading"
      class="elevation-1"
      @update:options="handleOptionsUpdate"
    >
      <template #item.release_date="{ item }">
        {{ formatDate(item.release_date) }}
      </template>
      
      <template #item.series_name="{ item }">
        {{ item.series_name || 'N/A' }}
      </template>
      
      <template #no-data>
        No books found.
      </template>
    </v-data-table-server>
  </v-card>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import debounce from 'lodash/debounce';
import { useBooks } from '~/composables/useBooks';

const {
  items,
  loading,
  totalItems,
  headers,
  fetchBooks,
  searchParams,
} = useBooks();

const page = ref(1);
const itemsPerPage = ref(10);
const sortBy = ref<string[]>([]);
const sortDesc = ref<boolean[]>([]);

// Debounced search function
const handleSearch = debounce(() => {
  page.value = 1; // Reset to first page on new search
  fetchBooks({
    ...searchParams.value,
    page: page.value,
    itemsPerPage: itemsPerPage.value,
    sortBy: sortBy.value,
    sortDesc: sortDesc.value,
  });
}, 300);

// Handle data table options changes
const handleOptionsUpdate = (options: any) => {
  page.value = options.page;
  itemsPerPage.value = options.itemsPerPage;
  sortBy.value = options.sortBy;
  sortDesc.value = options.sortDesc;
  
  fetchBooks({
    ...searchParams.value,
    page: page.value,
    itemsPerPage: itemsPerPage.value,
    sortBy: sortBy.value,
    sortDesc: sortDesc.value,
  });
};

// Format date helper
const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString();
};

// Initial fetch
onMounted(() => {
  fetchBooks({
    page: page.value,
    itemsPerPage: itemsPerPage.value,
  });
});
</script>
