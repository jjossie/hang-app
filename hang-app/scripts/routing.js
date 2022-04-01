/***
 * Provides a global navigate() function which accepts a string corresponding to a destination, which
 * will display a view on index.html by replacing the contents of div#contentContainer.
 * The destination is a view function with a callback for registering callbacks.
 */


import * as view from "./views.js";



function displayPage(page, registerListenersCallback) {
    const root = document.getElementById("contentContainer");
    root.innerHTML = "";
    root.appendChild(page());
    registerListenersCallback();
}


class Destination {
    constructor(renderFunction, registerListenersFunction) {
        this.renderFunction = renderFunction;
        this.registerListenersFunction = registerListenersFunction;
    }
}


const destinations = {
    "start": new Destination(view.renderStartPage, () => {
        document.getElementById("start__newHangoutButton").addEventListener('touchend', (e) => {
            // displayPage(view.renderLoginPage());
            navigate("login");
        });
        document.getElementById("start__joinHangoutButton").addEventListener('touchend', (e) => {
            // displayPage(view.renderJoinPage());
            navigate("join");
        });
    }),
    "join": new Destination(view.renderJoinPage, () => {
        document.getElementById("join__joinHangoutButton").addEventListener('touchend', (e) => {
            // API Request with the Join Code
            // displayPage(view.renderLoginPage());
            navigate("login");
        });
    }),
    "login": new Destination(view.renderLoginPage, () => {
        document.getElementById("login__loginButton").addEventListener('touchend', (e) => {
            // API Login Request
            // navigate("pickDecision");
        });
    }),
    "pickDecision": new Destination(view.renderPickDecisionPage, () => {
        document.getElementById("decision__startButton").addEventListener('touchend', (e) => {
            // API call?
            navigate("suggest");
        });

    }),
    "suggest": new Destination(view.renderSuggestPage, () => {

    }),
    "vote": new Destination(view.renderVotePage, () => {

    }),
    "result": new Destination(view.renderResultPage, () => {

    })
};


export function navigate(destinationString) {
    const destination = destinations[destinationString];
    displayPage(destination.renderFunction, destination.registerListenersFunction);
}