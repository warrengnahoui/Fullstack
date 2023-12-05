const DEPLOY = true

let BACKEND_URL

if (DEPLOY === false) {
  BACKEND_URL = "http://127.0.0.1:8080/api"
} else {
  BACKEND_URL = "http://0.0.0.0:8080/api"
}

const REGISTER_URL = BACKEND_URL + '/auth/register/'

const LOGIN_URL = BACKEND_URL + '/auth/login/'

const LOGOUT_URL = BACKEND_URL + '/auth/logout/'

const REFRESH_TOKEN_URL = BACKEND_URL + '/auth/token/refresh/'

const PLAYERS_URL = BACKEND_URL + '/players/'

const PERFORMANCES_URL = BACKEND_URL + '/performances/statistics/'


const TwentyThreeHoursAgo = function(connected_at) {
  const current_time = new Date().getTime()
  const twenty_three_hour =  1000 * 60 * 60 * 23;
  //const five_minutes =  1000 * 60 * 2;
  const hourago = current_time - connected_at;
  return hourago >= twenty_three_hour;
}

export { BACKEND_URL, REGISTER_URL, LOGIN_URL, LOGOUT_URL, REFRESH_TOKEN_URL, PLAYERS_URL, PERFORMANCES_URL, TwentyThreeHoursAgo }