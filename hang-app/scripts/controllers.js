/**
 * Controller Classes, which will each be associated with a view. 
 * Allows controlling DOM related behavior, including implementing 
 * click listeners and triggering navigation.
 */


import {
    navigate
} from "./routing.js";
import {
    addClickListener,
    ApiError,
    displayError,
    getElement
} from "./utilities.js"

class Controller {

    constructor(session) {
        this.session = session;
    }

    registerEventListeners() {}
}


export class StartController extends Controller {
    constructor(session) {
        super(session);
    }

    registerEventListeners() {
        addClickListener("start__newHangoutButton", (e) => {
            navigate("login");
        });
        addClickListener("start__joinHangoutButton", (e) => {
            this.session.startingNewSession = false;
            navigate("login");
        });
    }

}

export class JoinController extends Controller {
    constructor(session) {
        super(session);
    }

    registerEventListeners() {
        addClickListener("join__joinHangoutButton", (e) => {
            // API Request with the Join Code
            const inputJoinCode = getElement("join__codeText").value
            this.session.joinHangout(inputJoinCode)
                .then(() => {
                    navigate("pickDecision");
                })
                .catch((e) => {
                    console.log(e);
                    if (e instanceof ApiError)
                        displayError("Join Code Invalid");
                });
        });
    }

}

export class LoginController extends Controller {
    constructor(session) {
        super(session);
    }

    registerEventListeners() {
        addClickListener("login__loginButton", (e) => {
            // Set session username
            const inputUsername = getElement("login__nameText").value;
            this.session.setUsername(inputUsername);
            if (this.session.startingNewSession)
                this.session.joinHangout()
                    .then(() => {
                        navigate("pickDecision");
                    });
            else
                navigate("join");
        });
    }

}


export class PickDecisionController extends Controller {
    constructor(session) {
        super(session);
    }

    registerEventListeners() {
        const decisionTextBox = getElement("decision__decisionText");
        console.log(decisionTextBox);
        const suggestionChips = document.getElementsByClassName("chipView");
        for (let chip of suggestionChips){
            chip.addEventListener('touchend', () => {
                decisionTextBox.value = chip.innerHTML;
            });
        }

        addClickListener("decision__startButton", (e) => {
            // API call?
            if (decisionTextBox.value){
                // this.session.
                navigate("suggest");
            } else {
                displayError("Enter a decision")
            }
        });
    }
}

export class SuggestController extends Controller {
    constructor(session) {
        super(session);
    }

    registerEventListeners() {

    }

}

export class VoteController extends Controller {
    constructor(session) {
        super(session);
    }

    registerEventListeners() {

    }

}

export class ResultController extends Controller {
    constructor(session) {
        super(session);
    }

    registerEventListeners() {

    }

}