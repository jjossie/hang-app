import {displayPage, renderOptionCard, renderStartPage, Router} from "./components.js";
import {getAllOptions} from "./utilities.js";

const contentContainer = document.getElementById("contentContainer");

// contentContainer.appendChild(renderOptionCard(
//     "This is some more sample option text"
// ));
getAllOptions()
    .then((data) => {
        for (const option of data) {
            console.log(option);
            contentContainer.appendChild(
                renderOptionCard(option.optionText)
            );
        }
    });
// const r = new Router();
// r.navigateToStart();
// renderStartPage();