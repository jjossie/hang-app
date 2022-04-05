export function renderOptionCard(optionText) {
    const element = document.createElement("div");
    element.classList.add("optionDetailCard");
    element.innerHTML = /*html*/ `
        <h2 class="optionText">${optionText}</h1>
    `;
    return element;
}

