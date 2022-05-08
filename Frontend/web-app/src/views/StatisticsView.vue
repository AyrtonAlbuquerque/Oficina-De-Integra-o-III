<template>
  <v-container>
    <v-row class="text-center">
      <v-col class="mt-5">
        <h2 class="mt-5 mb-2">
          Statistics
        </h2>
      </v-col>

      <v-col cols="12" class="mb-5">
        <v-row justify="center">
            <strong>Metals:</strong> {{ statistics['METALS'] }}
        </v-row>
        <v-row justify="center">
            <strong>Plastics:</strong> {{ statistics['PLASTICS'] }}
        </v-row>
        <v-row justify="center">
            <strong>Paper:</strong> {{ statistics['PAPER'] }}
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from '../plugins/axios';

const CLASS_DEFINITIONS = {
  METALS: [0, 3],
  PLASTICS: [2, 4],
  PAPER: [5, 6],
};

export default {
  name: 'StatisticsView',
  data: () => ({
    statistics: [],
  }),
  async mounted() {
    await this.requestStatistics();
  },
  methods: {
    async requestStatistics() {
      const res = await axios.get('/classifications/statistics');
      const { statistics } = res.data;
      this.statistics = this.parseStatistics(statistics);
    },
    parseStatistics(statistics) {
      const amountFromEach = {
        METALS: 0,
        PLASTICS: 0,
        PAPER: 0,
      };
      statistics.forEach((statistic) => {
        const [label, quantity] = statistic;
        Object.keys(CLASS_DEFINITIONS).forEach((type) => {
          if (CLASS_DEFINITIONS[type].includes(label)) {
            amountFromEach[type] += quantity;
          }
        })
      });
      return amountFromEach;
    }
  }
};
</script>
