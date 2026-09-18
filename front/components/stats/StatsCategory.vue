<template>
	<div>
		<v-row>

			<!-- ── Left: names with occurrence counts ────────────────────── -->
			<v-col cols="12" md="6">
				<v-table fixed-header density="comfortable" class="stats-table">
					<thead>
						<tr>
							<th>{{ $t('stats.name') }}</th>
							<th class="text-right">{{ $t('stats.occurrences') }}</th>
						</tr>
					</thead>
					<tbody>
						<tr v-if="loading && !items.length">
							<td colspan="2" class="text-center py-4">
								<v-progress-circular indeterminate color="primary" />
							</td>
						</tr>
						<tr v-else-if="!items.length">
							<td colspan="2" class="text-center">{{ $t('stats.noData') }}</td>
						</tr>
						<tr
							v-for="item in items"
							:key="item.name"
							:class="{ 'stats-row-selected': item.name === selectedName }"
							@click="selectItem(item.name)"
						>
							<td>{{ item.name }}</td>
							<td class="text-right">{{ item.count }}</td>
						</tr>
					</tbody>
				</v-table>
			</v-col>

			<!-- ── Right: book titles of the chosen name ─────────────────── -->
			<v-col cols="12" md="6">
				<v-card variant="outlined" class="stats-book-panel">
					<div v-if="!selectedItem" class="text-center text-medium-emphasis pa-4">
						{{ $t('stats.selectHint') }}
					</div>
					<div v-else-if="loadingBooks" class="text-center py-4">
						<v-progress-circular indeterminate color="primary" />
					</div>
					<div v-else-if="!selectedBooks.length" class="text-center text-medium-emphasis pa-4">
						{{ $t('books.nobooks') }}
					</div>
					<v-list v-else>
						<v-list-item
							v-for="book in selectedBooks"
							:key="book.id"
							:title="book.title"
							prepend-icon="mdi-book-open-variant"
							@click="openBook(book)"
						/>
					</v-list>
				</v-card>
			</v-col>
		</v-row>

		<!-- ── Full book info popup ──────────────────────────────────────── -->
		<v-dialog
			v-model="showBookDialog"
			max-width="900px"
			scrollable
		>
			<v-card>
				<v-card-title class="d-flex justify-space-between align-center">
					<span>{{ selectedBook?.title }}</span>
					<v-btn
						icon="mdi-close"
						variant="text"
						@click="showBookDialog = false"
					/>
				</v-card-title>
				<v-card-text>
					<div v-if="loadingBook" class="text-center py-4">
						<v-progress-circular indeterminate color="primary" />
						<p class="mt-2">{{ $t('stats.loadingBook') }}</p>
					</div>
					<div v-else-if="bookError" class="text-center py-4">
						<v-icon color="error" size="48">mdi-alert-circle</v-icon>
						<p class="mt-2 text-error">{{ $t('stats.bookLoadError') }}</p>
					</div>
					<BookInfo
						v-else-if="bookInfo"
						:book="bookInfoData"
						@delete-requested="showDeleteDialog = true"
					/>
				</v-card-text>
			</v-card>
		</v-dialog>

		<!-- ── Delete confirmation ───────────────────────────────────────── -->
		<v-dialog v-model="showDeleteDialog" max-width="520px">
			<v-card>
				<v-card-title>{{ $t('books.deleteConfirmTitle') }}</v-card-title>
				<v-card-text>
					{{ $t('books.deleteConfirmText', { title: selectedBook?.title || '' }) }}
				</v-card-text>
				<v-card-actions class="justify-end">
					<v-btn
						variant="text"
						:disabled="deletingBook"
						@click="showDeleteDialog = false"
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
	</div>
</template>

<script setup lang="ts">
import type { StatsBook, StatsItem } from '~/types/book'

// ── Props ──────────────────────────────────────────────────────────────────

