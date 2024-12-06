<template>
  <div>
    <section class="hero" id="home">
      <div class="hero-content">
        <h1>Welcome to Our Amazing Platform</h1>
        <p>Discover the best solutions for your needs with our innovative products and services.</p>
        <NuxtLink to="/contact" class="cta-button">Get Started</NuxtLink>
      </div>
    </section>

    <section class="features" id="features">
      <h2>Our Features</h2>
      <div class="features-grid">
        <FeatureCard
          v-for="(feature, index) in features"
          :key="index"
          :title="feature.title"
          :description="feature.description"
        />
      </div>
    </section>
  </div>
</template>

<script>
export default {
  data() {
    return {
      features: [
        {
          title: 'Feature 1',
          description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        },
        {
          title: 'Feature 2',
          description: 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
        },
        {
          title: 'Feature 3',
          description: 'Ut enim ad minim veniam, quis nostrud exercitation ullamco.'
        }
      ]
    }
  }
}
</script>
