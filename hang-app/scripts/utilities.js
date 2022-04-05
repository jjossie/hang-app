import Cookies from './js.cookie.mjs';

/// User Error Handling
export function displayError(errorMessage){
    const box = getElement("errorBox");
    box.innerHTML = errorMessage;
    box.hidden = false;
    window.setTimeout(() => {
        box.hidden = true;
        box.innerHTML = "";
    }, 3000);
}


/// Front-end Utility Functions
export function getElement(id) {
    return document.getElementById(id);
}

export function addClickListener(id, callback){
    getElement(id).addEventListener('touchend', callback);
    // getElement(id).addEventListener('click', callback);
}

export function displayPage(page, controller) {
    const root = document.getElementById("contentContainer");
    root.innerHTML = "";
    root.appendChild(page());
    controller.registerEventListeners();
}

export function overwritePage(page){
    const root = document.getElementsByTagName("body")[0];
    root.innerHTML = page;
}


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


/// Utility functions

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