<template>
  <div class="bad">
    <div class="err">
      <span v-if="expired" class="n-green">23 hours has passed your session expired login again </span>
      <router-link :to="{ name: 'Home' }">
        <h1 id="err">404 Not Found</h1>
      </router-link>
    </div>
  </div>
</template>

<script>

import axios from 'axios'
import { LOGOUT_URL, TwentyThreeHoursAgo } from '../globals'

export default {

  name: 'App',
  mounted() {
    document.body.classList.add('perform')
	  let cache = localStorage.getItem('cache');
		if (cache !==  null) {
		  cache = JSON.parse(cache);
			var connected_at = cache.logged_at;
			this.$store.commit("retrieve", cache)
			if (TwentyThreeHoursAgo(connected_at)) {
			  this.expired = true;
			  setTimeout(() => this.Logout(), 800);
			} else {
				this.$router.push({ path: cache.route })
			}
		}
	},
  data() {
		return {
			danger: false,
			success: false,
			expired: false,
			msg: "",
		}
	},
  methods: {
    async Logout() {
		  const state = this.getCache;
		  alert(state.refreshToken)
		  const post_data = {
				"refresh": state.refreshToken
			}
			let response = ''
			try {
				response = await axios.post(LOGOUT_URL, post_data)
			} catch (error) {
				let api_error_message = ""
				if (!error.response) {
					this.api_error_message = "Network Error | Api Down!"
				} else {
					for (var err in error.response.data.errors) {
						api_error_message += error.response.data.errors[err]
						api_error_message += " |  Please retry!"
					}
				}
				this.danger = true;
				this.success = false;
				this.msg = api_error_message;
				setTimeout(() => {
          this.danger = false;
				  this.success = false;
				  this.msg = '';
				}, 3500);
			}
			if (response.status === 204) {
        this.danger = false
				this.success = true
				this.msg = 'Logged Out...';
				this.$store.commit('logout');
				localStorage.removeItem('cache');
				setTimeout(() => this.$router.push({ path: '/' }), 800);
			}
		}
  },
  computed: {
	  getCache() {
	    return this.$store.getters.state;
	  }
	}
}

</script>

<style>

.perform{
	background-color: #c9d6ff;
	background: linear-gradient(to right, #e2e2e2, #c9d6ff);
	display: flex;
	align-items: center;
	justify-content: center;
	flex-direction: column;
	height: 100vh;
}

.err {
display: grid;
width: 100%;
height: 90%;
align-items: center;
justify-content: center;
color: #512da8  ;
font-size: 20px;
font-weight: bold;
text-decoration: none;
}
</style>