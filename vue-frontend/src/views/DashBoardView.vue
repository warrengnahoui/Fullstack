<template>
	<div class="content">
      <h1 class="heading">Welcome To Dashboard</h1>
      <button class="logoutbtn" @click="Logout">Logout</button>
      <button class="addbtn" @click="Route">Add Player</button>
      <br><br>
      <span class="n-red" v-if="danger">{{msg}}</span>
      <span class="n-green" v-if="success">{{msg}}</span>
      <br><br>
    
    <div class="box-container" v-if="haveData">
      <div class="box"  v-for="player in players" :key="player">
        <img :src="Imager(player.id)"/>
        <h3>{{ player.name }}</h3>
        <p>Team: {{ player.team }} Basketball Club.</p>
				<p>Position: {{ player.position}}.</p>
				<p>Jersey Number: {{ player.number}}.</p>
				<p>Average Performances: {{ stats[player.id]['points'] }} pts  {{ stats[player.id]['assists'] }} assists {{ stats[player.id]['rebounds'] }} rebounds</p>
        <a @click="Update(player.id, player.name, player.team, player.position, player.number)" class="btn">Modify</a>
        <a @click="DelPlayer(player.id)" class="del">Delete</a>
      </div>
    </div>
    <div v-else>
			Please a Player to the Database
		</div>
  </div>
</template>

<script>
import axios from 'axios'
import { LOGOUT_URL, PLAYERS_URL, PERFORMANCES_URL, TwentyThreeHoursAgo } from '../globals'

