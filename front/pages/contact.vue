<template>
  <div class="grid-container">
    <div class="centered-content">
      <h2>{{ $t('contact') }}</h2>

      <div class="contact-details">
        <div class="contact-item">
          <strong>{{ $t('contactInfo.author') }}:</strong>
          <span><h2>Artur Łoziński</h2></span>
        </div>

        <div class="contact-item">
          <strong>{{ $t('contactInfo.email') }}:</strong>
          <a href="mailto:lozinski.artur@gmail.com" class="email-link">
            lozinski.artur@gmail.com
          </a>
        </div>

        <div class="contact-item">
          <strong>{{ $t('contactInfo.repository') }}:</strong>
          <a
            href="https://gitlab.com/ArtUrim/kolekcje.git"
            target="_blank"
            rel="noopener noreferrer"
            class="repo-link"
          >
            https://gitlab.com/ArtUrim/kolekcje.git
          </a>
        </div>

        <div class="contact-item">
          <strong>{{ $t('contactInfo.version') }}:</strong>
          <span class="version">0.9.2</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.grid-container {
  display: grid;
  place-items: center;
  min-height: 100vh;
  padding: 20px;
}

.centered-content {
  text-align: center;
  padding: 20px;
  max-width: 600px;
  width: 100%;
}

.contact-details {
  margin-top: 2rem;
  text-align: left;
}

.contact-item {
  display: flex;
  flex-direction: column;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background-color: rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.contact-item:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.contact-item strong {
  margin-bottom: 0.5rem;
  color: #333;
  font-size: 1.1rem;
}

.contact-item span {
  color: #666;
  font-size: 1rem;
}

.email-link,
.repo-link {
  color: #1976d2;
  text-decoration: none;
  transition: color 0.3s ease;
  word-break: break-all;
}

.email-link:hover,
.repo-link:hover {
  color: #1565c0;
  text-decoration: underline;
}

.version {
  font-family: 'Courier New', monospace;
  background-color: #e8f5e8;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-weight: bold;
  color: #2e7d32;
}

@media (max-width: 768px) {
  .centered-content {
    padding: 1rem;
  }

  .contact-item {
    padding: 0.75rem;
  }

  .repo-link {
    font-size: 0.9rem;
  }
}
</style>
