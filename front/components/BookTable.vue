<template>
	<v-card style="position: relative;">
		<v-overlay
				:model-value="isRetrying"
				contained
				persistent
				scrim="background"
				content-class="d-flex align-center justify-center w-100 h-100"
				>
				<div class="text-center">
					<span class="hourglass-icon" aria-hidden="true">⏳</span>
					<p class="mt-2">{{ $t('books.retrying') }}</p>
				</div>
		</v-overlay>
		<v-card-title class="d-flex justify-space-between align-center">
			<v-row>
				<v-col cols="9" sm="6" md="4">
					<span>{{ $t('books.db') }}</span>
				</v-col>
				<v-col cols="3" sm="6" md="4">
					<v-btn
							color="primary"
							variant="elevated"
							prepend-icon="mdi-plus"
							@click="showAddBookDialog = true"
							>
							{{ $t('books.new') }}
					</v-btn>
				</v-col>
			</v-row>
		</v-card-title>
		<v-row>
			<v-col cols="3">
				<v-text-field
						v-model="searchParams.title"
						:label="$t('books.searchTitle')"
						clearable
						@update:model-value="handleSearch"
						/>
			</v-col>
			<v-col cols="3">
				<v-text-field
						v-model="searchParams.author"
						:label="$t('books.searchAuthor')"
						clearable
						@update:model-value="handleSearch"
						/>
			</v-col>
			<v-col cols="3">
				<v-text-field
						v-model="searchParams.publisher"
						:label="$t('books.searchPublisher')"
						clearable
						@update:model-value="handleSearch"
						/>
			</v-col>
			<v-col cols="3">
				<v-text-field
						v-model="searchParams.serie"
						:label="$t('books.searchSeries')"
						clearable
						@update:model-value="handleSearch"
						/>
			</v-col>
		</v-row>

		<v-data-table-server
				v-model:items-per-page="itemsPerPage"
				v-model:page="page"
				v-model:sort-by="sortBy"
				v-model:sort-desc="sortDesc"
				:headers="headers"
				:items="items"
				:items-length="totalItems"
				:loading="loading"
				show-expand
				class="elevation-1"
				@update:options="handleOptionsUpdate"
				>
				<template #item.data-table-expand="{ internalItem, isExpanded, toggleExpand }">
					<v-btn
							:append-icon="isExpanded(internalItem) ? 'mdi-chevron-up' : 'mdi-chevron-down'"
							:text="isExpanded(internalItem) ? $t('bookinfo.collapse') : $t('bookinfo.details')"
							class="text-none"
							color="primary"
							size="small"
							variant="outlined"
							@click="handleExpandToggle(internalItem, toggleExpand)"
							/>
				</template>

			<template #expanded-row="{ columns, item }">
				<tr>
					<td :colspan="columns.length" class="pa-4">
						<v-card flat>
							<v-card-text>
								<!-- Loading state -->
								<div v-if="loadingDetails[item.id]" class="text-center py-4">
									<v-progress-circular indeterminate color="primary" />
										<p class="mt-2">Loading book details...</p>
								</div>

								<!-- Book details using ExpandableContainer -->
								<div v-else-if="bookDetails[item.id]">
									<ExpandableContainer
											:fields="bookDetails[item.id]"
											:book-id="String(item.id)"
											@book-updated="handleBookUpdated"
											@book-deleted="handleBookDeleted"
											@edit-cancelled="handleEditCancelled"
											@book-added="handleBookAdded"
											/>
								</div>

								<!-- Error state -->
								<div v-else-if="detailsErrors[item.id]" class="text-center py-4">
									<v-icon color="error" size="48">mdi-alert-circle</v-icon>
									<p class="mt-2 text-error">Failed to load book details</p>
									<v-btn
											color="primary"
											variant="outlined"
											@click="fetchBookDetails(item.id)"
											>
											Retry
									</v-btn>
								</div>
							</v-card-text>
						</v-card>
					</td>
				</tr>
			</template>
			<template #item.release_date="{ item }">
				{{ item.release_date }}
			</template>

			<template #item.series_name="{ item }">
				{{ item.series_name || 'N/A' }}
			</template>

			<template #no-data>
				{{ $t('books.nobooks') }}
			</template>
		</v-data-table-server>
		<v-dialog
				v-model="showAddBookDialog"
				max-width="1200px"
				persistent
				scrollable
				>
				<v-card>
					<v-card-title class="d-flex justify-space-between align-center">
						<span>{{ $t('books.edit') }}</span>
						<v-btn
								icon="mdi-close"
								variant="text"
								@click="closeAddBookDialog"
								/>
					</v-card-title>
					<v-card-text class="pa-0">
						<AddBook @book-added="handleBookAdded" />
					</v-card-text>
				</v-card>
		</v-dialog>
	</v-card>
