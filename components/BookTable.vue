<template>  
  <div class="table-container">  
    <table>  
      <thead>  
        <tr>  
          <th @click="sort('title')">  
            Tytuł  
            <span class="sort-icon">{{ getSortIcon('title') }}</span>  
          </th>  
          <th @click="sort('author')">  
            Autor  
            <span class="sort-icon">{{ getSortIcon('author') }}</span>  
          </th>  
          <th @click="sort('year')">  
            Rok wydania  
            <span class="sort-icon">{{ getSortIcon('year') }}</span>  
          </th>  
          <th @click="sort('publisher')">  
            Wydawnictwo  
            <span class="sort-icon">{{ getSortIcon('publisher') }}</span>  
          </th>  
        </tr>  
      </thead>  
      <tbody>  
        <tr v-for="(book, index) in sortedBooks" :key="index">  
          <td>{{ book.title }}</td>  
          <td>{{ book.author }}</td>  
          <td>{{ book.year }}</td>  
          <td>{{ book.publisher }}</td>  
        </tr>  
      </tbody>  
    </table>  
  </div>  
</template>  

<script>  
export default {  
  name: 'BooksTable',  
  data() {  
    return {  
      books: [  
        {  
          title: "Wyznania",  
          author: "Augustyn",  
          year: 485,  
          publisher: "rękopis"  
        },  
        {  
          title: "Boska Komedia",  
          author: "Dante Alighieri",  
          year: 1320,  
          publisher: "rękopis"  
        },  
        {  
          title: "Hamlet",  
          author: "William Shakespeare",  
          year: 1603,  
          publisher: "First Folio"  
        }  
      ],  
      sortKey: null,  
      sortOrder: 1 // 1 for ascending, -1 for descending  
    }  
  },  
  computed: {  
    sortedBooks() {  
      if (!this.sortKey) return this.books  

      return [...this.books].sort((a, b) => {  
        let valueA = a[this.sortKey]  
        let valueB = b[this.sortKey]  

        if (typeof valueA === 'string') valueA = valueA.toLowerCase()  
        if (typeof valueB === 'string') valueB = valueB.toLowerCase()  

        if (valueA < valueB) return -1 * this.sortOrder  
        if (valueA > valueB) return 1 * this.sortOrder  
        return 0  
      })  
    }  
  },  
  methods: {  
    sort(key) {  
      if (this.sortKey === key) {  
        this.sortOrder *= -1  
      } else {  
        this.sortKey = key  
        this.sortOrder = 1  
      }  
    },  
    getSortIcon(key) {  
      if (this.sortKey !== key) return '⇕'  
      return this.sortOrder === 1 ? '↑' : '↓'  
    }  
  }  
}  
</script>  

<style scoped>  
.table-container {  
  margin: 20px;  
  font-family: Arial, sans-serif;  
}  

table {  
  width: 100%;  
  border-collapse: collapse;  
  background-color: white;  
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);  
}  

th, td {  
  padding: 12px 15px;  
  text-align: left;  
  border-bottom: 1px solid #ddd;  
}  

th {  
  background-color: #f5f5f5;  
  font-weight: bold;  
  color: #333;  
  text-transform: uppercase;  
  font-size: 0.9em;  
  cursor: pointer;  
  user-select: none;  
}  

th:hover {  
  background-color: #ebebeb;  
}  

.sort-icon {  
  margin-left: 5px;  
  font-size: 0.8em;  
}  

tr:hover {  
  background-color: #f8f8f8;  
}  

tbody tr:nth-child(even) {  
  background-color: #f9f9f9;  
}  

/* Responsive design */  
@media screen and (max-width: 600px) {  
  table {  
    display: block;  
    overflow-x: auto;  
  }  

  th, td {  
    min-width: 120px;  
  }  
}  
</style>  
