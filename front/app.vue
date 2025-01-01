<template>
  <div>
	  <NuxtLayout>
	  	<NuxtPage />
	  </NuxtLayout>
  </div>
</template>

<script setup>
	const { $api } = useNuxtApp()
	const { data: book } = await useAsyncData('book', () => $api('/book'))
</script>