</template>

<script setup lang="ts">
	import { ref, watch } from 'vue';
import debounce from 'lodash/debounce';
import { useBooks } from '~/composables/useBooks';
import { useBookFormat } from '~/composables/bookFormat';

const emit = defineEmits<{
  'book-updated': (bookData: any) => void;
  'edit-cancelled': () => void;
}>();

const { t } = useI18n();

const {
  items,
  loading,
  totalItems,
  headers,
  fetchBooks,
  searchParams,
  isRetrying,
} = useBooks();

const { transformBookDataToCards, transformBookDataToBigCards } = useBookFormat();

const { userRole } =  useNetworkAdmin();

const showAddBookDialog = ref(false);
const page = ref(1);

const closeAddBookDialog = () => {
  showAddBookDialog.value = false;
};

const handleBookAdded = () => {
  showAddBookDialog.value = false;
  fetchBooks({
	 ...searchParams.value,
	 page: page.value,
	 itemsPerPage: itemsPerPage.value,
	 sortBy: sortBy.value,
	 sortDesc: sortDesc.value,
  });
};

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
const bookDetails = ref<Record<number, any>>({});
const loadingDetails = ref<Record<number, boolean>>({});
const detailsErrors = ref<Record<number, boolean>>({});

const fetchBookDetails = async (bookId: number, forceRefresh = false) => {
  if (bookDetails.value[bookId] && !forceRefresh) {
	 return; // Already loaded
  }

  loadingDetails.value[bookId] = true;
  detailsErrors.value[bookId] = false;

  try {
	 const data = await useAPI(`/bookinfo?id=${bookId}`);
	 const bookPayload = data?.book || data;

	 // Create deep copy of the data and transform it using bookFormat composable
	 const bookDataCopy = JSON.parse(JSON.stringify(bookPayload));
	 const transformedCards = transformBookDataToCards(bookDataCopy);
	 const transformedBigCards = transformBookDataToBigCards(bookDataCopy);

	 // Store as fields object for ExpandableContainer
	 bookDetails.value[bookId] = {
		originalData: bookDataCopy,
		cards: transformedCards,
		longCards: transformedBigCards
	 };
  } catch (error) {
	 console.error('Failed to fetch book details:', error);
	 detailsErrors.value[bookId] = true;
  } finally {
	 loadingDetails.value[bookId] = false;
  }
};

const handleExpandToggle = async (internalItem: any, toggleExpand: Function) => {
  const bookId = internalItem.value;

  if (!bookDetails.value[bookId] && !loadingDetails.value[bookId]) {
	 await fetchBookDetails(bookId);
  }

  toggleExpand(internalItem);
};

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

const handleBookUpdated = async (updatedBookData: any) => {
  const bookId = Number(updatedBookData?.bookId);

  if (Number.isFinite(bookId)) {
	 await Promise.allSettled([
		fetchBookDetails(bookId, true),
		fetchBooks({
		  ...searchParams.value,
		  page: page.value,
		  itemsPerPage: itemsPerPage.value,
		  sortBy: sortBy.value,
		  sortDesc: sortDesc.value,
		}),
	 ]);
  }

  emit('book-updated', updatedBookData);
};

const handleBookDeleted = async (payload: any) => {
  const bookId = Number(payload?.bookId);

  if (Number.isFinite(bookId)) {
	 delete bookDetails.value[bookId];
	 delete loadingDetails.value[bookId];
	 delete detailsErrors.value[bookId];
  }

  await fetchBooks({
	 ...searchParams.value,
	 page: page.value,
	 itemsPerPage: itemsPerPage.value,
	 sortBy: sortBy.value,
	 sortDesc: sortDesc.value,
  });
};

const handleEditCancelled = () => {
  emit('edit-cancelled');
};

</script>

<style scoped>
.book-details .v-card {
	min-height: 80px;
}

.book-details .v-card-subtitle {
	font-weight: 600;
	color: rgba(0, 0, 0, 0.6);
	padding-bottom: 4px;
}

.book-details .v-card-text {
	padding-top: 8px;
	font-size: 0.9rem;
}

.hourglass-icon {
	display: inline-block;
	font-size: 64px;
	line-height: 1;
	animation: hourglass-flip 2s ease-in-out infinite;
}

@keyframes hourglass-flip {
	0% { transform: rotate(0deg); }
	45% { transform: rotate(180deg); }
	55% { transform: rotate(180deg); }
	100% { transform: rotate(360deg); }
}
</style>
