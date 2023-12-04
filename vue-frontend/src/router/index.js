import { createRouter, createWebHistory } from 'vue-router'
import CustomView from '../views/CustomView.vue'
import NotFound from '../views/NotFound.vue'
import DashBoardView from '../views/DashBoardView.vue'
import AddPlayerView from '../views/AddPlayerView.vue'
import ModifyPlayerView from '../views/ModifyPlayerView.vue'
import Vuex from 'vuex'


const store = new Vuex.Store({
  state: {
    username: '',
    accessToken: '',
    refreshToken: '',
    isuserLoggedIn: false,
    logged_at: '',
    route: '',
    expired: false,
  },
  mutations: {
      login(state, api_datas) {
        state.isuserLoggedIn = true;
        state.username = api_datas.data.data.username;
        state.accessToken = api_datas.data.data.tokens['access'];
        state.refreshToken = api_datas.data.data.tokens['refresh'];
        state.route = `/${state.username}/dashboard/`;
        state.logged_at = new Date().getTime();
        state.expired = false;
      },
      setRoute(state, route) {
        state.route = route
      },
      setExpiration(state) {
        state.expired = true;
      },
      logout(state) {
        state.isuserLoggedIn = false;
        state.username = '';
        state.accessToken = '';
        state.refreshToken = '';
        state.logged_at = '';
        state.expired = false;
        state.route = '/';
      },
      retrieve(state, value) {
        state.isuserLoggedIn = value.isuserLoggedIn;
        state.username = value.username;
        state.accessToken = value.accessToken;
        state.refreshToken = value.refreshToken;
        state.route = value.route;
        state.logged_at = value.logged_at;
        state.expired = value.expired;
      }
  },
  getters: {
    state: state => {
      return state
    }
  }
})


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: CustomView,
      meta: {
        needsAuth: false
      }
    },
    {
      path: '/:username/dashboard',
      name: "Dashboard",
      component: DashBoardView,
      meta: {
          needsAuth: true
      }
    },
    {
      path: '/:username/dashboard/add',
      name: "Add Player",
      component: AddPlayerView,
      meta: {
          needsAuth: true
      }
    },
    {
      path: '/:username/dashboard/view/:id/:name/:team/:position/:number',
      name: "Update Player",
      component: ModifyPlayerView,
      meta: {
          needsAuth: true
      }
    },
    {
      path:'/:pathmatch(.*)*',
      name: "NotFound",
      component: NotFound,
      meta: {
          needsAuth: false
      }
    }
    /*{
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }*/
  ]
})

router.beforeEach((to, from, next) => {
  if (to.meta.needsAuth) {
      if (store.state.isuserLoggedIn) {
          next()
      } else {
          next("/login")
      }
  } else {
      next();
  }
})

export { router, store }
