/***
 * Provides a global navigate() function which accepts a string corresponding to a destination, which
 * will display a view on index.html by replacing the contents of div#contentContainer.
 * The destination is a view function with a callback for registering callbacks.
 */


import * as view from "./views.js";
import {JoinController, LoginController, PickDecisionController, ResultController, StartController, SuggestController, VoteController} from "./controllers.js";



function displayPage(page, controller) {
    const root = document.getElementById("contentContainer");
    root.innerHTML = "";
    root.appendChild(page());
    controller.registerEventListeners();
}


class Destination {
    constructor(renderFunction, controller) {
        this.renderFunction = renderFunction;
        this.controller = controller;
    }
}


const destinations = {
    "start": new Destination(view.renderStartPage, new StartController()),
    "join": new Destination(view.renderJoinPage, new JoinController()),
    "login": new Destination(view.renderLoginPage, new LoginController()),
    "pickDecision": new Destination(view.renderPickDecisionPage, new PickDecisionController()),
    "suggest": new Destination(view.renderSuggestPage, new SuggestController()),
    "vote": new Destination(view.renderVotePage, new VoteController()),
    "result": new Destination(view.renderResultPage, new ResultController())
};


export function navigate(destinationString) {
    const destination = destinations[destinationString];
    displayPage(destination.renderFunction, destination.controller);
}