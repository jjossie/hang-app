export function renderOptionCard(optionText) {
    const element = document.createElement("div");
    element.classList.add("optionDetailCard");
    element.innerHTML = /*html*/ `
        <form id="vote__voteForm">
            <button type="submit" id="vote__YesButton" class="box buttonVote">Yes</button>
            <h2 id="vote__optionText" class="optionText">${optionText}</h2>
            <button type="submit" id="vote__NoButton" class="box buttonVote">No</button>
        </form>
    `;
    return element;
}

export function renderOptionListItem(option) {
    const element = document.createElement("div");
    element.classList.add("optionListItem");
    element.innerHTML = /*html*/ `
        ${option['optionText']}
    `;
    return element;
}