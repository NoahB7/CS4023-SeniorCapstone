import * as axios from 'axios';

const api = {
    async makeGetRequest() {
        return await axios({
            method: 'GET',
            url: `${getUrl()}/test`,
            headers: { 'content-type': 'application/json' },
            //crossDomain: true,
            //withCredentials: true,
            // data: {
            //     Name: name,
            // }
        });
    },
    async getAllUsers() {
        return await axios({
            method: 'GET',
            url: `${getUrl()}/getUser`,
            headers: { 'content-type': 'application/json' },
            //crossDomain: true,
            //withCredentials: true,
            // data: {
            //     Name: name,
            // }
        });
    },
    async login(username, password) {
        return await axios({
            method: 'POST',
            url: `${getUrl()}/login`,
            headers: { 'content-type': 'application/json' },
            //crossDomain: true,
            //withCredentials: true,
            data: {
                username: username,
                password: password
            }
        });
    },
    async loginWithCookie(cookie) {
        return await axios({
            method: 'POST',
            url: `${getUrl()}/loginWithCookie`,
            headers: { 'content-type': 'application/json' },
            //crossDomain: true,
            //withCredentials: true,
            data: {
                token: cookie.token,
                username: cookie.username,
                userId: cookie.userId
            }
        });
    },
    async getLeaderboard() {
        return await axios({
            method: 'GET',
            url: `${getUrl()}/getLeaderboard`,
            headers: { 'content-type': 'application/json' },
            //crossDomain: true,
            //withCredentials: true,
        });
    },
    async register(username, password) {
        return await axios({
            method: 'POST',
            url: `${getUrl()}/register`,
            headers: { 'content-type': 'application/json' },
            //crossDomain: true,
            //withCredentials: true,
            data: {
                username: username,
                password: password
            }
        });
    },
    async getAllWorkoutsForUserId(userId) {
        return await axios({
            method: 'POST',
            url: `${getUrl()}/getAllWorkoutsForUserId`,
            headers: { 'content-type': 'application/json' },
            //crossDomain: true,
            //withCredentials: true,
            data: {
                userId: userId
            }
        });
    },
    async createWorkout(workout) {
        return await axios({
            method: 'POST',
            url: `${getUrl()}/createWorkout`,
            headers: { 'content-type': 'application/json' },
            //crossDomain: true,
            //withCredentials: true,
            data: {
                workout: workout
            }
        });
    }
}

function getUrl() {
    var url;
    if (document.location.hostname === 'localhost') {
        url = `http://localhost:8081`
    } else {
        url = `${window.location.origin}/`
    }
    return url;
}
export {
    api
}