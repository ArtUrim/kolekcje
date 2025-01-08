<template>
  <v-container>
    <v-card class="pa-4">
      <v-form ref="form" v-model="valid">
        <v-row>
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="firstName"
              label="First Name"
              :rules="nameRules"
              required
            ></v-text-field>
          </v-col>
          
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="lastName"
              label="Last Name"
              :rules="nameRules"
              required
            ></v-text-field>
          </v-col>

          <v-col cols="12" sm="6">
            <v-text-field
              v-model="age"
              label="Age"
              type="number"
              :rules="ageRules"
              required
            ></v-text-field>
          </v-col>

          <v-col cols="12" sm="6">
            <v-text-field
              v-model="email"
              label="Email"
              :rules="emailRules"
              required
            ></v-text-field>
          </v-col>

          <v-col cols="12">
            <v-textarea
              v-model="interests"
              label="Interests"
              rows="3"
              placeholder="Tell us about your interests..."
            ></v-textarea>
          </v-col>
        </v-row>

        <v-card-actions class="pt-4">
          <v-spacer></v-spacer>
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
    firstName: '',
    lastName: '',
    age: '',
    email: '',
    interests: '',
    nameRules: [
      v => !!v || 'Name is required',
      v => v.length <= 50 || 'Name must be less than 50 characters'
    ],
    ageRules: [
      v => !!v || 'Age is required',
      v => v >= 13 && v <= 19 || 'Age must be between 13 and 19'
    ],
    emailRules: [
      v => !!v || 'Email is required',
      v => /.+@.+\..+/.test(v) || 'Email must be valid'
    ]
  }),
  methods: {
    submitForm() {
      if (this.$refs.form.validate()) {
        // Handle form submission
        console.log('Form submitted:', {
          firstName: this.firstName,
          lastName: this.lastName,
          age: this.age,
          email: this.email,
          interests: this.interests
        })
      }
    },
    resetForm() {
      this.$refs.form.reset()
    }
  }
}
</script>
