import Cookies from './js.cookie.mjs';
import {
    ApiError,
    displayError,
    overwritePage
} from './utilities.js';

const baseApiUrl = "http://localhost:8000/api/";

/**
 * Represents the state of the user's session to be maintained
 * between calls and stuff and also possibly stored in LocalStorage.
 * Contains all necessary methods for interacting with the backend.
 */
export class Session {
    constructor() {
        this.username = "";
        this.hangoutId = null;
        this.homieId = null;
        this.startingNewSession = true;
    }
    setUsername(username) {
        this.username = username;
    }
    getUsername() {
        return this.username;
    }

    async joinHangout(hangoutId) {
        let url = baseApiUrl + "join-hangout/";
        // Add the hangoutID to the request if necessary
        if (hangoutId)
            url += hangoutId

        const body = {
            "username": this.username
        };
        const response = await this.djangoFetch(url, 'POST', body);
        if (response.ok) {
            response.json()
                .then(responseData => {
                    try {
                        this.hangoutId = responseData.hangoutId;
                        this.homieId = responseData.homieId;
                    } catch {
                        throw new ApiError(`Unexpected response from ${url}`);
                    }
                });
        } else {
            const error = await response.text();
            // displayError(response.statusText)
            // overwritePage(error);
            throw new ApiError(`some stuff went wrong:\n${response.status}`);
        }
    }

    async voteOnOption(optionId, vote, timePassed) {
        const url = baseApiUrl + "option-vote/" + optionId;
        const body = {
            "vote": vote,
            "time_passed": timePassed
        }
        const response = await djangoFetch(url, 'POST', body);
        if (response.ok) {
            return await response.json();
        } else {
            throw new ApiError(`could not vote on option: ${response.text().then(t => t)}`);
        }
    }

    /**
     * Helper function for performing fetch operations on the API which
     * includes the Session's Homie ID and Hangout ID with each request.
     */
    async djangoFetch(url, method, body) {

        let csrfToken = Cookies.get('csrftoken');
        console.log(`csrftoken: ${csrfToken}`);

        // Attach the locally stored Homie ID and Hangout ID if we have em.
        let sessionBody = body
        if (this.homieId)
            sessionBody.homieId = this.homieId;
        if (this.hangoutId)
            sessionBody.hangoutId = this.hangoutId;
        let requestOptions = {
            method: method,
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
                // 'mode': 'same-origin'
                // 'mode': 'no-cors'
            },
            body: JSON.stringify(sessionBody)
        };
        console.log(`requestOptions:`);
        console.log(requestOptions);
        return await fetch(url, requestOptions);
    }

}