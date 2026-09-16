<template>
  <nav class="left-menu">
    <div class="menu-icon">
      <span></span>
      <span></span>
      <span></span>
    </div>
    <div class="logo">
      <h2>Kolekcje</h2>
    </div>
    <ul class="nav-links">
		 <li><NuxtLink :to="localePath('/')">{{ $t('leftMenu.home') }}</NuxtLink></li>
		 <li><NuxtLink :to="localePath('/books')">{{ $t('leftMenu.books') }}</NuxtLink></li>
		<li v-if="showAddBook">
        <NuxtLink :to="localePath('/addbook')" class="small-text indent-left">
		  {{ $t('leftMenu.addBook') }}
		  </NuxtLink>
      </li>
		<li><NuxtLink :to="localePath('/contact')">{{ $t('contact') }}</NuxtLink></li>
	
		<li> <NuxtLink :to="switchLocalePath('pl')">Polski</NuxtLink></li>
		<li> <NuxtLink :to="switchLocalePath('en')">English</NuxtLink></li>
		<li> <NuxtLink :to="switchLocalePath('it')">Italiano</NuxtLink></li>

		<button @click="triggerRestart" class="btn-danger">
			{{ $t('leftMenu.shutdown') }}
		</button>
    </ul>
  </nav>
</template>

<script setup>
const route = useRoute()

const switchLocalePath = useSwitchLocalePath()
const localePath = useLocalePath()

const { userRole, triggerRestart } =  useNetworkAdmin();

const showAddBook = computed(() => {
  return [localePath('/books'), localePath('/addbook')].includes(route.path)
})
</script>

<style scoped>
.left-menu {
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  width: 40px;
  background-color: #2c3e50;
  color: white;
  padding: 2rem 0;
  z-index: 1000;
  overflow: hidden;
  transition: width 0.3s ease;
}

.left-menu:hover {
  width: 250px;
  padding: 2rem;
}

.menu-icon {
  position: absolute;
  top: 1rem;
  left: 0;
  width: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  opacity: 1;
  transition: opacity 0.2s ease;
}

.menu-icon span {
  display: block;
  width: 20px;
  height: 2px;
  background-color: white;
}

.left-menu:hover .menu-icon {
  opacity: 0;
  pointer-events: none;
}

.logo {
  margin-bottom: 3rem;
  text-align: center;
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.left-menu:hover .logo {
  opacity: 1;
}

.nav-links {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.left-menu:hover .nav-links {
  opacity: 1;
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
  .left-menu,
  .left-menu:hover {
    width: 100%;
    height: auto;
    padding: 1rem;
  }

  .logo,
  .nav-links {
    opacity: 1;
    white-space: normal;
  }

  .menu-icon {
    display: none;
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

.btn-danger {
	background: #ef4444;
}

.btn-danger:hover {
	background: #dc2626;
}

</style>
