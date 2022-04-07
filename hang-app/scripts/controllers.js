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
    displayErrorToast,
    getElement
} from "./utilities.js"

class Controller {

    constructor(session) {
        this.session = session;
    }

    setup() {}
}


export class StartController extends Controller {
    constructor(session) {
        super(session);
    }

    setup() {
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

    setup() {
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
                        displayErrorToast("Join Code Invalid");
                });
        });
    }

}

export class LoginController extends Controller {
    constructor(session) {
        super(session);
    }

    setup() {
        addClickListener("login__loginButton", (e) => {
            // Set session username
            const inputUsername = getElement("login__nameText").value;
            this.session.setUsername(inputUsername);
            if (this.session.startingNewSession)
                this.session.joinHangout()
                    .then(() => {
                        navigate("pickDecision");
                    })
                    .catch(e => {
                        if (e instanceof ApiError){
                            displayErrorToast(e.message);
                        }
                        console.log(e);
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

    setup() {
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
                this.session.addDecision(decisionTextBox.value)
                    .then(data => {
                        console.log(data)
                        navigate("suggest");
                    })
                    .catch(e => {
                        if (e instanceof ApiError){
                            displayErrorToast(e.message);
                        }
                        console.log(e);
                    });
            } else {
                displayErrorToast("Enter a decision")
            }
        });
    }
}

export class SuggestController extends Controller {
    constructor(session) {
        super(session);
    }

    setup() {
        this.session.getHangoutDecision()
            .then( data => {
                console.log(data);
                getElement("suggest__decisionTitle").innerHTML = data['decisionText'];
            })
            .catch(e => {
                if (e instanceof ApiError)
                    displayErrorToast(e.message);
                console.log(e);
            })


    }

}

export class VoteController extends Controller {
    constructor(session) {
        super(session);
    }

    setup() {

    }

}

export class ResultController extends Controller {
    constructor(session) {
        super(session);
    }

    setup() {

    }

}