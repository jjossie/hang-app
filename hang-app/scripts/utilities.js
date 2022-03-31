const baseUrl = "http://localhost:8000/";

export async function getAllOptions() {
    const url = baseUrl + "api/options/"

    const response = await djangoFetch(url, 'GET');
    if (response.ok) {
        return await response.json();
    } else {
        throw Error();
    }
}

async function djangoFetch(url, method) {
    let csrfToken = getCookie('csrftoken');
    let requestOptions = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
            // 'mode': 'no-cors'
        },
    };
    return await fetch(url, requestOptions);
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}