<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <v-app-bar-nav-icon v-if="false" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>

      <v-btn
        v-if="backButtonRoute"
        @click="goBack"
        icon
      >
        <v-icon>mdi-arrow-left-bold</v-icon>
      </v-btn>

      <div class="d-flex align-center">
        <v-icon
          large
          color="green darken-2"
        >
          mdi-recycle
        </v-icon>
      </div>

      <v-spacer></v-spacer>

      <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            v-bind="attrs"
            v-on="on"
            icon
          >
            <v-icon>mdi-account</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item>
            <v-list-item-title class="subtitle-1">iandouglas.1996</v-list-item-title>
          </v-list-item>
          <v-divider />
          <v-list-item>
            <v-btn
              block
              raised
            >
              <v-icon>mdi-logout</v-icon>
              Sign out
            </v-btn>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-main>
      <v-navigation-drawer
        v-model="drawer"
        absolute
        temporary
      >
        <v-list
          nav
          dense
        >
          <v-list-item-group
            v-model="group"
            active-class="deep-purple--text text--accent-4"
          >
            <v-list-item>
              <v-list-item-title>Foo</v-list-item-title>
            </v-list-item>

            <v-list-item>
              <v-list-item-title>Bar</v-list-item-title>
            </v-list-item>

            <v-list-item>
              <v-list-item-title>Fizz</v-list-item-title>
            </v-list-item>

            <v-list-item>
              <v-list-item-title>Buzz</v-list-item-title>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-navigation-drawer>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',
  data: () => ({
    drawer: false,
  }),
  computed: {
    backButtonRoute() {
      console.log(this.$route);
      return '';
    },
  },
  methods: {
    goBack() {
      console.log('backButton', this.backButtonRoute);
    }
  }
};
</script>
