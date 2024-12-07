<template>
  <v-card title="Nutrition" flat >
    <template v-slot:text>
      <v-text-field
        v-model="search"
        label="Search"
        prepend-inner-icon="mdi-magnify"
        variant="outlined"
        hide-details
        single-line
      ></v-text-field>
    </template>

    <v-data-table
      :headers="headers"
      :items="books"
      :search="search"
    ></v-data-table>
  </v-card>
</template>

<script>  
export default {  
  name: "BooksTable",  
  data() {  
    return {  
      // Table headers  
		search: '',
      headers: [  
        { title: "Tytuł", value: "title", sortable: true },  
        { title: "Autor", value: "author", sortable: true },  
        { title: "Rok wydania", value: "year", sortable: true },  
        { title: "Wydawnictwo", value: "publisher", sortable: true },  
      ],  
      // Table data  
      books: [  
        {  
          title: "Wyznania",  
          author: "Augustyn",  
          year: 485,  
          publisher: "rękopis",  
        },  
        {  
          title: "Boska Komedia",  
          author: "Dante Alighieri",  
          year: 1320,  
          publisher: "rękopis",  
        },  
        {  
          title: "Hamlet",  
          author: "William Shakespeare",  
          year: 1603,  
          publisher: "First Folio",  
        },  
      ],  
    };  
  },  
};  
</script>  

<style scoped>  
/* Optional: Add custom styles if needed */  
</style>  
