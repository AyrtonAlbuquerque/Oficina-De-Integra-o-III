<template>
  <v-container>
    <v-row class="text-center">
      <v-col class="mt-5">
        <h3 class="mt-5 mb-2">
          Credits
        </h3>
      </v-col>

      <v-col cols="12" class="mb-5">
        <v-row justify="center">
          <h1 class="primary--text display-2 font-weight-bold mb-5">
            $ 10,00
          </h1>
          <div class></div>
        </v-row>
      </v-col>

      <v-col cols="12" class="mt-5">
        <v-row justify="center">
          <v-col cols="8">
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
                          v-model="username"
                          label="Username"
                          required
                        ></v-text-field>
                      </v-col>
                      <v-col
                        cols="12"
                        sm="6"
                        md="4"
                      >
                        <v-text-field
                          v-model="amount"
                          label="Amount to send"
                          hide-details
                          single-line
                          type="number"
                        />
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
                    @click="dialog = false"
                  >
                    Send
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-col>
        </v-row>
      </v-col>

    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'WalletView',
  data: () => ({
    valid: true,
    dialog: false,
  }),
};
</script>
