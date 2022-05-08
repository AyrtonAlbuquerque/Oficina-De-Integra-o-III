<template>
  <v-container>
    <v-form
      ref="form"
      @submit.prevent="signup"
    >
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
            Sign up
          </h2>
        </v-col>

        <v-col cols="12">
          <v-row justify="center">
            <v-col cols="8">
              <v-text-field
                placeholder="Username"
                v-model="form.fields.username"
                :rules="form.rules.username"
              />
            </v-col>
          </v-row>
        </v-col>

        <v-col cols="12">
          <v-row justify="center">
            <v-col cols="8">
              <v-text-field
                placeholder="Password"
                v-model="form.fields.password"
                :rules="form.rules.password"
                type="password"
              />
            </v-col>
          </v-row>
        </v-col>

        <v-col cols="12">
          <v-row justify="center">
            <v-col cols="8">
              <v-text-field
                placeholder="Confirm password"
                v-model="form.fields.confirmPassword"
                :rules="form.rules.confirmPassword"
                type="password"
              />
            </v-col>
          </v-row>
        </v-col>

        <v-col cols="12" v-if="showExistsAlert">
          <v-row justify="center">
            <v-col cols="8">
              <v-alert type="error" dense>
                User with this username already exists
              </v-alert>
            </v-col>
          </v-row>
        </v-col>

        <v-col cols="12" class="mb-3">
          <v-row justify="center">
            <v-col cols="8">
              <v-btn
                block
                outlined
                type="submit"
              >
                <v-icon>mdi-account-plus</v-icon>
                Sign up
              </v-btn>
            </v-col>
          </v-row>
        </v-col>

      </v-row>
    </v-form>
  </v-container>
</template>

<script>
import { required, minLength, sameAs } from 'vuelidate/lib/validators';
import axios from '../plugins/axios';

export default {
  name: 'SignupView',
  data: () => ({
    showExistsAlert: false,
    form: {
      fields: {
        username: '',
        password: '',
        confirmPassword: '',
      },
      rules: {
        username: [
          v => required(v) || 'Required field',
          (v) => minLength(3)(v) || 'Username must be at least 3 characters long',
        ],
        password: [
          v => required(v) || 'Required field',
          (v) => minLength(8)(v) || 'Password must be at least 8 characters long',
        ],
        confirmPassword: [
          v => required(v) || 'Required field',
        ],
      }
    },
  }),
  created() {
    this.form.rules.confirmPassword.push(this.passwordSameAsConfirm);
  },
  methods: {
    fieldFocus() {
      this.showExistsAlert = false;
    },
    passwordSameAsConfirm(confirmPassword) {
      return this.form.fields.password === confirmPassword || 'Password mismatch';
    },
    async signup() {
      const isValid = this.$refs.form.validate();
      if (!isValid) return;

      try {
        await axios.post('/user/signup', {
          username: this.form.fields.username,
          password: this.form.fields.password,
        });
        this.$alert.showAlert('User Created');
        this.$router.push({ name: 'SignIn' });
      } catch (err) {
        if (
          err.response
          && err.response.status === 400
          && err.response.data.message === 'UserWithSameName') {
          this.showExistsAlert = true;
        }
      }

    }
  }
};
</script>
