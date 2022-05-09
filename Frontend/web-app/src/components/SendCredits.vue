<template>
  <v-dialog
    v-model="dialog"
    persistent
    max-width="600px"
  >
    <template v-slot:activator="{ on, attrs }">

      <v-btn
        block
        outlined
        v-bind="attrs"
        v-on="on"
      >
        <v-icon>mdi-cash</v-icon>
        Send credits
      </v-btn>
    </template>
    <v-form ref="form" @submit.prevent="send">
      <v-card>
        <v-card-title>
          <span class="text-h5">Send Credits</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col
                cols="12"
                sm="6"
                md="4"
              >
                <v-text-field
                  v-model="form.fields.toAccount"
                  :rules="form.rules.toAccount"
                  @focus="fieldFocus"
                  label="Receiver"
                ></v-text-field>
              </v-col>
              <v-col
                cols="12"
                sm="6"
                md="4"
              >
                <v-text-field
                  v-model="form.fields.amount"
                  :rules="form.rules.amount"
                  @focus="fieldFocus"
                  label="Amount to send"
                  single-line
                  type="number"
                />
              </v-col>

              <v-col cols="12" v-if="showAlert">
                <v-alert type="error" dense>
                  {{ alertMessage }}
                </v-alert>
              </v-col>
            </v-row>
          </v-container>
          <small>*indicates required field</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue darken-1"
            text
            @click="dialog = false"
          >
            Close
          </v-btn>
          <v-btn
            color="blue darken-1"
            text
            type="submit"
          >
            Send
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-form>
  </v-dialog>
</template>

<script>
import { required } from 'vuelidate/lib/validators';
import axios from '../plugins/axios';

const errorMessages = {
  InsufficientFunds: 'Insufficent funds',
  NotFound: 'Receiver not found',
  InvalidRequest: 'Some error occured. Try again later',
}

export default {
  name: 'SendCredits',
  data: () => ({
    dialog: false,
    showAlert: false,
    alertMessage: '',
    form: {
      fields: {
        toAccount: '',
        amount: '',
      },
      rules: {
        toAccount: [v => required(v) || 'Required field'],
        amount: [
          v => required(v) || 'Required field',
          v => Number(v) > 0 || 'Invalid amount',
        ],
      }
    },
  }),
  methods: {
    fieldFocus() {
      this.showAlert = false;
      this.alertMessage = '';
    },
    async send() {
      const isValid = this.$refs.form.validate();
      if (!isValid) return;

      try {
        const res = await axios.post('/transactions/send', {
          to_account: this.form.fields.toAccount,
          amount: Number(this.form.fields.amount),
        });
        this.$emit('resetUser');
        this.$alert.showAlert('Transaction sent');
        this.dialog = false;
      } catch (err) {
        if (err.response && (
          err.response.status === 400
          || err.response.status === 404)) {
          const { message } = err.response.data;
          this.showAlert = true;
          this.alertMessage = errorMessages[message];
        }
      }
    }
  }
};
</script>
