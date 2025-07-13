<template>
	<v-container>
		<v-card class="pa-4">
			<v-form ref="form" v-model="valid">
				<v-row>
					<v-col cols="12" sm="6">
						<v-text-field v-model="isbn" label="ISBN" :rules="isbnRules"
							hint="10 or 13 characters"></v-text-field>
					</v-col>

					<v-col cols="12" sm="6">
						<v-text-field v-model="title" label="Tytuł" :rules="titleRules" required></v-text-field>
					</v-col>

					<v-col cols="12" sm="6">
						<GenreCheck v-model="genre" label="gatunek" placeholder="Select or add a series"
							api-endpoint="/api/genres" />
					</v-col>

					<v-col cols="12" sm="6">
						<MultiAutocompleteField
							v-model="publisher"
							label="Publisher"
							placeholder="Select or add a publisher"
							api-endpoint="/api/publishers"
						/>
					</v-col>

					<!--

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
		          -->

					<v-col cols="12" sm="6">
						<AutocompleteField v-model="series" label="Series" placeholder="Select or add a series"
							api-endpoint="/api/series" />
					</v-col>

					<!--

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
        -->
				</v-row>

				<v-card-actions class="pt-4">
					<v-spacer></v-spacer>
					<v-btn color="info" @click="verifyForm">
						Verify
					</v-btn>
					<v-btn color="grey" text @click="resetForm">
						Reset
					</v-btn>
					<v-btn color="primary" :disabled="!valid" @click="submitForm">
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
		publisher: [],
		pages: '',
		description: '',
		notes: '',
		series: '',
		originalTitle: '',
		translator: '',
		language: '',
		genre: [],
		genreProp: ['proza', 'poezja'],

		formatOptions: [
			'unknown',
			'hardback',
			'paperback',
			'ebook'
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

		verifyForm() {
			this.$refs.form.validate()
		},

		async submitForm() {
			if (this.$refs.form.validate()) {
				const bookData = {
					isbn: this.isbn,
					title: this.title,
					author: this.author,
					publishYear: this.publishYear,
					firstPublishYear: this.firstPublishYear,
					format: this.format,
					pages: this.pages,
					description: this.description,
					notes: this.notes,
					originalTitle: this.originalTitle,
					translator: this.translator,
					language: this.language,
				};
				console.log("genre ", this.genre)
				console.log("series ", this.series)
				console.log("wydawca ", this.publisher)
				bookData.publisher = this.publisher;
				console.log('Form submitted:', bookData)
				try {
					const response = await fetch('/api/addbook', {
						method: 'POST',
						headers: {
							'Content-Type': 'application/json'
						},
						body: JSON.stringify(bookData)
					});

					if (response.status === 204) {
						// Success case - status 204 No Content
						console.log('Book added successfully');
						// You might want to add user feedback here, like:
						// this.$emit('book-added') or show a success message
						return;
					}

					// For non-204 responses, try to parse response body
					const data = await response.json();

					if (!response.ok) {
						throw new Error(data.message || `Error adding book (Status: ${response.status})`);
					}

					// Handle other successful responses (if any)
					console.log('Book added with response:', data);

				} catch (err) {
					console.error('Error adding book:', err);
					// You might want to add user feedback here, like:  
					// this.$emit('error', err.message) or show an error message
				}
			}
		},

		resetForm() {
			this.$refs.form.reset()
		},

	}
}
</script>
