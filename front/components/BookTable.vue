<template>
	<v-card>
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
							:text="isExpanded(internalItem) ? 'Collapse' : 'Details'"
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
											@edit-cancelled="handleEditCancelled"
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

			<template #item.actions="{ item }">
				<v-btn
						icon="mdi-delete"
						color="error"
						variant="text"
						:aria-label="$t('books.delete')"
						@click="openDeleteDialog(item)"
						/>
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
		<v-dialog
				v-model="showDeleteDialog"
				max-width="520px"
				>
				<v-card>
					<v-card-title>{{ $t('books.deleteConfirmTitle') }}</v-card-title>
					<v-card-text>
						{{ t('books.deleteConfirmText', { title: deleteCandidateTitle }) }}
					</v-card-text>
					<v-card-actions class="justify-end">
						<v-btn
								variant="text"
								:disabled="deletingBook"
								@click="closeDeleteDialog"
								>
								{{ $t('books.cancel') }}
						</v-btn>
						<v-btn
								color="error"
								variant="elevated"
								:loading="deletingBook"
								:disabled="deletingBook"
								@click="confirmDeleteBook"
								>
								{{ $t('books.confirm') }}
						</v-btn>
					</v-card-actions>
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
} = useBooks();

const { transformBookDataToCards, transformBookDataToBigCards } = useBookFormat();

const showAddBookDialog = ref(false);
const showDeleteDialog = ref(false);
const deletingBook = ref(false);
const deleteCandidateId = ref<number | null>(null);
const deleteCandidateTitle = ref('');
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
const openDeleteDialog = (item: any) => {
  const candidateId = Number(item?.id);
  if (!Number.isFinite(candidateId)) {
	 return;
  }

  deleteCandidateId.value = candidateId;
  deleteCandidateTitle.value = String(item?.title || '');
  showDeleteDialog.value = true;
};

const closeDeleteDialog = () => {
  showDeleteDialog.value = false;
  deleteCandidateId.value = null;
  deleteCandidateTitle.value = '';
};

const confirmDeleteBook = async () => {
  const candidateId = deleteCandidateId.value;
  if (candidateId === null) {
	 return;
  }

  deletingBook.value = true;

  try {
	 await useAPI(`/books/${candidateId}`, {
		method: 'DELETE'
	 });

	 delete bookDetails.value[candidateId];
	 delete loadingDetails.value[candidateId];
	 delete detailsErrors.value[candidateId];

	 await fetchBooks({
		...searchParams.value,
		page: page.value,
		itemsPerPage: itemsPerPage.value,
		sortBy: sortBy.value,
		sortDesc: sortDesc.value,
	 });

	 closeDeleteDialog();
  } catch (error) {
	 console.error('Failed to delete book:', error);
  } finally {
	 deletingBook.value = false;
  }
};

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
</style>
