<template>
  <div class="feature-card">
    <h3>{{ title }}</h3>
    <p>{{ description }}</p>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      required: true
    },
    description: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
.feature-card {
  padding: 2rem;
  text-align: center;
  background-color: #f8f9fa;
  border-radius: 10px;
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
}
</style>
