export function renderOptionCard(optionText) {
    const element = document.createElement("div");
    element.classList.add("optionDetailCard");
    element.innerHTML = `
        <h2 class="optionText">${optionText}</h1>
    `;
    return element;
}


export function renderStartPage() {
    let container = document.createElement("div");
    container.innerHTML = `
        <button id="newHangoutButton" class="buttonBig">New Hangout</button>
        <button id="joinHangoutButton" class="buttonBig">Join Hangout</button>
    `;
    return container;
}

function renderJoinPage() {
}

function renderLoginPage() {
}

function renderPickDecisionPage() {
}

function renderSuggestPage() {
}

function renderVotePage() {
}

function renderResultPage() {
}


export function displayPage(page, registerListenersCallback) {
    const root = document.getElementById("contentContainer");
    root.innerHTML = "";
    root.appendChild(page);
    registerListenersCallback();
}

export class Router {
    navigateToStart() {
        displayPage(renderStartPage(), () => {
            document.getElementById("newHangoutButton").addEventListener('touchend', () => {
                displayPage(renderLoginPage());
            });
            document.getElementById("joinHangoutButton").addEventListener('touchend', (e) => {
                displayPage(renderJoinPage());
            });
        });
    }
}
