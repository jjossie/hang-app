import Cookies from './js.cookie.mjs';
import {ApiError} from './utilities.js';

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


    //
    // TODO REFACTOR
    // some of these could maybe be made synchronous, since the logic for handling
    // the .then() and .catch() stuff might be more session/viewmodel/repository related.

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
        const jsonData = await this.djangoFetch(url, 'POST', body,
            "Failed to log in")
            .then(responseData => {
                // This might need refactoring still
                try {
                    this.hangoutId = responseData.hangoutId;
                    this.homieId = responseData.homieId;
                } catch {
                    throw new ApiError(`Unexpected response from ${url}`);
                }
            })
            .catch(e => {
                console.log("ok something really went wrong. Maybe the server's off?: ");
                console.log(e);
            });
    }

    /**
     * Tell the server that this homie is ready to vote
     * @returns {Promise<*>}
     */
    async readyUpHomie() {
        const url = baseApiUrl + "homie/ready-up/";
        return await this.djangoFetch(url, 'POST', {},
            "Failed to Ready Up");
    }

    async areHomiesReady() {
        const url = baseApiUrl + "hangout/" + this.hangoutId + "/is-ready/";
        return await this.djangoFetch(url, 'GET', null,
            "Could not check if the homies are ready");
    }

    /**
     * Adds a new decision to be associated with the HangoutSession.
     * @param decisionText The user-entered text describing the hangout decision to be made.
     * @returns {Promise<Response>} Resolves on successful response from the server.
     */
    async addDecision(decisionText) {
        const url = baseApiUrl + "decision-add/";
        const body = {
            "decisionText": decisionText,
            "session": this.hangoutId
        };
        return await this.djangoFetch(url, 'POST', body,
            "Failed to add Decision");
    }

    /**
     * Gets the (first) Decision associated with this Session's Hangout.
     * @returns {Promise<any>} Resolves to a Decision object, serialized from the backend.
     */
    async getHangoutDecision() {
        const url = baseApiUrl + "hangout/" + this.hangoutId + "/decision/";
        return await this.djangoFetch(url, 'GET', null,
            "Failed to get Decision")
    }

    async getOptionsForDecision(decisionId) {
        const url = baseApiUrl + "decision/" + decisionId + "/options/";
        return await this.djangoFetch(url, 'GET', null,
            "Failed to get Options for Decision");
    }


    async addOptionForDecision(decisionId, optionText) {
        const url = baseApiUrl + "option-add/" + decisionId + "/";
        const body = {
            "optionText": optionText
        }
        return await this.djangoFetch(url, 'POST', body,
            `Failed to add Option for Decision ${decisionId}`);
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
        return await this.djangoFetch(url, 'POST', body, "could not vote on option");
    }

    async getResults(decisionId){
        const url = baseApiUrl + "results/" + decisionId + "/";
        return await this.djangoFetch(url, 'GET', null,
            "Could not get results");
    }

    /**
     * Helper function for performing fetch operations on the API which
     * includes this Session's Homie ID and Hangout ID with each request.
     * @param url The URL to send the Request to.
     * @param method String representation of the HTTP method, e.g. 'GET'
     * @param body The data payload for POST/PUT requests, null for GET requests.
     * @param errorMessage Message to display to the log and/or the user if something goes wrong.
     * @returns {Promise<any>} Returns a promise of the server's response in JSON.
     */
    async djangoFetch(url, method, body, errorMessage) {

        let csrfToken = Cookies.get('csrftoken');
        // console.log(csrfToken);
        // Attach the locally stored Homie ID and Hangout ID if we have em.
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
        };
        if (body) {
            let sessionBody = body
            if (this.homieId)
                sessionBody.homieId = this.homieId;
            if (this.hangoutId)
                sessionBody.hangoutId = this.hangoutId;
            requestOptions.body = JSON.stringify(sessionBody);
        }
        // console.log(`DjangoFetch(): Sending the following request:`);
        // console.log(requestOptions);
        const response = await fetch(url, requestOptions);
        if (response.ok)
            return await response.json();
        else {
            const error = await response.text();
            console.log(JSON.parse(error));
            let apiError = new ApiError(`${errorMessage}:\n${response.statusText}`);
            apiError.errorPageText = error;
            throw apiError;
        }
    }

}