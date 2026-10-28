/**
 * app.js
 *
 * Author: Abraham Horta
 *
 * Purpose: This file manages the frontend logic for sending requests to the FastAPI backend.
 * It handles user login, JWT token storage, protected transaction requests, and displays API
 * responses, dynamically within the user interface.
 *
 * Sources: The following code was inspired/influenced by the following
 *     -- sources, but adapted and altered for the API project.
 *
 * 1. https://www.w3schools.com/
 * 2. https://www.youtube.com/watch?v=vqjZOyT4QRs
 * 3. https://blog.logrocket.com/server-side-rendering-with-fastapi-and-mysql/
 */

let accessToken = "";

function showResponse(data)
    {
        document.getElementById("responseBox").textContent =
            JSON.stringify(data, null, 2);
    }

async function loginUser()
    {
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        const response = await fetch("/login",
            {method: "POST",
                headers:{"Content-Type": "application/json"},
                body: JSON.stringify({username: username, password: password})
            });

        const data = await response.json();

        if (data.access_token)
        {
            accessToken = data.access_token;
            showResponse({Message: "Login successful", Token: accessToken});
        }
        else
        {
            showResponse(data);
        }
    }

async function createTransaction()
    {
        const amount = parseFloat(document.getElementById("amount").value);

        const currency = document.getElementById("currency").value;
        const description = document.getElementById("description").value;

        const response = await fetch("/create_transaction",
            {method: "POST", headers: {"Content-Type": "application/json",
                    "Authorization": `Bearer ${accessToken}`},
                body: JSON.stringify({amount: amount, currency: currency, description: description})
            });

        const data = await response.json();
        showResponse(data);
    }

async function updateTransaction()
    {
        const transaction_id = parseInt(document.getElementById("transaction_id").value);

        const new_status = document.getElementById("new_status").value;

        const response = await fetch("/update_transaction",
            {method: "POST", headers: {"Content-Type": "application/json",
                    "Authorization": `Bearer ${accessToken}`},
                body: JSON.stringify({transaction_id: transaction_id, new_status: new_status})
            });

        const data = await response.json();
        showResponse(data);
    }