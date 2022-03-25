import {displayPage, renderOptionCard, renderStartPage, Router} from "./components.js";

const contentContainer = document.getElementById("contentContainer");

// contentContainer.appendChild(renderOptionCard(
//     "This is some more sample option text"
// ));

const baseUrl = "http://localhost:8000/";
const url = baseUrl + "api/options/"

async function getAllOptions() {
    let requestOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            // 'mode': 'no-cors'
        },
        // mode: 'no-cors'
    };
    const response = await fetch(url, requestOptions);
    console.log(response);
    if (response.ok) {
        const data = await response.json();
        console.log(data[0]);
        for (const option of data) {
            console.log(option);
            contentContainer.appendChild(
                renderOptionCard(option.optionText)
            );
        }
        return data;
    } else {
        throw Error();
    }
}

// getAllOptions();
const r = new Router();
r.navigateToStart();
// renderStartPage();