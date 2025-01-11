<template>
  <nav class="left-menu">
    <div class="logo">
      <h2>Kolekcje</h2>
    </div>
    <ul class="nav-links">
      <li><NuxtLink to="/">Home</NuxtLink></li>
      <li><NuxtLink to="/books">Książki</NuxtLink></li>
		<li v-if="showAddBook">
        <NuxtLink to="/addbook" class="small-text indent-left">Dodaj</NuxtLink>
      </li>
      <li><NuxtLink to="/contact">Kontakt</NuxtLink></li>
    </ul>
  </nav>
</template>

<script setup>
const route = useRoute()

const showAddBook = computed(() => {
  return ['/books', '/addbook'].includes(route.path)
})
</script>

<style scoped>
.left-menu {
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  width: 250px;
  background-color: #2c3e50;
  color: white;
  padding: 2rem;
  z-index: 1000;
}

.logo {
  margin-bottom: 3rem;
  text-align: center;
}

.nav-links {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-size: 1.1rem;
  transition: color 0.3s;
}

.nav-links a:hover {
  color: #3498db;
}

@media (max-width: 768px) {
  .left-menu {
    width: 100%;
    height: auto;
    padding: 1rem;
  }

  .logo {
    margin-bottom: 1rem;
  }

  .nav-links {
    flex-direction: row;
    justify-content: center;
  }
}

.small-text {
  font-size: 0.85em;
  list-style-type: disc;
  color: black;
}

.indent-left {
  margin-left: 1rem; /* You can adjust this value to move it more or less */
}
</style>
