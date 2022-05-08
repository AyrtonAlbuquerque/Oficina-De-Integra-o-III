<template>
  <v-container>
    <v-form ref="form" @submit.prevent="onSubmit">
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
                v-model="form.fields.username"
                :rules="form.rules.username"
                @focus="fieldFocus"
              />
            </v-col>
          </v-row>
        </v-col>

        <v-col cols="12">
          <v-row justify="center">
            <v-col cols="8">
              <v-text-field
                type="password"
                placeholder="Password"
                v-model="form.fields.password"
                @focus="fieldFocus"
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
                type="submit"
              >
                <v-icon>mdi-login</v-icon>
                Sign in
              </v-btn>
            </v-col>
          </v-row>
        </v-col>


        <v-col cols="12" v-if="showPassAlert">
          <v-row justify="center">
            <v-col cols="8">
              <v-alert type="error" dense>
                Invalid Username or Password
              </v-alert>
            </v-col>
          </v-row>
        </v-col>


        <v-col cols="12">
          <v-row justify="center">
            <v-col cols="8">
              <router-link to="/signup">Register account</router-link>
            </v-col>
          </v-row>
        </v-col>

      </v-row>
    </v-form>
  </v-container>
</template>

<script>
import { required } from 'vuelidate/lib/validators';
import axios from '../plugins/axios';

export default {
  name: 'SigninView',
  data: () => ({
    form: {
      fields: {
        username: '',
        password: '',
      },
      rules: {
        username: [v => required(v) || 'Required field'],
        password: [v => required(v) || 'Required field'],
      }
    },
    showPassAlert: false,
  }),
  methods: {
    fieldFocus() {
      this.showPassAlert = false;
    },
    async onSubmit() {
      const isValid = this.$refs.form.validate();
      if (!isValid) return;

      try {
        const res = await axios.post('/user/signin', this.form.fields);
        const { token } = res.data;
        this.$cookies.set('authentication-token', token);
        this.$router.push({ name: 'Wallet' });
      } catch (err) {
        if (
          err.response
          && err.response.status === 401
          && err.response.data.message === 'WrongPass') {
          this.showPassAlert = true;
        }
      }
    },
  }
};
</script>
