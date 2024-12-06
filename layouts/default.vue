<template>
  <div class="app-container">
    <LeftMenu />
    <main class="main-content">
      <slot />
    </main>
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
}

.main-content {
  margin-left: 250px;
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
    margin-top: 80px;
  }
}
</style>
