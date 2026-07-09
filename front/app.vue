<template>
  <div>
	  <NuxtLayout>
	  	<NuxtPage />
	  </NuxtLayout>
  </div>
</template>

<script setup>
	const { $api } = useNuxtApp()
	const { startHeartbeat } = useHeartbeat()

onMounted(() => {
  startHeartbeat()
})
</script>

