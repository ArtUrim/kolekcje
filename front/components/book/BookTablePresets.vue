<template>
	<v-row class="px-4 pt-2 pb-0 align-center" no-gutters>

		<!-- ── Preset toggle buttons ──────────────────────────────────────── -->
		<v-col cols="auto">
			<v-btn-toggle
				:model-value="store.isCustom ? undefined : store.activePresetId"
				color="primary"
				variant="outlined"
				density="compact"
				rounded="pill"
			>
				<v-btn
					v-for="preset in store.presets"
					:key="preset.id"
					:value="preset.id"
					size="small"
					@click="store.applyPreset(preset.id)"
				>
					{{ $t(preset.labelI18n) }}
				</v-btn>
			</v-btn-toggle>
		</v-col>

		<!-- ── Custom indicator (shown when user edited settings manually) ── -->
		<v-col v-if="store.isCustom" cols="auto" class="ml-2">
			<v-chip size="small" color="secondary" variant="tonal">
				{{ $t('books.presetCustom') }}
			</v-chip>
		</v-col>

		<!-- ── Settings icon (opens BookTableSettings dialog) ────────────── -->
		<v-col cols="auto" class="ml-auto">
			<v-btn
				icon="mdi-table-cog"
				variant="text"
				color="primary"
				:title="$t('books.settings')"
				@click="showSettings = true"
			/>
		</v-col>

	</v-row>

	<!-- ── Settings dialog (lazy-mounted) ─────────────────────────────────── -->
	<BookTableSettings v-model="showSettings" />
</template>

<script setup lang="ts">
import { useBookTableStore } from '~/stores/bookTable'

const store       = useBookTableStore()
const showSettings = ref(false)
</script>
