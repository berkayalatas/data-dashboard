const searchField = document.querySelector("#searchField");

const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
tableOutput.style.display = "none";
const noResults = document.querySelector(".no-results");
const tbody = document.querySelector(".table-body");

// run the function once we type to search input field
searchField.addEventListener("keyup", (e) => {
    const searchValue = e.target.value;

    // trim : removes whitespace from both ends of a string and returns a new string
    if (searchValue.trim().length > 0) {
        paginationContainer.style.display = "none";
        tbody.innerHTML = "";
         //fetch json data and stringify 
        fetch("/income/search-income", {
                body: JSON.stringify({
                    searchText: searchValue
                }),
                method: "POST",
            })
            .then((res) => res.json())
            .then((data) => {
                //console.log("data", data);
                appTable.style.display = "none";
                tableOutput.style.display = "block";

                if (data.length === 0) {
                    noResults.style.display = "block";
                    tableOutput.style.display = "none";
                } else {
                    noResults.style.display = "none";
                    data.forEach((item) => {
                        tbody.innerHTML += `
                <tr>
                <td>${item.amount}</td>
                <td>${item.source}</td>
                <td>${item.description}</td>
                <td>${item.date}</td>
                </tr>`;
                    });
                }
            });
    } else {
        tableOutput.style.display = "none";
        appTable.style.display = "block";
        paginationContainer.style.display = "block";
    }
});