const props = withDefaults(
	defineProps<{
		items: StatsItem[]
		loading?: boolean
		loadBooks?: (item: StatsItem) => Promise<StatsBook[]>
	}>(),
	{
		loading: false,
	}
)

// ── Emits ──────────────────────────────────────────────────────────────────

const emit = defineEmits<{
	'book-deleted': [bookId: number]
}>()

// ── Left table selection ───────────────────────────────────────────────────

const selectedName = ref<string | null>(null)

const selectedItem = computed<StatsItem | null>(() =>
	props.items.find((item) => item.name === selectedName.value) ?? null
)

const lazyBooks = ref<StatsBook[]>([])
const loadingBooks = ref(false)

const selectedBooks = computed<StatsBook[]>(() =>
	props.loadBooks ? lazyBooks.value : selectedItem.value?.books ?? []
)

const loadBooksFor = async (item: StatsItem) => {
	if (!props.loadBooks) {
		return
	}

	loadingBooks.value = true
	try {
		lazyBooks.value = await props.loadBooks(item)
	} catch (err) {
		console.error('Error fetching books for item:', err)
		lazyBooks.value = []
	} finally {
		loadingBooks.value = false
	}
}

const selectItem = (name: string) => {
	selectedName.value = name

	const item = props.items.find((i) => i.name === name)
	if (item) {
		loadBooksFor(item)
	}
}

// ── Full book info popup ───────────────────────────────────────────────────

const selectedBook = ref<StatsBook | null>(null)
const showBookDialog = ref(false)
const loadingBook = ref(false)
const bookError = ref(false)
const bookInfo = ref<Record<string, any> | null>(null)

const openBook = async (book: StatsBook) => {
	selectedBook.value = book
	showBookDialog.value = true
	loadingBook.value = true
	bookError.value = false
	bookInfo.value = null

	try {
		bookInfo.value = await useAPI(`/books/${book.id}`)
	} catch (err) {
		console.error('Error fetching book details:', err)
		bookError.value = true
	} finally {
		loadingBook.value = false
	}
}

const detailNames = (
	details: Array<{ name?: string } | null | undefined> | null | undefined
): string[] =>
	(details ?? []).map((detail) => detail?.name).filter((name): name is string => Boolean(name))

const bookInfoData = computed(() => {
	const source = bookInfo.value ?? {}

	return {
		title: source.title || '',
		originalTitle: source.original_title || '',
		subtitle: source.subtitle || '',
		authors: detailNames(source.authors_details),
		isbn: source.isbn || '',
		releaseDate: source.release_date || '',
		firstPolishRelease: source.first_polish_release_date || '',
		format: source.format || '',
		pages: source.pages || '',
		serie: source.series_name || '',
		size: source.size || '',
		language: source.language_name || '',
		translator: source.translator || '',
		publishers: detailNames(source.publishers_details),
		genres: detailNames(source.genres_details),
		labels: detailNames(source.labels_details),
		description: source.description || '',
		note: source.note || '',
	}
})

// ── Delete book ────────────────────────────────────────────────────────────

const showDeleteDialog = ref(false)
const deletingBook = ref(false)

const confirmDeleteBook = async () => {
	if (!selectedBook.value) {
		return
	}

	deletingBook.value = true

	try {
		await useAPI(`/books/${selectedBook.value.id}`, { method: 'DELETE' })
		showDeleteDialog.value = false
		showBookDialog.value = false
		emit('book-deleted', selectedBook.value.id)

		if (selectedItem.value) {
			loadBooksFor(selectedItem.value)
		}
	} catch (err) {
		console.error('Failed to delete book:', err)
	} finally {
		deletingBook.value = false
	}
}
</script>

<style scoped>
.stats-table {
	max-height: 480px;
}

.stats-table tbody tr {
	cursor: pointer;
}

.stats-row-selected {
	background: rgba(2, 136, 209, 0.1);
}

.stats-book-panel {
	max-height: 480px;
	overflow-y: auto;
}
</style>
