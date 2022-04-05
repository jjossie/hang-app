import {navigate} from "./routing.js";
import {addClickListener, getElement} from "./utilities.js"

class Controller {

    constructor(session){
        this.session = session;
    }

    registerEventListeners(){}
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
            navigate("join");
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
            navigate("login");
        });
    }

}

export class LoginController extends Controller {
    constructor(session) {
        super(session);
    }   

    registerEventListeners(){
        addClickListener("login__loginButton", (e) => {
            // Set session username
            const inputUsername = getElement("login__nameText").value;
            this.session.setUsername(inputUsername);
            this.session.joinHangout();
            // API Login Request
            // navigate("pickDecision");
        });
    }

}


export class PickDecisionController extends Controller {
    constructor(session) {
        super(session);
    }   
    
    registerEventListeners(){
        addClickListener("decision__startButton", (e) => {
            // API call?
            navigate("suggest");
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