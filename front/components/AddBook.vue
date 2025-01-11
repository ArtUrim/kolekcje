<template>
  <v-container>
    <v-card class="pa-4">
      <v-form ref="form" v-model="valid">
        <v-row>
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="isbn"
              label="ISBN"
              :rules="isbnRules"
              hint="10 or 13 characters"
            ></v-text-field>
          </v-col>

          <v-col cols="12" sm="6">
            <v-text-field
              v-model="title"
              label="Tytuł"
              :rules="titleRules"
              required
            ></v-text-field>
          </v-col>

          <v-col cols="12" sm="6">
            <v-text-field
              v-model="author"
              label="Autor"
            ></v-text-field>
          </v-col>

          <v-col cols="12" sm="6">
            <v-text-field
              v-model="publishYear"
              label="Data wydania"
              type="number"
              :rules="yearRules"
            ></v-text-field>
          </v-col>

          <v-col cols="12" sm="6">
            <v-text-field
              v-model="firstPublishYear"
              label="Data pierwszego wydania"
              type="number"
              :rules="yearRules"
            ></v-text-field>
          </v-col>

          <v-col cols="12" sm="6">
            <v-select
              v-model="format"
              :items="formatOptions"
              label="Format"
            ></v-select>
          </v-col>

          <v-col cols="12" sm="6">
            <v-autocomplete
              v-model="publisher"
              :items="publisherHints"
              label="Wydawca"
              :search-input.sync="publisherSearch"
              clearable
              @update:search-input="searchPublisher"
            ></v-autocomplete>
          </v-col>

          <v-col cols="12" sm="6">
            <v-text-field
              v-model="pages"
              label="Liczba stron"
              type="number"
              :rules="pagesRules"
            ></v-text-field>
          </v-col>

          <v-col cols="12">
            <v-textarea
              v-model="description"
              label="Opis"
              rows="3"
            ></v-textarea>
          </v-col>

          <v-col cols="12">
            <v-textarea
              v-model="notes"
              label="Uwagi"
              rows="3"
            ></v-textarea>
          </v-col>

          <v-col cols="12" sm="6">
            <v-text-field
              v-model="series"
              label="Seria"
            ></v-text-field>
          </v-col>

          <v-col cols="12" sm="6">
            <v-text-field
              v-model="originalTitle"
              label="Tytuł oryginalny"
            ></v-text-field>
          </v-col>

          <v-col cols="12" sm="6">
            <v-text-field
              v-model="translator"
              label="Tłumacz"
            ></v-text-field>
          </v-col>

          <v-col cols="12" sm="6">
            <v-text-field
              v-model="language"
              label="Język"
            ></v-text-field>
          </v-col>
        </v-row>

        <v-card-actions class="pt-4">
          <v-spacer></v-spacer>
          <v-btn
            color="info"
            @click="verifyForm"
          >
            Verify
          </v-btn>
          <v-btn
            color="grey"
            text
            @click="resetForm"
          >
            Reset
          </v-btn>
          <v-btn
            color="primary"
            :disabled="!valid"
            @click="submitForm"
          >
            Submit
          </v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    valid: false,
    isbn: '',
    title: '',
    author: '',
    publishYear: '',
    firstPublishYear: '',
    format: 'unknown',
    publisher: '',
    publisherSearch: null,
    publisherHints: [],
    pages: '',
    description: '',
    notes: '',
    series: '',
    originalTitle: '',
    translator: '',
    language: '',

    formatOptions: [
      { text: 'Unknown', value: 'unknown' },
      { text: 'Hardback', value: 'hardback' },
      { text: 'Paperback', value: 'paperback' },
      { text: 'Ebook', value: 'ebook' }
    ],

    isbnRules: [
      v => !v || [10, 13].includes(v.length) || 'ISBN must be 10 or 13 characters'
    ],
    titleRules: [
      v => !!v || 'Title is required'
    ],
    yearRules: [
      v => !v || (parseInt(v) > 1000 && parseInt(v) <= new Date().getFullYear()) || 
        'Year must be valid'
    ],
    pagesRules: [
      v => !v || (parseInt(v) > 0) || 'Pages must be positive number'
    ]
  }),

  methods: {
    async searchPublisher(val) {
      if (val && val.length > 2) {
        try {
          const response = await fetch(`/api/series/hint?q=${val}`)
          const data = await response.json()
          this.publisherHints = data
        } catch (error) {
          console.error('Error fetching publisher hints:', error)
        }
      }
    },

    verifyForm() {
      this.$refs.form.validate()
    },

    async submitForm() {
      if (this.$refs.form.validate()) {
        console.log('Form submitted:', {
          isbn: this.isbn,
          title: this.title,
          author: this.author,
          publishYear: this.publishYear,
          firstPublishYear: this.firstPublishYear,
          format: this.format,
          publisher: this.publisher,
          pages: this.pages,
          description: this.description,
          notes: this.notes,
          series: this.series,
          originalTitle: this.originalTitle,
          translator: this.translator,
          language: this.language
        })
		  try {
		  	
		  	const { data, error } = await useAPI( "/addbook" )

		  	if (error.value) {
		 	 	throw new Error(error.value.message);
		  	}

		  	if (data.value) {
		  	items.value = data.value.books;
		  	totalItems.value = data.value.count;
		  	}
		  } catch (err) {
		  	console.error('Error fetching books:', err);
		  	// Handle error appropriately
		  } finally {
		  	loading.value = false;
		  }
      }
    },

    resetForm() {
      this.$refs.form.reset()
    }
  }
}
</script>
