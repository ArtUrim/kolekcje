<template>
	<v-card>

		<v-card-title>{{ $t('stats.title') }}</v-card-title>

		<!-- ── Tabs: labels / genres / series / languages ─────────────────── -->
		<v-tabs v-model="tab" color="primary">
			<v-tab value="labels">{{ $t('stats.tabs.labels') }}</v-tab>
			<v-tab value="genres">{{ $t('stats.tabs.genres') }}</v-tab>
			<v-tab value="series">{{ $t('stats.tabs.series') }}</v-tab>
			<v-tab value="languages">{{ $t('stats.tabs.languages') }}</v-tab>
		</v-tabs>

		<v-card-text>

			<!-- ── Error state ───────────────────────────────────────────── -->
			<div v-if="loadError" class="text-center py-4">
				<v-icon color="error" size="48">mdi-alert-circle</v-icon>
				<p class="mt-2 text-error">{{ $t('stats.error') }}</p>
				<v-btn color="primary" variant="outlined" @click="fetchAll">
					{{ $t('stats.retry') }}
				</v-btn>
			</div>

			<!-- ── Shared tab structure, one instance per category ────────── -->
			<v-window v-else v-model="tab">
				<v-window-item value="labels">
					<StatsCategory
						:items="labelItems"
						:loading="loading"
						:load-books="loadLabelBooks"
						@book-deleted="fetchAll"
					/>
				</v-window-item>
				<v-window-item value="genres">
					<StatsCategory
						:items="genreItems"
						:loading="loading"
						:load-books="loadGenreBooks"
						@book-deleted="fetchAll"
					/>
				</v-window-item>
				<v-window-item value="series">
					<StatsCategory
						:items="seriesItems"
						:loading="loading"
						:load-books="loadSeriesBooks"
						@book-deleted="fetchAll"
					/>
				</v-window-item>
				<v-window-item value="languages">
					<StatsCategory
						:items="languageItems"
						:loading="loading"
						:load-books="loadLanguageBooks"
						@book-deleted="fetchAll"
					/>
				</v-window-item>
			</v-window>
		</v-card-text>
	</v-card>
</template>

<script setup lang="ts">
import type { StatsBook, StatsItem } from '~/types/book'

type StatsTab = 'labels' | 'genres' | 'series' | 'languages'

type StatsCatalog = 'labels' | 'genres' | 'series' | 'languages'

interface CatalogStat {
	id: string | number
	value: string
	count: number
}

// ── State ──────────────────────────────────────────────────────────────────

const tab = ref<StatsTab>('labels')

const loading = ref(false)
const loadError = ref(false)
const catalogStats = ref<Record<StatsCatalog, CatalogStat[]>>({
	labels: [],
	genres: [],
	series: [],
	languages: [],
})

// ── Data fetching (client side only, so prerender needs no backend) ────────

const fetchAll = async () => {
	loading.value = true
	loadError.value = false

	try {
		const [labelStatsResponse, genreStatsResponse, seriesStatsResponse, languageStatsResponse] =
			await Promise.all([
				useAPI<CatalogStat[]>('/labels/stats'),
				useAPI<CatalogStat[]>('/genres/stats'),
				useAPI<CatalogStat[]>('/series/stats'),
				useAPI<CatalogStat[]>('/languages/stats'),
			])

		catalogStats.value = {
			labels: labelStatsResponse ?? [],
			genres: genreStatsResponse ?? [],
			series: seriesStatsResponse ?? [],
			languages: languageStatsResponse ?? [],
		}
	} catch (err) {
		console.error('Error fetching statistics:', err)
		loadError.value = true
	} finally {
		loading.value = false
	}
}

// Fetch the books of a single catalog entry on demand instead of pulling
// every book up front. Books of a language live under /language/{id}
// (singular); the other catalogs under /{catalog}/{id}.
const BOOKS_PATH: Record<StatsCatalog, string> = {
	labels: 'labels',
	genres: 'genres',
	series: 'series',
	languages: 'language',
}

const loadCatalogBooks =
	(catalog: StatsCatalog) =>
	(item: StatsItem): Promise<StatsBook[]> => {
		if (item.id == null) {
			return Promise.resolve([])
		}
		return useAPI<StatsBook[]>(`/${BOOKS_PATH[catalog]}/${item.id}`)
	}

const loadLabelBooks = loadCatalogBooks('labels')
const loadGenreBooks = loadCatalogBooks('genres')
const loadSeriesBooks = loadCatalogBooks('series')
const loadLanguageBooks = loadCatalogBooks('languages')

onMounted(fetchAll)

// ── Statistics computation ──────────────────────────────────────────────────

const statsToItems = (stats: CatalogStat[]): StatsItem[] =>
	[...stats]
		.map((stat) => ({ id: stat.id, name: stat.value, count: stat.count }))
		.sort((a, b) => b.count - a.count || a.name.localeCompare(b.name))

const labelItems = computed<StatsItem[]>(() => statsToItems(catalogStats.value.labels))
const genreItems = computed<StatsItem[]>(() => statsToItems(catalogStats.value.genres))
const seriesItems = computed<StatsItem[]>(() => statsToItems(catalogStats.value.series))

const languageItems = computed<StatsItem[]>(() => statsToItems(catalogStats.value.languages))
</script>
