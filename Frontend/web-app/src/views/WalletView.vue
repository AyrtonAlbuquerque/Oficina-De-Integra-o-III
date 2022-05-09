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
            $ {{ creditsAmount }}
          </h1>
          <div class></div>
        </v-row>
      </v-col>

      <v-col cols="12" class="mt-5">
        <v-row justify="center">
          <v-col cols="8">
            <send-credits @resetUser="resetUser" />
          </v-col>
        </v-row>
      </v-col>

    </v-row>
  </v-container>
</template>

<script>
import axios from '../plugins/axios';

export default {
  name: 'WalletView',
  components: {
    SendCredits: () => import('../components/SendCredits.vue')
  },
  data: () => ({
    valid: true,
    creditsAmount: 0,
  }),
  async mounted() {
    await this.requestUserBalance();
  },
  methods: {
    async resetUser() {
      await this.requestUserBalance();
    },
    async requestUserBalance() {
      const res = await axios.get('/user/');
      const user = res.data;
      this.creditsAmount = user.balance.toFixed(2);
    }
  }
};
</script>
