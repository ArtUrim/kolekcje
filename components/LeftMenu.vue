<template>
  <nav class="left-menu">
    <div class="logo">
      <h2>Logo</h2>
    </div>
    <ul class="nav-links">
      <li><NuxtLink to="/">Home</NuxtLink></li>
      <li><NuxtLink to="#features">Features</NuxtLink></li>
      <li><NuxtLink to="/books">Books</NuxtLink></li>
      <li><NuxtLink to="/contact">Contact</NuxtLink></li>
    </ul>
  </nav>
</template>

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
</style>
