<template>
	<!--
		BookFilterSelector
		──────────────────
		Lets the user choose up to 4 fields to display as search inputs.
		Only columns that are BOTH currently visible AND in FILTERABLE_KEYS are shown.

		Props
		  modelValue    : string[]  – currently selected filter keys
		  visibleColumns: string[]  – columns selected in BookColumnSelector
	-->
	<v-row dense>
		<v-col
			v-for="col in filterableVisible"
			:key="col.key"
			cols="12" sm="6" md="4"
		>
			<v-checkbox
				:model-value="modelValue.includes(col.key)"
				:label="$t(col.titleI18n)"
				:disabled="!modelValue.includes(col.key) && modelValue.length >= MAX_FILTERS"
				density="compact"
				hide-details
				@update:model-value="toggle(col.key, $event as boolean)"
			/>
		</v-col>

		<!-- Counter hint ──────────────────────────────────────────────── -->
		<v-col cols="12" class="pt-1">
			<span
				class="text-caption"
				:class="modelValue.length >= MAX_FILTERS ? 'text-warning' : 'text-medium-emphasis'"
			>
				{{ $t('books.filtersSelected', { count: modelValue.length, max: MAX_FILTERS }) }}
			</span>
		</v-col>
	</v-row>
</template>

<script setup lang="ts">
import { ALL_BOOK_COLUMNS, FILTERABLE_KEYS } from '~/stores/bookTable'

// ── Constants ──────────────────────────────────────────────────────────────

const MAX_FILTERS = 4

// ── Props / emits ──────────────────────────────────────────────────────────

const props = defineProps<{
	modelValue:     string[]
	visibleColumns: string[]
}>()
const emit = defineEmits<{ 'update:modelValue': [value: string[]] }>()

// ── Filtered column list ───────────────────────────────────────────────────

const filterableVisible = computed(() =>
	ALL_BOOK_COLUMNS.filter(
		c => props.visibleColumns.includes(c.key) && FILTERABLE_KEYS.includes(c.key),
	),
)

// ── Toggle helper ──────────────────────────────────────────────────────────

const toggle = (key: string, checked: boolean) => {
	if (checked && props.modelValue.length >= MAX_FILTERS) return
	const next = [...props.modelValue]
	if (checked) {
		if (!next.includes(key)) next.push(key)
	} else {
		const idx = next.indexOf(key)
		if (idx !== -1) next.splice(idx, 1)
	}
	emit('update:modelValue', next)
}
</script>
