<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="text-center pa-5">
          <v-card-title class="text-h4 font-weight-bold mb-3">
            404 - Page Not Found
          </v-card-title>
          <v-card-text>
            <p>The page you are looking for does not exist.</p>
            <p class="text-caption mt-2">
              (This includes browser-specific requests like <code>/.well-known/...</code> which can be safely ignored.)
            </p>
          </v-card-text>
          <v-card-actions class="justify-center">
            <v-btn color="primary" to="/">
              Go Back Home
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { setResponseStatus } from '#app';
setResponseStatus(404);
</script>