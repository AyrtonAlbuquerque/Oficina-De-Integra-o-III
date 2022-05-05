<template>
  <v-container>
    <v-form v-model="valid">
      <v-row class="text-center">
        <v-col cols="12">
          <v-img
            :src="require('../assets/recycling_icon.jpg')"
            class="my-3"
            contain
            height="100"
          />
        </v-col>

        <v-col>
          <h2 class="display-2 font-weight-bold mb-3">
            Sign in
          </h2>
        </v-col>

        <v-col cols="12">
          <v-row justify="center">
            <v-col cols="8">
              <v-text-field
                placeholder="Username"
              />
            </v-col>
          </v-row>
        </v-col>

        <v-col cols="12">
          <v-row justify="center">
            <v-col cols="8">
              <v-text-field
                placeholder="Password"
              />
            </v-col>
          </v-row>
        </v-col>

        <v-col cols="12">
          <v-row justify="center">
            <v-col cols="8">
              <v-btn
                block
                outlined
              >
                <v-icon>mdi-login</v-icon>
                Sign in
              </v-btn>
            </v-col>
          </v-row>
        </v-col>

        <v-col cols="12">
          <v-row justify="center">
            <v-col cols="8">
              <a href="/#signup">Register account</a>
            </v-col>
          </v-row>
        </v-col>

      </v-row>
    </v-form>
  </v-container>
</template>

<script>
export default {
  name: 'SigninView',
  data: () => ({
    valid: true,
  }),
};
</script>
