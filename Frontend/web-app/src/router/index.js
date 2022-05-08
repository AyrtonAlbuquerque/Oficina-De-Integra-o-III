import Vue from 'vue';
import VueRouter from 'vue-router';
import jwtDecode from 'jwt-decode';
import axios from '../plugins/axios';
import alert from '../plugins/alert';

Vue.use(VueRouter);

const signedMenu = [{
  viewName: 'Wallet',
  route: { name: 'Wallet' },
}, {
  viewName: 'Statistics',
  route: { name: 'Statistics' }
}];

const routes = [
  {
    path: '/',
    name: 'Wallet',
    meta: {
      authRequired: true,
      menu: signedMenu,
    },
    component: () => import('../views/WalletView.vue'),
  },
  {
    path: '/statistics',
    name: 'Statistics',
    meta: {
      authRequired: true,
      menu: signedMenu,
    },
    component: () => import('../views/StatisticsView.vue'),
  },
  {
    path: '/signin',
    name: 'SignIn',
    component: () => import('../views/SigninView.vue'),
  },
  {
    path: '/signup',
    name: 'SignUp',
    meta: {
      backButtonRoute: { name: 'SignIn' },
    },
    component: () => import('../views/SignupView.vue'),
  },
];

const router = new VueRouter({
  mode: 'history',
  routes,
});

router.beforeEach(async (to, from, next) => {
  await checkRedeemCode(to);
  if (to.meta.authRequired) {
    const decoded = getTokenDecoded();
    if (decoded) next();
    else next({ name: 'SignIn' })
  } else {
    next()
  }
});

async function checkRedeemCode(route) {
  const redeemCode = Vue.$cookies.get('redeem-code');
  const classificationLabel = Vue.$cookies.get('classification-label');
  if (redeemCode && route.meta && route.meta.authRequired) {
    const creditsRedeemed = await redeemCredits(redeemCode, classificationLabel);
    Vue.$cookies.remove('redeem-code');
    Vue.$cookies.remove('classification-label');
    if (creditsRedeemed) alert.showAlert('Credits redeemed');
  }
  const { r: routeRedeemCode, l: routeLabel } = route.query;

  if (routeRedeemCode && route.meta && route.meta.authRequired) {
    const creditsRedeemed = await redeemCredits(routeRedeemCode, routeLabel);
    if (creditsRedeemed) alert.showAlert('Credits redeemed');
    router.replace({ query: {} })
  } else if (routeRedeemCode && route.meta && !route.meta.authRequired) {
    Vue.$cookies.set('redeem-code', routeRedeemCode);
    Vue.$cookies.set('classification-label', routeLabel);
    router.replace({ ...route, query: {} })
  }
}

async function redeemCredits(redeemCode, label) {
  try {
    await axios.post('/transactions/give_credits', {
      redeem_code: redeemCode,
      label: label,
    });
    return true;
  } catch (err) {
    return false
  }
}

function getTokenDecoded() {
  const authToken = Vue.$cookies.get('authentication-token');
  if (!authToken) return null;
  try {
    const decoded = jwtDecode(authToken);
    return decoded;
  } catch (err) {
    return null;
  }
}

export default router;
