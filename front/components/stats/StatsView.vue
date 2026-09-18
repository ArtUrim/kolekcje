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
			<div v-if="loadError[tab]" class="text-center py-4">
				<v-icon color="error" size="48">mdi-alert-circle</v-icon>
				<p class="mt-2 text-error">{{ $t('stats.error') }}</p>
				<v-btn color="primary" variant="outlined" @click="fetchCategory(tab)">
					{{ $t('stats.retry') }}
				</v-btn>
			</div>

			<!-- ── Shared tab structure, one instance per category ────────── -->
			<v-window v-else v-model="tab">
				<v-window-item value="labels">
					<StatsCategory
						:items="labelItems"
						:loading="loading.labels"
						:load-books="loadLabelBooks"
						@book-deleted="fetchCategory('labels')"
					/>
				</v-window-item>
				<v-window-item value="genres">
					<StatsCategory
						:items="genreItems"
						:loading="loading.genres"
						:load-books="loadGenreBooks"
						@book-deleted="fetchCategory('genres')"
					/>
				</v-window-item>
				<v-window-item value="series">
					<StatsCategory
						:items="seriesItems"
						:loading="loading.series"
						:load-books="loadSeriesBooks"
						@book-deleted="fetchCategory('series')"
					/>
				</v-window-item>
				<v-window-item value="languages">
					<StatsCategory
						:items="languageItems"
						:loading="loading.languages"
						:load-books="loadLanguageBooks"
						@book-deleted="fetchCategory('languages')"
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

const loading = reactive<Record<StatsCatalog, boolean>>({
	labels: false,
	genres: false,
	series: false,
	languages: false,
})
const loadError = reactive<Record<StatsCatalog, boolean>>({
	labels: false,
	genres: false,
	series: false,
	languages: false,
})
const loaded = reactive<Record<StatsCatalog, boolean>>({
	labels: false,
	genres: false,
	series: false,
	languages: false,
})
const catalogStats = ref<Record<StatsCatalog, CatalogStat[]>>({
	labels: [],
	genres: [],
	series: [],
	languages: [],
})

// ── Data fetching (client side only, so prerender needs no backend) ────────
// Each catalog's stats are fetched lazily, only the first time its tab is
// shown, instead of pulling every catalog up front.

const STATS_PATH: Record<StatsCatalog, string> = {
	labels: '/labels/stats',
	genres: '/genres/stats',
	series: '/series/stats',
	languages: '/languages/stats',
}

const fetchCategory = async (catalog: StatsCatalog) => {
	loading[catalog] = true
	loadError[catalog] = false

	try {
		const response = await useAPI<CatalogStat[]>(STATS_PATH[catalog])
		catalogStats.value[catalog] = response ?? []
		loaded[catalog] = true
	} catch (err) {
		console.error('Error fetching statistics:', err)
		loadError[catalog] = true
	} finally {
		loading[catalog] = false
	}
}

watch(
	tab,
	(newTab) => {
		if (!loaded[newTab] && !loading[newTab]) {
			fetchCategory(newTab)
		}
	},
	{ immediate: true }
)

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
