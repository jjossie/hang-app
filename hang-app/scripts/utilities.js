import Cookies from './js.cookie.mjs';

/// User Error Handling
export function displayErrorToast(errorMessage){
    const box = getElement("errorBox");
    box.innerHTML = errorMessage;
    // box.hidden = false;
    box.classList.remove('hide');
    window.setTimeout(() => {
        // box.hidden = true;
        box.classList.add('hide');
        box.innerHTML = "";
    }, 3000);
}

export class ApiError extends Error {
    constructor (message){
        super(message);
        this.name = "ApiError";
        this.errorPageText = null;
    }
}


/// Front-end Utility Functions
export function getElement(id) {
    return document.getElementById(id);
}

export function addClickListener(id, callback){
    getElement(id).addEventListener('touchend', callback);
    getElement(id).addEventListener('click', callback);
}

export function displayPage(page, controller) {
    const root = document.getElementById("contentContainer");
    root.innerHTML = "";
    let newPage = page();
    root.appendChild(newPage);
    controller.root = newPage;
    controller.setup();
}

export function overwritePage(page){
    const root = document.getElementsByTagName("body")[0];
    root.innerHTML = page;
}