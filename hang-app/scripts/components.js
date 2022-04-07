export function renderOptionCard(optionText) {
    const element = document.createElement("div");
    element.classList.add("optionDetailCard");
    element.innerHTML = /*html*/ `
        <h2 class="optionText">${optionText}</h2>
    `;
    return element;
}

export function renderOptionListItem(option) {
    const element = document.createElement("div");
    element.classList.add("optionListItem")
    element.innerHTML = /*html*/ `
        ${option['optionText']}
    `;
    return element;
}