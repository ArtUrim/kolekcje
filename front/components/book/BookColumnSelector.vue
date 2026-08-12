<template>
	<!--
		BookColumnSelector
		──────────────────
		Renders a checkbox for every possible book column.
		modelValue  : string[]  – keys of currently visible columns
		Emits 'update:modelValue' with the new list whenever a checkbox is toggled.
	-->
	<v-row dense>
		<v-col
			v-for="col in ALL_BOOK_COLUMNS"
			:key="col.key"
			cols="12" sm="6" md="4"
		>
			<v-checkbox
				:model-value="modelValue.includes(col.key)"
				:label="$t(col.titleI18n)"
				density="compact"
				hide-details
				@update:model-value="toggle(col.key, $event as boolean)"
			/>
		</v-col>
	</v-row>
</template>

<script setup lang="ts">
import { ALL_BOOK_COLUMNS } from '~/stores/bookTable'

// ── Props / emits ──────────────────────────────────────────────────────────

const props = defineProps<{ modelValue: string[] }>()
const emit  = defineEmits<{ 'update:modelValue': [value: string[]] }>()

// ── Toggle helper ──────────────────────────────────────────────────────────

const toggle = (key: string, checked: boolean) => {
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
