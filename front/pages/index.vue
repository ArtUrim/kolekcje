<template>
  <div>
    <section class="hero" id="home">
      <div class="hero-content">
			<h1>{{ $t('welcome') }}</h1>
        <p>Aplikacja służaca do porządkowania kolekcji (ksiązek, płyt z muzyką i filmów).</p>
		  <NuxtLink to="/contact" class="cta-button">{{ $t('contact') }}</NuxtLink>
      </div>
    </section>

  </div>
</template>

<script setup>
</script>
