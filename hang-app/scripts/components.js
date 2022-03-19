export function renderOptionCard(optionText) {
    const element = document.createElement("div");
    element.classList.add("optionDetailCard");
    const html = `
        <h2 class="optionText">${optionText}</h1>
    `;
    element.innerHTML = html;
    return element;
}