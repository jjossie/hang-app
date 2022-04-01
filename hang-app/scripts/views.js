/***
 * Functions representing views. Each one returns a Div Element that will 
 * replace the contentContainer of index.html.
 */

import {
    renderOptionCard
} from "./components.js";

export function renderStartPage() {
    let container = document.createElement("div");
    container.innerHTML = /*html*/ `
        <button id="start__newHangoutButton" class="buttonBig">New Hangout</button>
        <button id="start__joinHangoutButton" class="buttonBig">Join Hangout</button>
    `;
    return container;
}

export function renderJoinPage() {
    let container = document.createElement("div");
    container.innerHTML = /*html*/ `
        <h2>Enter Join Code</h2>
        <input type="text" name="joinCode" id="join__codeText" class="textBoxBig box">
        <button id="join__joinHangoutButton" class="buttonMedium">Join</button>
    `;
    return container;
}

export function renderLoginPage() {
    let container = document.createElement("div");
    container.innerHTML = /*html*/ `
        <h2>What's your name?</h2>
        <input type="text" name="nameText" id="login__nameText" class="textBoxMedium" />
        <button id="login__loginButton" class="buttonMedium">Join</button>
    `;
    return container;
}

export function renderPickDecisionPage() {
    let container = document.createElement("div");
    container.innerHTML = /*html*/ `
        <h2>What are we deciding on?</h2>
        <div class="suggestionBox flexDown">
            <div id="decisionSuggestionContainer" class="chipViewContainer">
                <div class="chipView">Where should we go eat?</div>
                <div class="chipView">What movie should we watch?</div>
                <div class="chipView">Where should we hang out?</div>
            </div>
            <input type="text" name="decisionText" id="decision__decisionText" />
        </div>
        <button id="decision__startButton">Start</button>
    `;
}

export function renderSuggestPage() {
    let container = document.createElement("div");
    container.innerHTML = /*html*/ `
        <h2 id="suggest__decisionTitle" class="userGeneratedTitle"></h2>
        <div class="suggestionBox">
            <div id="suggest__optionList" class="chipView flexDown">

            </div>
            <input type="text" name="optionText" id="suggest__optionText" />
        </div>
        <button id="suggest__readyButton">Ready</button>
    `;
}

export function renderVotePage() {
    let container = document.createElement("div");
    container.innerHTML = /*html*/ `
`;
}

export function renderResultPage() {
    let container = document.createElement("div");
    container.innerHTML = /*html*/ `
`;
}