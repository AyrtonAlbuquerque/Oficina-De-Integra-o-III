import Vue from 'vue';
import * as Axios from 'axios';
import router from '../router';

const { default: axios } = Axios;

axios.interceptors.request.use(
  async (res) => res,
  async (err) => {
    const status = err.response ? err.response.status : null;
    const url = err.request ? err.request.responseURL : null;

    if (url && (url.endsWith('/auth/token') || url.endsWith('/auth/revoke'))) {
      throw err;
    } else if (status === 401) {
      Vue.$cookies.remove('authenticationToken');
      router.push({ name: 'Sign in' });
    }
  },
);

export default axios;
