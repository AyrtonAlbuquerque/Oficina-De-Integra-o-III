<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <v-app-bar-nav-icon
        v-if="menu.length"
        @click.stop="drawer = !drawer">
      </v-app-bar-nav-icon>

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

      <v-menu offset-y v-if="username">
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
            <v-list-item-title class="subtitle-1">{{ username }}</v-list-item-title>
          </v-list-item>
          <v-divider />
          <v-list-item>
            <v-btn
              block
              raised
              @click="logout"
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
        v-if="menu.length"
        v-model="drawer"
        absolute
        temporary
      >
        <v-list
          nav
          dense
        >
          <v-list-item-group
            active-class="deep-purple--text text--accent-4"
          >
            <v-list-item
              v-for="item of menu"
              :key="item.route.name"
              @click.stop="$router.push(item.route)">
              <v-list-item-title>
                {{ item.viewName }}
              </v-list-item-title>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-navigation-drawer>
      <router-view/>
      <v-snackbar
        v-model="snackbar"
        :timeout="3000"
      >
        {{ snackbarMessage }}
      </v-snackbar>
    </v-main>
  </v-app>
</template>

<script>
import jwtDecode from 'jwt-decode';

export default {
  name: 'App',
  data: () => ({
    drawer: false,
    snackbar: false,
    snackbarMessage: '',
  }),
  computed: {
    backButtonRoute() {
      if (!this.$route.meta) return false;
      if (!this.$route.meta.backButtonRoute) return false;
      return this.$route.meta.backButtonRoute;
    },
    getUsername() {
      if (!this.$route.meta) return false;
      if (this.$route.meta.menu)  return true;
      return false;
    },
    menu() {
      if (!this.$route.meta) return [];
      if (!this.$route.meta.menu) return [];
      return this.$route.meta.menu;
    },
    username() {
      if (!this.getUsername) return '';
      const authToken = this.$cookies.get('authentication-token');
      if (!authToken) return '';

      try {
        const decoded = jwtDecode(authToken);
        let username = decoded.username.split('@');
        if (username.length > 1) username.pop();
        return username.join('');
      } catch (err) {
        return '';
      }
    },
  },
  created() {
    this.$alert.onAlert = (message) => {
      this.snackbar = true;
      this.snackbarMessage = message;
    }
  },
  methods: {
    goBack() {
      this.$router.push(this.backButtonRoute);
    },
    logout() {
      this.$cookies.remove('authentication-token');
      this.$router.push({ name: 'SignIn' });
    }
  }
};
</script>
