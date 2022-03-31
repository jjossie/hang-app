import Cookies from './js.cookie.mjs';


const baseApiUrl = "http://localhost:8000/api/";


/// API Calls
export async function getAllOptions() {
    const url = baseApiUrl + "options/";

    const response = await djangoFetch(url, 'GET');
    if (response.ok) {
        return await response.json();
    } else {
        throw Error(`Login failed due to:\n ${response.error()}`);
    }
}

export async function login(username) {
    const url = baseApiUrl + "user-entry/";
    const body = {
        "username": username
    };
    const response = await djangoFetch(url, 'POST', body);
    if (response.ok){
        return await response.json();
    } else {
        throw Error(`some stuff went wrong:\n${response.status} ${response.text().then((t)=>t)}`);
    }
}



/// Utility functions
async function djangoFetch(url, method, body) {
    let csrfToken = Cookies.get('csrftoken');
    let requestOptions = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
            // 'mode': 'same-origin'
            // 'mode': 'no-cors'
        },
        body: JSON.stringify(body)
    };
    return await fetch(url, requestOptions);
}

// function getCookie(name) {
//     const value = `; ${document.cookie}`;
//     const parts = value.split(`; ${name}=`);
//     if (parts.length === 2) return parts.pop().split(';').shift();
// }