# Kolekcje - Collections Management Application

A Vue.js/Nuxt.js application for organizing personal collections including books, music albums, and movies.

## About

Kolekcje is a comprehensive collection management system that helps users organize and track their personal collections. The application currently focuses on book management with plans to expand to music albums and movies.

### Look

![Kolekcje Application Screenshot](kolekcje.png)

*The main interface of Kolekcje showing the clean, intuitive design for managing your book collections with easy navigation and search functionality.*

### Features

- **Book Management**: Add, search, and organize your book collection
- **Advanced Search**: Search by title, author, publisher, or series
- **Detailed Book Information**: Track ISBN, publication details, genres, series, and personal notes
- **Multi-language Support**: Available in multiple languages
- **Responsive Design**: Works seamlessly on desktop and mobile devices

### Current Version

**Version**: 0.9.2

## Technology Stack

### Frontend

- **Frontend**: Vue.js 3 with Nuxt.js
- **Internationalization**: Vue i18n
- **Styling**: Scoped CSS with responsive design

### Backend

- **API**: Python with Flask framework
- **Database**: MariaDB for data persistence
- **Reverse Proxy**: nginx for HTTP traffic routing and load balancing
- **Architecture**: RESTful API design with nginx routing requests between frontend and backend services

## Setup

Make sure to install dependencies:

```bash
docker compose up
```