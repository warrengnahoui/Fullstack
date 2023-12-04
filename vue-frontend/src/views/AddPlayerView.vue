<template>
  <div class="container" id="container" ref="container">
    <span v-if="expired" class="n-green">23 hours has passed your session expired login again </span>
    <br><br>
    
    <div class="form-container sign-in">
      <div class="form">
        <h1>Create Player</h1>
        <br>
        <span>Basketball platform</span>
        <input type="text" v-model.trim="name" placeholder="Player Name">
        <input type="text" v-model.trim="team" placeholder="Team Name">
        <input type="text" v-model.trim="position" placeholder="Postion">
        <input type="text" v-model.trim="number" placeholder="Jersey Number">
        <a href="#">Copyright Ned Warren Gnh 2023</a>
        <button @click="AddPlayer">Add Player</button>
        <br>
        <span class="n-red" v-if="danger">{{msg}}</span>
        <span class="n-green" v-if="success">{{msg}}</span>
      </div>
    </div>
    <div class="toggle-container">
      <div class="toggle">
        <div class="toggle-panel toggle-right">
          <h1>Add your Player!</h1>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import useValidate from '@vuelidate/core'
import { required, maxLength, alphaNum, alpha, numeric } from '@vuelidate/validators'
import { LOGOUT_URL, PLAYERS_URL, TwentyThreeHoursAgo } from '../globals'

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
				this.$router.push({ path: `/${cache.username}/dashboard/add/` });
			}
		}
	},
  data() {
		return {
			v$: useValidate(),
			name: '',
			team: '',
			position: '',
			number: 0,
			danger: false,
			success: false,
			expired: false,
			msg: "",
		}
	},
	validations() {
		return {
			name: {
				required,
				maxLength: maxLength(60),
			},
			team: {
				required,
				maxLength: maxLength(60),
			},
			position: {
				required,
				maxLength: maxLength(60),
			},
			number: {
			  required,
			  numeric
      }
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
		},
		async PostPlayer()
		{
		  const state = this.getCache;
		  const post_data = {
		    'name' : this.name,
		    'team' : this.team,
		    'position' : this.position,
		    'number': this.number.toString()
		  }
			let response = '';
			try {
				response = await axios.post(PLAYERS_URL, post_data,  {
					headers: {
						'Authorization': `Bearer ${state.accessToken}`
					}
				});
			} catch (error) {
				let api_error_message = ""
				if (!error.response) {
					api_error_message = "Network Error | Api Down!"
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
			if (response.status === 201) {
        this.danger = false
				this.success = true
				this.msg = 'Data Created successfully...';
				setTimeout(() => {
          this.danger = false;
				  this.success = false;
				  this.msg = '';
				  this.$router.go();
				}, 800);
			}
		},
		AddPlayer()
		{
		  this.v$.$touch()
			let error_message = ""
			if (this.v$.name.$error) {
				error_message += "Invalid name format entered (alphanumeric only, maximun 60)\n"
			}
			if (this.v$.team.$error) {
				error_message += "Invalid team name format entered (alphanumeric only, maximun 60)\n"
			}
			if (this.v$.position.$error) {
				error_message += "Invalid position format entered (alpha only, maximun 60)\n"
			}
			if (this.v$.number.$error) {
				error_message += "Invalid number format entered (numeric only)\n"
			}
			this.v$.$validate()
			if (!this.v$.$error) {
				this.danger = false
				this.success = true
				this.PostPlayer()
			} else {
				this.danger = true;
				this.success = false;
				this.msg = error_message;
				setTimeout(() => {
          this.danger = false;
				  this.success = false;
				  this.msg = ''
				}, 3500);
			}
		}
  },
  computed: {
	  getCache() {
	    return this.$store.getters.state;
	  },
	  postData() {
	    if (this.$route.params.id) {
	      return true;
	    }
	    return false;
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
.container{
    background-color: #fff;
    border-radius: 30px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.35);
    position: relative;
    overflow: hidden;
    width: 768px;
    max-width: 100%;
    min-height: 480px;
}

.container p{
    font-size: 14px;
    line-height: 20px;
    letter-spacing: 0.3px;
    margin: 20px 0;
}

.container span{
    font-size: 12px;
}

.container a{
    color: #333;
    font-size: 13px;
    text-decoration: none;
    margin: 15px 0 10px;
}

.container button{
    background-color: #512da8;
    color: #fff;
    font-size: 12px;
    padding: 10px 45px;
    border: 1px solid transparent;
    border-radius: 8px;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-top: 10px;
    cursor: pointer;
}

.container button.hidden{
    background-color: transparent;
    border-color: #fff;
}

.container .form{
    background-color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    padding: 0 40px;
    height: 100%;
}

.container input{
    background-color: #eee;
    border: none;
    margin: 8px 0;
    padding: 10px 15px;
    font-size: 13px;
    border-radius: 8px;
    width: 100%;
    outline: none;
}

.form-container{
    position: absolute;
    top: 0;
    height: 100%;
    transition: all 0.6s ease-in-out;
}

.sign-in{
    left: 0;
    width: 50%;
    z-index: 2;
}

.container.active .sign-in{
    transform: translateX(100%);
}

.sign-up{
    left: 0;
    width: 50%;
    opacity: 0;
    z-index: 1;
}

.container.active .sign-up{
    transform: translateX(100%);
    opacity: 1;
    z-index: 5;
    animation: move 0.6s;
}

@keyframes move{
    0%, 49.99%{
        opacity: 0;
        z-index: 1;
    }
    50%, 100%{
        opacity: 1;
        z-index: 5;
    }
}

.toggle-container{
    position: absolute;
    top: 0;
    left: 50%;
    width: 50%;
    height: 100%;
    overflow: hidden;
    transition: all 0.6s ease-in-out;
    border-radius: 150px 0 0 100px;
    z-index: 1000;
}

.container.active .toggle-container{
    transform: translateX(-100%);
    border-radius: 0 150px 100px 0;
}

.toggle{
    background-color: #512da8;
    height: 100%;
    background: linear-gradient(to right, #5c6bc0, #512da8);
    color: #fff;
    position: relative;
    left: -100%;
    height: 100%;
    width: 200%;
    transform: translateX(0);
    transition: all 0.6s ease-in-out;
}

.container.active .toggle{
    transform: translateX(50%);
}

.toggle-panel{
    position: absolute;
    width: 50%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    padding: 0 30px;
    text-align: center;
    top: 0;
    transform: translateX(0);
    transition: all 0.6s ease-in-out;
}

.toggle-left{
    transform: translateX(-200%);
}

.container.active .toggle-left{
    transform: translateX(0);
}

.toggle-right{
    right: 0;
    transform: translateX(0);
}

.container.active .toggle-right{
    transform: translateX(200%);
}
.n-red{
  color: red !important;
}
.n-green{
  color: teal !important;
}

</style>