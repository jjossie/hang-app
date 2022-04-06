import Cookies from './js.cookie.mjs';
import {ApiError, overwritePage} from './utilities.js';

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

    /**
     * Tells the backend to join a user to a hangout. Also creates the user if they
     * did not exist in the database already. If a hangoutId is not specified, it will
     * call the appropriate API endpoint to create a new Hangout.
     * @param hangoutId The ID of the hangout to be joined (entered by the user)
     * @returns {Promise<void>} Resolves when the hangout is joined on the backend
     * and a response with an OK status is received.
     */
    async joinHangout(hangoutId = null) {
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
            throw new ApiError(`Failed to log in:\n${response.status}`);
        }
    }

    async addDecision(decisionText) {
        const url = baseApiUrl + "decision-add/";
        // const hangoutUrl = baseApiUrl + "hangoutViewSet/" + this.hangoutId + "/";
        const body = {
            "decisionText": decisionText,
            "session": this.hangoutId
        };
        const response = await this.djangoFetch(url, 'POST', body);
        if (response.ok) {

        } else {
            const error = await response.text();
            // console.log(error);
            // overwritePage(error);
            console.log(JSON.parse(error));
            throw new ApiError(`Failed to add Decision:\n${response.statusText}`);
        }
    }

    /**
     * API Call to have a user vote on a particular option.
     * @param optionId The option to vote on.
     * @param vote an int: 0 for no, 1 for neutral, 2 for yes.
     * @param timePassed The time it took the user to decide, in milliseconds.
     * @returns {Promise<*>} Resolves on successful response from server.
     */
    async voteOnOption(optionId, vote, timePassed) {
        const url = baseApiUrl + "option-vote/" + optionId + "/";
        const body = {
            "vote": vote,
            "time_passed": timePassed
        }
        const response = await this.djangoFetch(url, 'POST', body);
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
        console.log(csrfToken);
        // Attach the locally stored Homie ID and Hangout ID if we have em.
        let sessionBody = body
        if (this.homieId)
            sessionBody.homieId = this.homieId;
        if (this.hangoutId)
            sessionBody.hangoutId = this.hangoutId;
        let requestOptions = {
            method: method,
            mode: 'cors',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                // 'Accept': 'application/json',
                // 'Access-Control-Allow-Origin': 'http://localhost:5500',
                'Access-Control-Allow-Credentials': 'true',
                'X-CSRFToken': csrfToken,
                // 'mode': 'same-origin'
                // 'mode': 'cors'
            },
            body: JSON.stringify(sessionBody)
        };
        console.log(`DjangoFetch(): Sending the following request:`);
        console.log(requestOptions);
        return await fetch(url, requestOptions);
    }

}