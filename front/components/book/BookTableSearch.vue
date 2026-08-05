<template>
	<!--
		BookTableSearch
		───────────────
		Renders up to 4 search text-fields driven by the store's activeFilterFields.

		Props
		  searchParams : reactive object from useBooks() – mutated in-place
		                 (same reference, so the parent observes changes automatically)
		Emits
		  search       : trigger a (debounced) fetchBooks in the parent
	-->
	<v-row class="px-4 pt-2 pb-0">
		<v-col
			v-for="field in visibleFields"
			:key="field.key"
			cols="12" sm="6" md="3"
		>
			<v-text-field
				v-model="searchParams[field.searchKey]"
				:label="$t(field.labelI18n)"
				clearable
				density="compact"
				@update:model-value="emit('search')"
			/>
		</v-col>
	</v-row>
</template>

<script setup lang="ts">
import {
	useBookTableStore,
	ALL_BOOK_COLUMNS,
	COLUMN_TO_SEARCH_KEY,
} from '~/stores/bookTable'

// ── Props / emits ──────────────────────────────────────────────────────────

/**
 * searchParams is the reactive object from useBooks() passed in by BookTableView.
 * Since it is an object (not a primitive), in-place mutations are fine and Vue
 * tracks them reactively in the parent.
 */
const props = defineProps<{
	searchParams: Record<string, string>
}>()

const emit = defineEmits<{ search: [] }>()

// ── Store ──────────────────────────────────────────────────────────────────

const store = useBookTableStore()

// ── Derived field list ─────────────────────────────────────────────────────

/**
 * For each active filter key in the store, resolve:
 *  - the searchParams key used by useBooks()
 *  - the i18n label key
 */
const visibleFields = computed(() =>
	store.activeFilterFields
		.filter(key => key in COLUMN_TO_SEARCH_KEY)
		.map(key => {
			const col = ALL_BOOK_COLUMNS.find(c => c.key === key)
			return {
				key,
				searchKey: COLUMN_TO_SEARCH_KEY[key],
				labelI18n: col?.titleI18n ?? `books.col${key}`,
			}
		}),
)
</script>
