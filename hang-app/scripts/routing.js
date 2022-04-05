/***
 * Provides a global navigate() function which accepts a string corresponding to a destination, which
 * will display a view on index.html by replacing the contents of div#contentContainer.
 * The destination is a view function with a callback for registering callbacks.
 */


import * as view from "./views.js";
import {
    JoinController,
    LoginController,
    PickDecisionController,
    ResultController,
    StartController,
    SuggestController,
    VoteController
} from "./controllers.js";
import { login } from "./utilities.js";



function displayPage(page, controller) {
    const root = document.getElementById("contentContainer");
    root.innerHTML = "";
    root.appendChild(page());
    controller.registerEventListeners();
}


/**
 * Represents the state of the user's session to be maintained
 * between calls and stuff and also possibly stored in LocalStorage
 */
class Session {
    constructor() {
        this.username = "";
        this.hangoutId = null;
    }
    setUsername(username) {
        this.username = username;
    }
    getUsername() {
        return this.username;
    }

    async joinHangout(){
        const loginResponse = await login(this.username);
        console.log(loginResponse);
        if (loginResponse["username"] != this.username){
            throw Error("Client/server username mismatch");
        }
        
        // if (!this.session.hangoutId){
        //     // If we haven't specified a session to join, make a new one
            
        // } else {

        // }
    }

}


class Destination {
    constructor(renderFunction, controller) {
        this.renderFunction = renderFunction;
        this.controller = controller;
    }
}

const userSession = new Session();

const destinations = {
    "start": new Destination(view.renderStartPage, new StartController(userSession)),
    "join": new Destination(view.renderJoinPage, new JoinController(userSession)),
    "login": new Destination(view.renderLoginPage, new LoginController(userSession)),
    "pickDecision": new Destination(view.renderPickDecisionPage, new PickDecisionController(userSession)),
    "suggest": new Destination(view.renderSuggestPage, new SuggestController(userSession)),
    "vote": new Destination(view.renderVotePage, new VoteController(userSession)),
    "result": new Destination(view.renderResultPage, new ResultController(userSession))
};


export function navigate(destinationString) {
    const destination = destinations[destinationString];
    displayPage(destination.renderFunction, destination.controller);
}