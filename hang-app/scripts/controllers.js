import {navigate} from "./routing.js";

class Controller {
    registerEventListeners(){}
}


export class StartController extends Controller {
    constructor() {
        super();
    }

    registerEventListeners() {
        document.getElementById("start__newHangoutButton").addEventListener('touchend', (e) => {
            // displayPage(view.renderLoginPage());
            navigate("login");
        });
        document.getElementById("start__joinHangoutButton").addEventListener('touchend', (e) => {
            // displayPage(view.renderJoinPage());
            navigate("join");
        });
    }

}

export class JoinController extends Controller {
    constructor() {
        super();
    }

    registerEventListeners() {
        document.getElementById("join__joinHangoutButton").addEventListener('touchend', (e) => {
            // API Request with the Join Code
            // displayPage(view.renderLoginPage());
            navigate("login");
        });
    }

}

export class LoginController extends Controller {
    constructor() {
        super();
    }   

    registerEventListeners(){
        document.getElementById("login__loginButton").addEventListener('touchend', (e) => {
            // API Login Request
            // navigate("pickDecision");
        });
    }

}


export class PickDecisionController extends Controller {
    constructor() {
        super();
    }   
    
    registerEventListeners(){
        document.getElementById("decision__startButton").addEventListener('touchend', (e) => {
            // API call?
            navigate("suggest");
        });
    }
}

export class SuggestController extends Controller {
    constructor() {
        super();
    }

    registerEventListeners() {
        
    }

}

export class VoteController extends Controller {
    constructor() {
        super();
    }

    registerEventListeners() {
        
    }

}

export class ResultController extends Controller {
    constructor() {
        super();
    }

    registerEventListeners() {
        
    }

}