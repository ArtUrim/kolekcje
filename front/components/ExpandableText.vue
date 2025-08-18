<template>
  <div class="expandable-text-wrapper">
    <v-hover v-slot="{ isHovering, props }">
      <v-card
        v-bind="props"
        :elevation="isHovering ? 8 : 2"
        :class="{ 'on-hover': isHovering }"
        rounded="xl"
        class="transition-swing mb-4"
      >
      <v-card-title
        :class="`bg-${card.headerColor}`"
        class="white--text rounded-t-xl py-2"
      >
        <v-icon left color="white" x-small>{{ card.icon }}</v-icon>
        <span class="text-subtitle-2 font-weight-small">{{ card.title }}</span>
      </v-card-title>

      <v-card-text class="pa-4">
        <p class="mb-3 text-h6">{{ card.shortText }}</p>

        <!-- Progress indicator if applicable
        <v-progress-linear
          v-if="card.progress"
          :color="card.headerColor"
          :model-value="card.progress"
          height="6"
          rounded
          class="mb-3"
        ></v-progress-linear>
      -->

        <v-expand-transition>
          <div v-show="card.expanded" class="mt-3">
            <v-divider class="mb-3"></v-divider>
            <p class="mb-3">{{ card.expandedText }}</p>

            <!-- Additional content based on type -->
            <v-chip-group v-if="card.tags" class="mb-3">
              <v-chip 
                v-for="tag in card.tags"
                :key="tag"
                :color="card.headerColor"
                size="small"
                variant="outlined"
              >
                {{ tag }}
              </v-chip>
            </v-chip-group>
          </div>
        </v-expand-transition>
      </v-card-text>

      <!--
      <v-card-actions class="px-4 pb-4">
        <v-btn
          :color="card.headerColor"
          variant="outlined"
          rounded
          @click="toggleExpanded"
        >
          <v-icon left>
            {{ card.expanded ? 'mdi-eye-off' : 'mdi-eye' }}
          </v-icon>
          {{ card.expanded ? 'Collapse' : 'Expand' }}
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn 
          :color="card.headerColor"
          variant="text"
          icon
          size="small"
        >
          <v-icon>mdi-heart-outline</v-icon>
        </v-btn>
        <v-btn 
          :color="card.headerColor"
          variant="text"
          icon
          size="small"
        >
          <v-icon>mdi-share-variant</v-icon>
        </v-btn>
      </v-card-actions>
    -->
      </v-card>
    </v-hover>
  </div>
</template>

<script>
export default {
  name: 'ExpandableText',
  props: {
    card: {
      type: Object,
      required: true
    }
  },
  emits: ['toggle-expanded'],
  methods: {
    toggleExpanded() {

      this.$emit('toggle-expanded', this.card);
    }
  }
}
</script>

<style scoped>
.expandable-text-wrapper {
  /* Wrapper to handle attribute inheritance properly */
}

.v-card.on-hover {
  opacity: 0.9;
  transform: translateY(-2px);
}

.transition-swing {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.v-card-title {
  font-weight: 600;
}
</style>