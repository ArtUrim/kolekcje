<template>
  <v-data-table
    :headers="headers"
    :items="movies"
    item-value="title"
    show-expand
  >
    <template v-slot:item.data-table-expand="{ internalItem, isExpanded, toggleExpand }">
      <v-btn
        :append-icon="isExpanded(internalItem) ? 'mdi-chevron-up' : 'mdi-chevron-down'"
        :text="isExpanded(internalItem) ? 'Collapse' : 'More info'"
        class="text-none"
        color="medium-emphasis"
        size="small"
        variant="text"
        width="105"
        border
        slim
        @click="toggleExpand(internalItem)"
      ></v-btn>
    </template>

    <template v-slot:expanded-row="{ columns, item }">
      <tr>
        <td :colspan="columns.length" class="py-2">
          <v-sheet rounded="lg" border>
            <v-table density="compact">
              <tbody class="bg-surface-light">
                <tr>
                  <th>ISBN</th>
                  <th>Labels</th>
                  <th>Language</th>
                  <th>Pages</th>
                  <th>Publisher(s)</th>
                  <th>Size</th>
                </tr>
              </tbody>

              <tbody>
                <tr>
                  <td class="py-2">{{ item.isbn || 'N/A' }}</td>
                  <td class="py-2">{{ item.labels || 'N/A' }}</td>
                  <td class="py-2">{{ item.language_name || 'N/A' }}</td>
                  <td class="py-2">{{ item.pages || 'N/A' }}</td>
                  <td class="py-2">{{ item.publishers || 'N/A' }}</td>
                  <td class="py-2">{{ item.size || 'N/A' }}</td>
                </tr>
              </tbody>
            </v-table>
          </v-sheet>
        </td>
      </tr>
    </template>
  </v-data-table>
</template>
<script setup>
  const headers = [
    { width: 300, title: 'Title', key: 'title', align: 'start', sortable: true },
    { width: 250, title: 'Author(s)', key: 'authors' },
    { width: 150, title: 'Genre', key: 'genres' },
    { width: 100, title: 'Year', key: 'release_date', align: 'end' },
    { width: 140, title: 'Serie', key: 'series_name', align: 'end' },
    { width: 1, key: 'data-table-expand', align: 'end' }, // optional, to keep it as short as possible
  ]

