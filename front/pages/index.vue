<template>
  <div>
    <section class="hero" id="home">
      <div class="hero-content">
			<h1>{{ $t('welcome') }}</h1>
        <p>{{ $t('shortDescription') }}</p>
		  <NuxtLink to="/contact" class="cta-button">{{ $t('contact') }}</NuxtLink>
      </div>
    </section>

  </div>
</template>

<script setup>
</script>
