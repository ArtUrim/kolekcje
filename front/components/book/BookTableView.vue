<template>
	<v-card style="position: relative;">

		<!-- ── Retrying overlay ──────────────────────────────────────────── -->
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

		<!-- ── Card header: title + New Book button ───────────────────────── -->
		<v-card-title>
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

		<!-- ── Preset toggle buttons + Settings icon ─────────────────────── -->
		<BookTablePresets />

		<!-- ── Dynamic search fields (driven by activeFilterFields) ──────── -->
		<BookTableSearch
			:search-params="searchParams"
			@search="handleSearch"
		/>

		<!-- ── Server-side data table ─────────────────────────────────────── -->
		<BookDataTable
			:items="items"
			:loading="loading"
			:total-items="totalItems"
			:book-details="bookDetails"
			:loading-details="loadingDetails"
			:details-errors="detailsErrors"
			v-model:page="page"
			v-model:items-per-page="itemsPerPage"
			v-model:sort-by="sortBy"
			v-model:sort-desc="sortDesc"
			@update:options="handleOptionsUpdate"
			@expand-toggle="handleExpandToggle"
			@book-updated="handleBookUpdated"
			@book-deleted="handleBookDeleted"
			@edit-cancelled="handleEditCancelled"
			@book-added="handleBookAdded"
			@retry-details="fetchBookDetails"
		/>

		<!-- ── Add-book dialog ────────────────────────────────────────────── -->
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
						@click="showAddBookDialog = false"
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
import debounce from 'lodash/debounce'
import { useBooks }      from '~/composables/useBooks'
import { useBookFormat } from '~/composables/bookFormat'

// ── Emits ──────────────────────────────────────────────────────────────────

const emit = defineEmits<{
	'book-updated':   [bookData: any]
	'edit-cancelled': []
}>()

// ── Composables ────────────────────────────────────────────────────────────

const {
	items,
	loading,
	totalItems,
	fetchBooks,
	searchParams,
	isRetrying,
} = useBooks()

const { transformBookDataToCards, transformBookDataToBigCards } = useBookFormat()

// ── Local state ────────────────────────────────────────────────────────────

const showAddBookDialog = ref(false)
const page              = ref(1)
const itemsPerPage      = ref(10)
const sortBy            = ref<string[]>([])
const sortDesc          = ref<boolean[]>([])

const bookDetails    = ref<Record<number, any>>({})
const loadingDetails = ref<Record<number, boolean>>({})
const detailsErrors  = ref<Record<number, boolean>>({})

// ── Helpers ────────────────────────────────────────────────────────────────

const fetchCurrentPage = () =>
	fetchBooks({
		...searchParams.value,
		page:         page.value,
		itemsPerPage: itemsPerPage.value,
		sortBy:       sortBy.value,
		sortDesc:     sortDesc.value,
	})

// ── Search (debounced) ─────────────────────────────────────────────────────

const handleSearch = debounce(() => {
	page.value = 1
	fetchCurrentPage()
}, 300)

// ── Table options update ───────────────────────────────────────────────────

const handleOptionsUpdate = (options: any) => {
	page.value         = options.page
	itemsPerPage.value = options.itemsPerPage
	sortBy.value       = options.sortBy
	sortDesc.value     = options.sortDesc
	fetchCurrentPage()
}

// ── Book-details fetching ──────────────────────────────────────────────────

const fetchBookDetails = async (bookId: number, forceRefresh = false) => {
	if (bookDetails.value[bookId] && !forceRefresh) return

	loadingDetails.value[bookId] = true
	detailsErrors.value[bookId]  = false

	try {
		const data        = await useAPI(`/bookinfo?id=${bookId}`)
		const bookPayload = data?.book || data
		const copy        = JSON.parse(JSON.stringify(bookPayload))

		bookDetails.value[bookId] = {
			originalData: copy,
			cards:        transformBookDataToCards(copy),
			longCards:    transformBookDataToBigCards(copy),
		}
	} catch {
		detailsErrors.value[bookId] = true
	} finally {
		loadingDetails.value[bookId] = false
	}
}

// ── Expand / collapse row ──────────────────────────────────────────────────

const handleExpandToggle = async (internalItem: any, toggleExpand: Function) => {
	const bookId = internalItem.value
	if (!bookDetails.value[bookId] && !loadingDetails.value[bookId]) {
		await fetchBookDetails(bookId)
	}
	toggleExpand(internalItem)
}

// ── CRUD event handlers ────────────────────────────────────────────────────

const handleBookAdded = () => {
	showAddBookDialog.value = false
	fetchCurrentPage()
}

const handleBookUpdated = async (updatedBookData: any) => {
	const bookId = Number(updatedBookData?.bookId)
	if (Number.isFinite(bookId)) {
		await Promise.allSettled([
			fetchBookDetails(bookId, true),
			fetchCurrentPage(),
		])
	}
	emit('book-updated', updatedBookData)
}

const handleBookDeleted = async (payload: any) => {
	const bookId = Number(payload?.bookId)
	if (Number.isFinite(bookId)) {
		delete bookDetails.value[bookId]
		delete loadingDetails.value[bookId]
		delete detailsErrors.value[bookId]
	}
	await fetchCurrentPage()
}

const handleEditCancelled = () => emit('edit-cancelled')
</script>

<style scoped>
.hourglass-icon {
	display: inline-block;
	font-size: 64px;
	line-height: 1;
	animation: hourglass-flip 2s ease-in-out infinite;
}

@keyframes hourglass-flip {
	0%   { transform: rotate(0deg);   }
	45%  { transform: rotate(180deg); }
	55%  { transform: rotate(180deg); }
	100% { transform: rotate(360deg); }
}
</style>