export default {
	name: 'App',
	mounted() {
		document.body.classList.remove('perform')
	  let cache = localStorage.getItem('cache');
		if (cache !==  null) {
		  cache = JSON.parse(cache);
			var connected_at = cache.logged_at;
			this.$store.commit("retrieve", cache)
			if (TwentyThreeHoursAgo(connected_at)) {
			  this.expired = true;
			  setTimeout(() => this.Logout(), 800);
			} else {
				this.$router.push({ path: cache.route });
				this.FetchPlayers();
				this.FetchPerformances();
			}
		}
	},
	data() {
		return {
			danger: false,
			success: false,
			expired: false,
			players: [],
			stats: {},
			msg: "",
		}
	},
	methods: {
		async Logout() {
		  const state = this.getCache;
		  const post_data = {
				"refresh": state.refreshToken
			}
			let response = ''
			try {
				response = await axios.post(LOGOUT_URL, post_data)
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
			if (response.status === 204) {
        this.danger = false
				this.success = true
				this.msg = 'Logged Out...';
				this.$store.commit('logout');
				localStorage.removeItem('cache');
				setTimeout(() => this.$router.push({ path: '/' }), 800);
			}
		},
		async FetchPlayers() {
			const state = this.getCache;
			let response = '';
			try {
				response = await axios.get(PLAYERS_URL, {
					headers: {
						'Authorization': `Bearer ${state.accessToken}`
					}
				})
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
			if (response.status === 200) {
        this.danger = false
				this.success = true
				this.msg = 'Data Fetched successfully...';
				this.players = response.data.data;
				setTimeout(() => {
          this.danger = false;
				  this.success = false;
				  this.msg = '';
				}, 800);
			}
			console.log(response, this.players)
		},
		async FetchPerformances() {
			let response = '';
			try {
				response = await axios.get(PERFORMANCES_URL)
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
			if (response.status === 200) {
        this.danger = false
				this.success = true
				this.msg = 'Data Fetched successfully...';
				this.stats = response.data.data;
				setTimeout(() => {
          this.danger = false;
				  this.success = false;
				  this.msg = '';
				}, 800);
			}
			console.log(response, this.stats)
		},
		async DelPlayer(id) {
			const state = this.getCache;
			let response = '';
			let post = id.toString();
			try {
				response = await axios.delete(PLAYERS_URL + post ,  {
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
			if (response.status === 204) {
        this.danger = false
				this.success = true
				this.msg = 'Data Deleted successfully...';
				setTimeout(() => {
          this.danger = false;
				  this.success = false;
				  this.msg = '';
				  this.$router.go();
				}, 800);
			}
			console.log(response, this.players)
		},
		Update(id, name, team, position, number){
			const cache = this.$store.getters.state
			setTimeout(() => {
        this.$router.push(`/${cache.username}/dashboard/view/${id}/${name}/${team}/${position}/${number}`);
			}, 100);
		},
		Route()
		{
			const cache = this.$store.getters.state
			setTimeout(() => {
        this.$router.push(`/${cache.username}/dashboard/add/`);
			}, 300);
		},
		Imager(id){
			let res = id % 3;
			let photo = '../assets/img/' + res.toString() + '.jpg';
			console.log(photo);
			return new URL(photo, import.meta.url);
		},
		haveData() {
	    return this.players.length !== 0;
	  }
	},
	computed: {
	  getCache() {
	    return this.$store.getters.state;
	  },
	}
}
</script>

<style scoped>

*{
  font-family: 'Montserrat', sans-serif;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  outline: none;
  text-decoration: none;
  text-transform: capitalize;
  transition: .2s linear;
}

.n-red{
  color: red !important;
}
.n-green{
  color: teal !important;
}

.logoutbtn{
	text-align: center;
  padding-bottom: 15px;
  color: #fff;
  background-color: #444;
	color: #fff;
	font-size: 12px;
	padding: 10px 45px;
	border: 1px solid transparent;
	border-radius: 8px;
	font-weight: 600;
	letter-spacing: 0.5px;
	text-transform: uppercase;
	align-content: center;
	justify-content: center;
}

.addbtn{
	text-align: center;
  padding-bottom: 15px;
  color: #fff;
  background-color: #8D83C1;
	color: #fff;
	font-size: 12px;
	padding: 10px 45px;
	border: 1px solid transparent;
	border-radius: 8px;
	font-weight: 600;
	letter-spacing: 0.5px;
	text-transform: uppercase;
	align-content: center;
	justify-content: center;
	margin-left: 10px;
}

.content .logoutbtn:hover{
  box-shadow: 0 10px 15px rgba(0, 0, 0, .2);
  transform: scale(1.03);
}

.content .addbtn:hover{
  box-shadow: 0 10px 15px rgba(0, 0, 0, .2);
  transform: scale(1.03);
}
.content{
  background: linear-gradient(to right, #e2e2e2, #c9d6ff);
  padding: 15px 9%;
  padding-bottom: 100px;
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 2000px; 
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 2;
  cursor: pointer;
}

.content .heading{
  text-align: center;
  padding-bottom: 15px;
  color: #fff;
  text-shadow: 0 5px 10px rgba(0, 0, 0, .2);
  font-size: 40px;
}

.content .box-container{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(270px, 1fr));
  gap: 15px;
}

.content .box-container .box{
  box-shadow: 0 5px, 10px, rgba(0, 0, 0, .2);
  border-radius: 15px;
  background: linear-gradient(45deg, #c9d6ff, #633ebb);;
  text-align: center;
  padding: 30px 20px;
}

.content .box-container .box img{
  height: 180px;
  width: 180px;
  border-radius: 100px;
}

.content .box-container .box h3{
  color: #333;
  font-size: 22px;
  padding: 10px 0;
}

.content .box-container .box p{
	text-align: center;
	justify-content: center;
  color: #ffffffcd;
  font-size: 15px;
  line-height: 1.8;
}

.content .box-container .box .btn{
  margin-top: 10px;
  display: block;
  background: #8D83C1;
  color: #fff;
  font-size: 17px;
  border-radius: 5px;
  padding: 8px 25px;
}

.content .box-container .box .del{
  margin-top: 10px;
  display: block;
  background: #444;
  color: #fff;
  font-size: 17px;
  border-radius: 5px;
  padding: 8px 25px;
}

.content .box-container .box .btn:hover{
  letter-spacing: 1px;
}

.content .box-container .btn:hover{
  box-shadow: 0 10px 15px rgba(0, 0, 0, .2);
  transform: scale(1.03);
}

.content .box-container .box .del:hover{
  letter-spacing: 1px;
}

.content .box-container .del:hover{
  box-shadow: 0 10px 15px rgba(0, 0, 0, .2);
  transform: scale(1.03);
}

.content .box-container .box:hover{
  box-shadow: 0 10px 15px rgba(0, 0, 0, .2);
  transform: scale(1.03);
}

@media (max-width:768px){
  .content{
    padding: 20px;
  }
}

</style>