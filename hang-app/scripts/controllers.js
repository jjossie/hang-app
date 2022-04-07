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
import {renderOptionListItem} from "./components.js";

const REFRESH_INTERVAL = 5000;

class Controller {

    constructor(session) {
        this.session = session;
    }

    registerListeners() {
    }

    refreshView() {
    }

    setup() {
    }
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
                        if (e instanceof ApiError) {
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
        const suggestionChips = document.getElementsByClassName("chipView");
        for (let chip of suggestionChips) {
            chip.addEventListener('touchend', () => {
                decisionTextBox.value = chip.innerHTML;
            });
        }

        addClickListener("decision__startButton", (e) => {
            // API call?
            if (decisionTextBox.value) {
                this.session.addDecision(decisionTextBox.value)
                    .then(data => {
                        // console.log(data);
                        navigate("suggest");
                    })
                    .catch(e => {
                        if (e instanceof ApiError) {
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
        // TODO move all these attributes into Session
        //  (Session is like the repository/ViewModel, whereas Controllers
        //  are like the Activity/Fragment classes in Android). They shouldn't
        //  hold data, just control behavior.
        this.decision = {};
        this.options = [];
        this.ready = false;
        this.timeoutIds = [];
    }

    refreshView() {
        console.log("RefreshView() called");
        // Get the Decision Title
        this.session.getHangoutDecision()
            .then(data => {
                this.decision = data;
                // Display the title
                getElement("suggest__decisionTitle").innerHTML = data['decisionText'];
            })
            .then(() => {
                const listContainer = getElement("suggest__optionList");
                // Get all the options
                this.session.getOptionsForDecision(this.decision['decisionId'])
                    .then(jsonData => {
                        // Display all the options
                        listContainer.innerHTML = "";
                        console.log("JSON DATA: ");
                        console.log(jsonData);
                        for (let option of jsonData['options']) {
                            // console.log(option);
                            listContainer.appendChild(renderOptionListItem(option));
                        }
                    })
            })
            .catch(e => {
                if (e instanceof ApiError)
                    displayErrorToast(e.message);
                console.log(e);
            });
        if (this.ready) {
            const readyButton = getElement("suggest__readyButton");
            readyButton.innerHTML = "Waiting for others...";
            readyButton.classList.add("greyedOut");
        }
    }

    registerListeners() {
        let thisInstance = this;
        const form = getElement('suggest__submitSuggestionForm');
        form.addEventListener('submit', e => {
            e.preventDefault();
            // API call to add Options
            const optionTextBox = getElement("suggest__optionText");
            const optionText = optionTextBox.value;
            if (optionText) {
                this.session.addOptionForDecision(this.decision['decisionId'], optionText)
                    .then(() => {
                        // Clear the text input field
                        optionTextBox.value = "";
                        thisInstance.refresh();
                    })
                    .catch(e => {
                        console.log(e);
                    });
            } else {
                displayErrorToast("Option can't be empty");
            }
        });
        addClickListener("suggest__readyButton", () => {
            // API Call to ready up
            console.log("Readying up on the frontend");
            this.session.readyUpHomie()
                .then((response) => {
                    console.log(response);
                    console.log("Readied up on the backend");
                    thisInstance.ready = true;
                    thisInstance.refresh();
                })
                .catch(e => {
                    console.log(e);
                });
        });
    }

    refresh() {
        let thisInstance = this;
        if (this.ready) {
            this.session.areHomiesReady()
                .then(result => {
                    console.log(result);
                    if (result['areHomiesReady']){
                        console.log("Everyone's ready!");
                        // Clear timers
                        this.timeoutIds.forEach(id => {
                            clearTimeout(id);
                        });
                        this.timeoutIds = [];
                        navigate("vote");
                    }
                });
        }
        this.refreshView();
        // Don't re-register listeners
        const timeoutId = window.setTimeout(() => {
            thisInstance.refresh();
        }, REFRESH_INTERVAL);
        this.timeoutIds.push(timeoutId);
    }

    setup() {
        // Only Called Once, on View Load
        this.registerListeners();
        this.refresh();
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