const movies = [
  {
    "authors": "Pawe\u0142 Pompa",
    "authors_details": [
      {
        "birth_date": null,
        "death_date": null,
        "description": null,
        "id": 2,
        "name": "Pawe\u0142 Pompa",
        "nationality_id": "pl_",
        "note": null
      }
    ],
    "description": null,
    "first_polish_release_date": 2022,
    "format": "hardback",
    "genres": "j\u0119zyki, orientalia",
    "genres_details": [
      {
        "id": 10,
        "name": "j\u0119zyki"
      },
      {
        "id": 8,
        "name": "orientalia"
      }
    ],
    "id": 1,
    "isbn": "6155849576385",
    "labels": null,
    "labels_details": [],
    "language_id": "pl_",
    "language_name": "polski",
    "note": null,
    "original_title": null,
    "pages": 298,
    "publishers": "inne tryby",
    "publishers_details": [
      {
        "description": null,
        "id": 5,
        "name": "inne tryby",
        "note": null,
        "webpage": null
      }
    ],
    "release_date": 2022,
    "series_id": 1,
    "series_name": "paczki",
    "size": null,
    "title": "Mocz powodowa\u0107 orze\u0142 ni\u017c",
    "translator": null
  },
  {
    "authors": "Kornelia Migo\u0144",
    "authors_details": [
      {
        "birth_date": null,
        "death_date": null,
        "description": null,
        "id": 6,
        "name": "Kornelia Migo\u0144",
        "nationality_id": "pl_",
        "note": null
      }
    ],
    "description": null,
    "first_polish_release_date": 1987,
    "format": "unknown",
    "genres": "j\u0119zyki, komiks, proza",
    "genres_details": [
      {
        "id": 10,
        "name": "j\u0119zyki"
      },
      {
        "id": 4,
        "name": "komiks"
      },
      {
        "id": 2,
        "name": "proza"
      }
    ],
    "id": 8,
    "isbn": "4971463793014",
    "labels": null,
    "labels_details": [],
    "language_id": "pl_",
    "language_name": "polski",
    "note": null,
    "original_title": null,
    "pages": 315,
    "publishers": "monologi",
    "publishers_details": [
      {
        "description": null,
        "id": 2,
        "name": "monologi",
        "note": null,
        "webpage": null
      }
    ],
    "release_date": 1987,
    "series_id": 1,
    "series_name": "paczki",
    "size": null,
    "title": "Ni\u017c \u017ce\u0144ski",
    "translator": null
  },
  {
    "authors": "Adrianna Skoneczna, Kazimierz Wojs\u0142aw",
    "authors_details": [
      {
        "birth_date": null,
        "death_date": null,
        "description": null,
        "id": 12,
        "name": "Adrianna Skoneczna",
        "nationality_id": "pl_",
        "note": null
      },
      {
        "birth_date": null,
        "death_date": null,
        "description": null,
        "id": 7,
        "name": "Kazimierz Wojs\u0142aw",
        "nationality_id": "pl_",
        "note": null
      }
    ],
    "description": null,
    "first_polish_release_date": 2010,
    "format": "unknown",
    "genres": "humanistyka, nauka, poradnik",
    "genres_details": [
      {
        "id": 12,
        "name": "humanistyka"
      },
      {
        "id": 9,
        "name": "nauka"
      },
      {
        "id": 1,
        "name": "poradnik"
      }
    ],
    "id": 13,
    "isbn": "8051448433020",
    "labels": null,
    "labels_details": [],
    "language_id": "pl_",
    "language_name": "polski",
    "note": null,
    "original_title": null,
    "pages": 314,
    "publishers": "diatryby",
    "publishers_details": [
      {
        "description": null,
        "id": 4,
        "name": "diatryby",
        "note": null,
        "webpage": null
      }
    ],
    "release_date": 2010,
    "series_id": 1,
    "series_name": "paczki",
    "size": null,
    "title": "Robak wczoraj",
    "translator": null
  },
  {
    "authors": "Ewelina Ma\u0142ys, Marysia \u015arodka, Nicole Szpila",
    "authors_details": [
      {
        "birth_date": null,
        "death_date": null,
        "description": null,
        "id": 11,
        "name": "Ewelina Ma\u0142ys",
        "nationality_id": "pl_",
        "note": null
      },
      {
        "birth_date": null,
        "death_date": null,
        "description": null,
        "id": 14,
        "name": "Marysia \u015arodka",
        "nationality_id": "pl_",
        "note": null
      },
      {
        "birth_date": null,
        "death_date": null,
        "description": null,
        "id": 5,
        "name": "Nicole Szpila",
        "nationality_id": "pl_",
        "note": null
      }
    ],
    "description": "Fuego y pasi\u00f3n bajo la luna...\n\nNoc\u0105 rytm salsy miesza si\u0119 z szeptem palm, a gor\u0105ce powietrze dr\u017cy od d\u017awi\u0119k\u00f3w gitary. Cia\u0142a p\u0142on\u0105 w ta\u0144cu, jak p\u0142omienie na piasku. \u00a1Vamos! \u017bycie to fiesta \u2013 niech trwa do \u015bwitu!",
    "first_polish_release_date": 1994,
    "format": "paperback",
    "genres": "proza, wykwity",
    "genres_details": [
      {
        "id": 2,
        "name": "proza"
      },
      {
        "id": 14,
        "name": "wykwity"
      }
    ],
    "id": 40,
    "isbn": "1234567890123",
    "labels": null,
    "labels_details": [],
    "language_id": "en_",
    "language_name": "angielski",
    "note": "hasta la vista",
    "original_title": "qqryq qq",
    "pages": 234,
    "publishers": "inne tryby, pomponiki",
    "publishers_details": [
      {
        "description": null,
        "id": 5,
        "name": "inne tryby",
        "note": null,
        "webpage": null
      },
      {
        "description": null,
        "id": 8,
        "name": "pomponiki",
        "note": null,
        "webpage": null
      }
    ],
    "release_date": 2001,
    "series_id": 1,
    "series_name": "paczki",
    "size": null,
    "title": "plotki, p\u0142otki",
    "translator": "bia\u0142y kot"
  },
  {
    "authors": "Pawe\u0142 Pompa",
    "authors_details": [
      {
        "birth_date": null,
        "death_date": null,
        "description": null,
        "id": 2,
        "name": "Pawe\u0142 Pompa",
        "nationality_id": "pl_",
        "note": null
      }
    ],
    "description": "",
    "first_polish_release_date": null,
    "format": "unknown",
    "genres": null,
    "genres_details": [],
    "id": 22,
    "isbn": null,
    "labels": null,
    "labels_details": [],
    "language_id": "pl_",
    "language_name": "polski",
    "note": "",
    "original_title": null,
    "pages": null,
    "publishers": null,
    "publishers_details": [],
    "release_date": null,
    "series_id": null,
    "series_name": null,
    "size": null,
    "title": "ksi\u0105\u017cka 2",
    "translator": null
  }
]
</script>