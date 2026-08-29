<template>
  <div>
    <section class="hero" id="home">
      <div class="hero-content">
			<h1>{{ $t('welcome') }} <span class="highlight-text">kolekcje</span></h1>
         <p>{{ $t('shortDescription') }}</p>
		   <NuxtLink to="/contact" class="cta-button">{{ $t('contact') }}</NuxtLink>
      </div>
    </section>

  </div>
</template>

<script setup>
</script>

<style scoped>
/* Apply using a class name */
.highlight-text {
  font-size: 5rem; /* Makes text ~25% larger than normal body size */
  color: #A8C3BC;     /* Changes text color (HEX code) */
}

</style>
