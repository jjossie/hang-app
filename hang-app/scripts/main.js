import { renderOptionCard } from "./components.js";

const contentContainer = document.getElementById("contentContainer");

contentContainer.appendChild(renderOptionCard(
    "This is some more sample option text"
));
