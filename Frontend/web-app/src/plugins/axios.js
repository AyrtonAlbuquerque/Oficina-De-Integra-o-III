import Vue from 'vue';
import * as Axios from 'axios';
import router from '../router';

const { default: axios } = Axios;

const backendUrl = 'http://localhost:8081';

axios.defaults.baseURL = backendUrl;

axios.interceptors.request.use(
  async (res) => {
    const authToken = Vue.$cookies.get('authentication-token');
    if (authToken) {
      res.headers['Authorization'] = `Bearer ${authToken}`;
    }
    return res
  },
  async (err) => {
    const status = err.response ? err.response.status : null;
    const url = err.request ? err.request.responseURL : null;

    if (url && (url.endsWith('/user/signin') || url.endsWith('/user/signup'))) {
      throw err;
    } else if (status === 401) {
      Vue.$cookies.remove('authentication-token');
      router.push({ name: 'Sign in' });
    }
  },
);

export default axios;
