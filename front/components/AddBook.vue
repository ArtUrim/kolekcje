<template>
	<v-container>
		<v-card class="pa-4">
			<v-form ref="form" v-model="valid">
				<v-row>
					<v-col cols="12" sm="6">
						<v-text-field v-model="isbn" :label="$t('addBook.isbn')" :rules="isbnRules"
															  hint="10 or 13 characters"></v-text-field>
					</v-col>

					<v-col cols="12" sm="6">
						<v-text-field v-model="title" :label="$t('addBook.title')" :rules="titleRules" required></v-text-field>
					</v-col>

					<v-col cols="12" sm="6">
						<MultiAutocompleteField
								v-model="author"
								:label="$t('addBook.author')"
								:placeholder="$t('addBook.placeholders.author')"
								api-endpoint="/api/authors"
								/>
					</v-col>

					<v-col cols="12" sm="6">
						<MultiAutocompleteField
								v-model="publisher"
								:label="$t('addBook.publisher')"
								:placeholder="$t('addBook.placeholders.publisher')"
								api-endpoint="/api/publishers"
								/>
					</v-col>

					<v-col cols="12" sm="6">
						<GenreCheck v-model="genre" :label="$t('addBook.genre')" :placeholder="$t('addBook.placeholders.genre')"
																				  api-endpoint="/api/genres" />
					</v-col>


					<v-col cols="12" sm="6">
						<v-text-field
								v-model="publishYear"
								:label="$t('addBook.publishYear')"
								type="number"
								:rules="yearRules"
								></v-text-field>
					</v-col>

					<v-col cols="12" sm="6">
						<v-text-field
								v-model="firstPublishYear"
								:label="$t('addBook.firstPublishYear')"
								type="number"
								:rules="yearRules"
								></v-text-field>
					</v-col>

					<v-col cols="12" sm="6">
						<v-select
								v-model="format"
								:items="formatOptions"
								:label="$t('addBook.format')"
								></v-select>
					</v-col>

					<v-col cols="12" sm="6">
						<v-text-field
								v-model="pages"
								:label="$t('addBook.pages')"
								type="number"
								:rules="pagesRules"
								></v-text-field>
					</v-col>

					<v-col cols="12">
						<v-textarea
								v-model="description"
								:label="$t('addBook.description')"
								rows="3"
								></v-textarea>
					</v-col>

					<v-col cols="12">
						<v-textarea
								v-model="notes"
								:label="$t('addBook.notes')"
								rows="3"
								></v-textarea>
					</v-col>

					<v-col cols="12" sm="6">
						<AutocompleteField v-model="series" :label="$t('addBook.series')" :placeholder="$t('addBook.placeholders.series')"
																							api-endpoint="/api/series" />
					</v-col>

					<v-col cols="12" sm="6">
						<v-text-field
								v-model="originalTitle"
								:label="$t('addBook.originalTitle')"
								></v-text-field>
					</v-col>

					<v-col cols="12" sm="6">
						<v-text-field
								v-model="translator"
								:label="$t('addBook.translator')"
								></v-text-field>
					</v-col>

					<v-col cols="12" sm="6">
						<v-text-field
								v-model="language"
								:label="$t('addBook.language')"
								></v-text-field>
					</v-col>
				</v-row>

				<v-card-actions class="pt-4">
					<v-spacer></v-spacer>
					<v-btn color="info" @click="verifyForm">
						{{ $t('addBook.buttons.verify') }}
					</v-btn>
					<v-btn color="grey" text @click="resetForm">
						{{ $t('addBook.buttons.reset') }}
					</v-btn>
					<v-btn color="primary" :disabled="!valid" @click="submitForm">
						{{ $t('addBook.buttons.submit') }}
					</v-btn>
				</v-card-actions>
			</v-form>
		</v-card>
	</v-container>
	<v-snackbar
		v-model="snackbar.show"
		:color="snackbar.color"
		:timeout="5000"
		top
		right
	>
		{{ snackbar.message }}
		<template v-slot:actions>
			<v-btn
				color="white"
				text
				@click="snackbar.show = false"
			>
				{{ $t('addBook.buttons.close') }}
			</v-btn>
		</template>
	</v-snackbar>
</template>

<script>
export default {

	data: () => ({
		valid: false,
		snackbar: {
			show: false,
			message: '',
			color: 'success'
		},
		isbn: '',
		title: '',
		author: [],
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
		showSnackbar(message, color = 'success') {
			this.snackbar.message = message;
			this.snackbar.color = color;
			this.snackbar.show = true;
		},

		verifyForm() {
			this.$refs.form.validate()
		},

		async submitForm() {
			if (this.$refs.form.validate()) {
				const bookData = {
					isbn: this.isbn ? parseInt(this.isbn) : null,
					title: this.title,
					publishYear: this.publishYear ? parseInt(this.publishYear) : null,
					firstPublishYear: this.firstPublishYear ? parseInt(this.firstPublishYear) : null,
					format: this.format,
					pages: this.pages ? parseInt(this.pages) : null,
					description: this.description,
					notes: this.notes,
					originalTitle: this.originalTitle,
					translator: this.translator,
					language: this.language,
				};

				// Process genre array - handle both objects and strings
				if (this.genre && this.genre.length > 0) {
					bookData.genre = this.genre.map(item => {
						// Check if the item is an object
						if (typeof item === 'object' && item !== null) {
							return {
								id: item.id,
								title: item.title,
								isCustom: false
							};
						}
						// If it's a string, create object format
						else if (typeof item === 'string') {
							return {
								id: null,
								title: item,
								isCustom: true
							};
						}
						// Fallback for any other type
						return {
							id: null,
							title: String(item),
							isCustom: true
						};
					});
				}

				// Process publisher array - extract IDs and titles
				if (this.publisher && this.publisher.length > 0) {
					bookData.publisher = this.publisher.map(pub => ({
						id: pub.id,
						title: pub.title,
						isCustom: pub.isCustom
					}));
				}

				// Process author array - extract IDs and titles
				if (this.author && this.author.length > 0) {
					bookData.author = this.author.map(pub => ({
						id: pub.id,
						title: pub.title,
						isCustom: pub.isCustom
					}));
				}

				// Process series object - extract ID and title
				if (this.series) {
					bookData.series= {
						id: this.series.id,
						title: this.series.title,
						isCustom: this.series.isCustom
					};
				}
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
						this.showSnackbar(this.$t('addBook.messages.bookAddedSuccess'), 'success');
						this.resetForm();
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
					this.showSnackbar(this.$t('addBook.messages.errorAddingBook', { message: err.message }), 'error');
				}
			}
		},

		resetForm() {
			// Reset form validation
			this.$refs.form.reset();

			// Manually clear all form fields
			this.isbn = '';
			this.title = '';
			this.author = [];
			this.publishYear = '';
			this.firstPublishYear = '';
			this.format = 'unknown';
			this.publisher = [];
			this.pages = '';
			this.description = '';
			this.notes = '';
			this.series = '';
			this.originalTitle = '';
			this.translator = '';
			this.language = '';
			this.genre = [];
		},

	}
}
</script>
