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

    // Cookies.remove('csrftoken');

    const url = baseApiUrl + "user-entry/";
    const body = {
        "username": username
    };
    const response = await djangoFetch(url, 'POST', body);
    if (response.ok) {
        return await response.json();
    } else {
        const error = await response.text();
        throw Error(`some stuff went wrong:\n${response.status} ${error}`);
    }
}

export async function voteOnOption(optionId, vote, timePassed) {
    const url = baseApiUrl + "option-vote/" + optionId;
    const body = {
        "vote": vote,
        "time_passed": timePassed
    }
    const response = await djangoFetch(url, 'POST', body);
    if (response.ok) {
        return await response.json();
    } else {
        throw Error(`could not vote on option: ${response.text().then(t => t)}`);
    }
}


/// Utility functions
async function djangoFetch(url, method, body) {

    // This isn't working apparently because fetch() doesn't store cookies, so we're never actually getting the session stuff.
    let csrfToken = Cookies.get('csrftoken');
    console.log(`csrftoken: ${csrfToken}`);
    // let sessionid = Cookies.get('sessionid')
    let requestOptions;
    if (csrfToken) {
        requestOptions = {
            method: method,
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
                // 'mode': 'same-origin'
                // 'mode': 'no-cors'
            },
            body: JSON.stringify(body)
        };
    } else {
        requestOptions = {
            method: method,
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                // 'mode': 'same-origin'
                // 'mode': 'no-cors'
            },
            body: JSON.stringify(body)
        };
    }
    console.log(`requestOptions:`);
    console.log(requestOptions);
    return await fetch(url, requestOptions);
}


// Can't figure this one out. Idk how to work with XMLHttpRequests.
// function djangoFetchX(url, method, body) {
//     const csrfToken = Cookies.get('csrftoken');
//     console.log(`csrftoken: ${csrfToken}`);
//     const requestOptions = {
//         method: method,
//         credentials: 'include',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrfToken,
//             // 'mode': 'same-origin'
//             // 'mode': 'no-cors'
//         },
//         body: JSON.stringify(body)
//     };
//
//     let xhr = new XMLHttpRequest();
//     xhr.open(method, url, true);
//     xhr.setRequestHeader('Content-Type', 'application/json');
//     xhr.setRequestHeader('X-CSRFToken', csrfToken);
//     xhr.withCredentials = true;
//
//     xhr.send();
//     return xhr.response;
// }

// function getCookie(name) {
//     const value = `; ${document.cookie}`;
//     const parts = value.split(`; ${name}=`);
//     if (parts.length === 2) return parts.pop().split(';').shift();
// }