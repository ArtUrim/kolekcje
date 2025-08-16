<template>
  <v-container fluid class="pa-6">
    <!-- Page Header    <v-row class="mb-6">
      <v-col cols="12">
        <h1 class="text-h3 text-center mb-4">Expandable Text Components</h1>
        <p class="text-h6 text-center text-medium-emphasis">
          Compare different Vuetify expandable text component variations
        </p>
      </v-col>
    </v-row>
    -->

    <!-- Custom Card Components with Transitions -->
    <v-row class="mb-8">
      <v-col cols="12">
        <!--
        <h2 class="text-h4 mb-4">
          <v-icon left color="success">mdi-card-multiple</v-icon>
          Custom Cards with Advanced Transitions
        </h2>
      -->
        <v-row>
          <v-col
            v-for="(card, index) in processedCards"
            :key="index"
            cols="12"
            md="6"
            lg="4"
          >
            <expandable-text
              :card="card"
              @toggle-expanded="handleToggleExpanded"
            />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>

export default {
  props: {
    cards: {
      type: Array,
      required: true
    }
  },
  computed: {
    processedCards() {
      return this.cards.map(card => ({
        title: card.title || 'Untitled',
        headerColor: card.headerColor || 'lightblue',
        icon: card.icon || 'mdi-book-open-variant',
        shortText: card.shortText || card.description || `${card.authors || 'Unknown Author'} - ${card.genres || 'No genre specified'}`,
        expandedText: card.expandedText || '',
        tags: card.tags || [],
        progress: card.progress !== undefined ? card.progress : 100,
        expanded: card.expanded || false,
        ...card
      }))
    }
  },
  setup() {

    const handleToggleExpanded = (card) => {
      card.expanded = !card.expanded
    }

    return {
      handleToggleExpanded
    }
  }
}
</script>

<style scoped>
.v-expansion-panel-title {
  font-weight: 500;
}

h1, h2 {
  font-weight: 700;
}
</style>