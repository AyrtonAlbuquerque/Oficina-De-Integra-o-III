import Vue from 'vue';
import VueRouter from 'vue-router';
import jwtDecode from 'jwt-decode';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Wallet',
    meta: {
      authRequired: true,
    },
    component: () => import('../views/WalletView.vue'),
  },
  {
    path: '/signin',
    name: 'Sign in',
    component: () => import('../views/SigninView.vue'),
  },
  {
    path: '/signup',
    name: 'Sign up',
    meta: {
      backButtonRoute: { name: 'Sign in' },
    },
    component: () => import('../views/SignupView.vue'),
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

// router.beforeEach((to, from) => {
//   console.log('to', to, 'from', from);

//   if (to.meta.authRequired) {
//     const authToken = Vue.$cookies.get('authToken');
//     if (!authToken) return { name: 'Sign in' };
//     try {
//       jwtDecode(authToken);
//     } catch (err) {
//       return { name: 'Sign in' };
//     }
//   }
//   return true;
// });

export default router;
