<template>
	<v-dialog
		:model-value="modelValue"
		max-width="640px"
		scrollable
		@update:model-value="$emit('update:modelValue', $event)"
	>
		<v-card>
			<v-card-title class="d-flex justify-space-between align-center">
				{{ $t('books.settingsTitle') }}
				<v-btn
					icon="mdi-close"
					variant="text"
					@click="cancel"
				/>
			</v-card-title>

			<v-divider />

			<v-card-text class="py-4">

				<!-- ── Column visibility ──────────────────────────────────────── -->
				<p class="text-subtitle-2 mb-2">{{ $t('books.settingsColumns') }}</p>
				<BookColumnSelector v-model="localColumns" />

				<v-divider class="my-4" />

				<!-- ── Filter fields ──────────────────────────────────────────── -->
				<p class="text-subtitle-2 mb-1">
					{{ $t('books.settingsFilters') }}
					<span class="text-caption text-medium-emphasis ml-1">(max 4)</span>
				</p>
				<BookFilterSelector
					v-model="localFilters"
					:visible-columns="localColumns"
				/>

			</v-card-text>

			<v-divider />

			<v-card-actions class="justify-end pa-3">
				<v-btn variant="text"     @click="cancel">{{ $t('common.cancel') }}</v-btn>
				<v-btn color="primary" variant="elevated" @click="save">{{ $t('common.save') }}</v-btn>
			</v-card-actions>
		</v-card>
	</v-dialog>
</template>

<script setup lang="ts">
import { useBookTableStore } from '~/stores/bookTable'

// ── Props / emits ──────────────────────────────────────────────────────────

const props = defineProps<{ modelValue: boolean }>()
const emit  = defineEmits<{ 'update:modelValue': [value: boolean] }>()

// ── Store ──────────────────────────────────────────────────────────────────

const store = useBookTableStore()

// ── Local (draft) state – initialised when dialog opens ───────────────────

const localColumns = ref<string[]>([])
const localFilters = ref<string[]>([])

watch(
	() => props.modelValue,
	(open) => {
		if (open) {
			localColumns.value = [...store.activeColumns]
			localFilters.value = [...store.activeFilterFields]
		}
	},
)

// ── Actions ────────────────────────────────────────────────────────────────

const save = () => {
	store.applyCustom(localColumns.value, localFilters.value)
	emit('update:modelValue', false)
}

const cancel = () => emit('update:modelValue', false)
</script>
