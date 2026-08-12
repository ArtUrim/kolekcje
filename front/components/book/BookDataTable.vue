<template>
	<!--
		BookDataTable
		─────────────
		Pure presentation layer around <v-data-table-server>.
		All data-fetching and state live in BookTableView; this component
		only renders rows, handles expand/collapse, and surfaces CRUD events
		from ExpandableContainer back up to the parent.

		Column headers are derived from the Pinia store so they respond
		immediately when the user switches a preset or custom setting.
	-->
	<v-data-table-server
		v-model:items-per-page="internalItemsPerPage"
		v-model:page="internalPage"
		v-model:sort-by="internalSortBy"
		v-model:sort-desc="internalSortDesc"
		:headers="computedHeaders"
		:items="items"
		:items-length="totalItems"
		:loading="loading"
		show-expand
		class="elevation-1"
		@update:options="$emit('update:options', $event)"
	>

		<!-- ── Expand / collapse button ──────────────────────────────────── -->
		<template #item.data-table-expand="{ internalItem, isExpanded, toggleExpand }">
			<v-btn
				:append-icon="isExpanded(internalItem) ? 'mdi-chevron-up' : 'mdi-chevron-down'"
				:text="isExpanded(internalItem) ? $t('bookinfo.collapse') : $t('bookinfo.details')"
				class="text-none"
				color="primary"
				size="small"
				variant="outlined"
				@click="$emit('expand-toggle', internalItem, toggleExpand)"
			/>
		</template>

		<!-- ── Expanded detail row ────────────────────────────────────────── -->
		<template #expanded-row="{ columns, item }">
			<tr>
				<td :colspan="columns.length" class="pa-4">
					<v-card flat>
						<v-card-text>

							<!-- Loading state -->
							<div v-if="loadingDetails[item.id]" class="text-center py-4">
								<v-progress-circular indeterminate color="primary" />
								<p class="mt-2">{{ $t('books.loadingDetails') }}</p>
							</div>

							<!-- Loaded state -->
							<div v-else-if="bookDetails[item.id]">
								<ExpandableContainer
									:fields="bookDetails[item.id]"
									:book-id="String(item.id)"
									@book-updated="$emit('book-updated', $event)"
									@book-deleted="$emit('book-deleted', $event)"
									@edit-cancelled="$emit('edit-cancelled')"
									@book-added="$emit('book-added')"
								/>
							</div>

							<!-- Error state -->
							<div v-else-if="detailsErrors[item.id]" class="text-center py-4">
								<v-icon color="error" size="48">mdi-alert-circle</v-icon>
								<p class="mt-2 text-error">{{ $t('books.detailsError') }}</p>
								<v-btn
									color="primary"
									variant="outlined"
									@click="$emit('retry-details', item.id)"
								>
									{{ $t('common.retry') }}
								</v-btn>
							</div>

						</v-card-text>
					</v-card>
				</td>
			</tr>
		</template>

		<!-- ── Cell slots for special formatting ─────────────────────────── -->
		<template #item.release_date="{ item }">
			{{ item.release_date }}
		</template>

		<template #item.series_name="{ item }">
			{{ item.series_name || '' }}
		</template>

		<!-- ── Empty state ────────────────────────────────────────────────── -->
		<template #no-data>
			{{ $t('books.nobooks') }}
		</template>

	</v-data-table-server>
</template>

<script setup lang="ts">
import { useBookTableStore } from '~/stores/bookTable'

// ── Props ──────────────────────────────────────────────────────────────────
const props = withDefaults(
	defineProps<{
		items:          any[]
		loading:        boolean
		totalItems:     number
		bookDetails:    Record<number, any>
		loadingDetails: Record<number, boolean>
		detailsErrors:  Record<number, boolean>
		page:           number
		itemsPerPage:   number
		sortBy?:        any[]
		sortDesc?:      boolean[]
	}>(),
	{
		sortBy:   () => [],
		sortDesc: () => [],
	}
)

// ── Emits ──────────────────────────────────────────────────────────────────

const emit = defineEmits<{
	'update:page':         [v: number]
	'update:itemsPerPage': [v: number]
	'update:sortBy':       [v: string[]]
	'update:sortDesc':     [v: boolean[]]
	'update:options':      [options: any]
	'expand-toggle':       [internalItem: any, toggleExpand: Function]
	'book-updated':        [bookData: any]
	'book-deleted':        [payload: any]
	'edit-cancelled':      []
	'book-added':          []
	'retry-details':       [bookId: number]
}>()

// ── v-model proxies ────────────────────────────────────────────────────────

const internalPage = computed({
	get: () => props.page,
	set: (v) => emit('update:page', v),
})
const internalItemsPerPage = computed({
	get: () => props.itemsPerPage,
	set: (v) => emit('update:itemsPerPage', v),
})
const internalSortBy = computed({
	get: () => props.sortBy,
	set: (v) => emit('update:sortBy', v),
})
const internalSortDesc = computed({
	get: () => props.sortDesc,
	set: (v) => emit('update:sortDesc', v),
})

// ── Headers (reactive, driven by store) ───────────────────────────────────

const store = useBookTableStore()
const { t } = useI18n()

/**
 * Translate column definitions to the format expected by v-data-table-server.
 * Recomputed automatically whenever the active preset / custom selection changes.
 */
const computedHeaders = computed(() =>
	store.activeColumnDefs.map(col => ({
		title:    t(col.titleI18n),
		key:      col.key,
		sortable: col.sortable,
		align:    col.align,
	})),
)
</script>
