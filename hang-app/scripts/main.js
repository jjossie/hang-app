// import {displayPage, renderOptionCard, renderStartPage} from "./components.js";
import {getAllOptions, login, voteOnOption} from "./utilities.js";
import { navigate } from "./routing.js";

const contentContainer = document.getElementById("contentContainer");

// contentContainer.appendChild(renderOptionCard(
//     "This is some more sample option text"
// ));

// login("JoeMomma")
//     .then((data) => {
//         // data.json().then(t => console.log(t));
//         console.log(data);
//     })
//     .then(()=> {
//         voteOnOption(1, 2, 0)
//             .then(d => console.log(d));
//     })
//     .catch((p) => {
//         console.log(p);
//     });


// getAllOptions()
//     .then((data) => {
//         for (const option of data) {
//             console.log(option);
//             contentContainer.appendChild(
//                 renderOptionCard(option.optionText)
//             );
//         }
//     });

navigate("start");

// const r = new Router();
// r.navigateToStart();
// renderStartPage();