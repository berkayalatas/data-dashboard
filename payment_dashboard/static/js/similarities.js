const getExpenseAndIncomeData = () => {
    /* Fetch Expense Data */
    fetch('/expense_category_summary').then((res) => res.json()).then((result) => {
        const category_data = result.expense_category_data;
        const expenseDataArr = Object.values(category_data);
        //console.log(expenseDataArr)
        localStorage.setItem('expenseData', JSON.stringify(expenseDataArr)); //save to localStorage
    })
    /* Fetch Income Data */
    fetch('/income/income_source_summary').then((res) => res.json()).then((result) => {
        const category_data = result.income_source_data;
        const incomeDataArr = Object.values(category_data);
        //console.log(incomeDataArr)
        localStorage.setItem('incomeData', JSON.stringify(incomeDataArr)); //save to localStorage
    })
 
}
var expenseData = JSON.parse(localStorage.getItem('expenseData'))
var incomeData = JSON.parse(localStorage.getItem('incomeData'))
//console.log(expenseData); 


/* Expense Table */
function createExpenseTable(expenseData) {
    let counter = 0;
    for (let i = 0; i < expenseData?.length; i++) {
        document.getElementById('expense').innerHTML += (`          
            <tr>
                <th scope="row">${++counter}</th>
                <td>${expenseData[i]}</td>
            </tr>`)
    }
}

/* Income  Table */
function createIncomeTable(incomeData) {
    let counter = 0;
    for (let i = 0; i < incomeData?.length; i++) {
        document.getElementById('income').innerHTML += (`          
            <tr>
                <th scope="row">${++counter}</th>
                <td>${incomeData[i]}</td>
            </tr>`)
    }
}

/*  Calculate Means */
const getExpenseMean = (expenseData) => {
    const mean = expenseData.reduce((a, b) => a + b) / expenseData.length;
    document.getElementById('expenseMean').innerHTML = (`Expense Mean:<b> ${mean}</b>`)
}

const getIncomeMean = (incomeData) => {
    const mean = incomeData.reduce((a, b) => a + b) / incomeData.length;
    document.getElementById('incomeMean').innerHTML = (`Income Mean:<b> ${mean}</b>`)
}

/*  Calculate Variance */
const getExpenseVariance = (expenseData) => {
    const n = expenseData.length
    const mean = expenseData.reduce((a, b) => a + b) / n;
    const variance = expenseData.map(x => Math.pow(x - mean, 2)).reduce((a, b) => a + b) / n
    document.getElementById('expenseVariance').innerHTML = (`Expense Variance: <b> ${variance.toFixed(2)} </b>`)
}

const getIncomeVariance = (incomeData) => {
    const n = incomeData.length
    const mean = incomeData.reduce((a, b) => a + b) / n;
    const variance = incomeData.map(x => Math.pow(x - mean, 2)).reduce((a, b) => a + b) / n
    document.getElementById('incomeVariance').innerHTML = (`Income Variance: <b>${variance.toFixed(2)}</b> `)
}


/*  Calculate standard-deviation */
const getExpenseStd = (expenseData) => {
    const n = expenseData.length
    const mean = expenseData.reduce((a, b) => a + b) / n;
    const std = Math.sqrt(expenseData.map(x => Math.pow(x - mean, 2)).reduce((a, b) => a + b) / n)
    document.getElementById('expenseStd').innerHTML = (`Expense Standard Deviation: <b> ${std.toFixed(2)} </b>`)
}

const getIncomeStd = (incomeData) => {
    const n = incomeData.length
    const mean = incomeData.reduce((a, b) => a + b) / n;
    const std = Math.sqrt(incomeData.map(x => Math.pow(x - mean, 2)).reduce((a, b) => a + b) / n)
    document.getElementById('incomeStd').innerHTML = (`Income Standard Deviation: <b>${std.toFixed(2)}</b> `)
}

// Function to find covariance.
function covariance(expenseData, incomeData) {
    n = incomeData.length > expenseData.length ? incomeData.length : expenseData.length
    let sum = 0;
    let mean_expense = expenseData.reduce((a, b) => a + b) / n;
    let mean_income = incomeData.reduce((a, b) => a + b) / n;
    for (let i = 0; i < n; i++)
        sum = sum + (expenseData[i] - mean_expense) * (incomeData[i] - mean_income);

    document.getElementById('covariance').innerHTML = (`Covariance: <b>${(sum / (n - 1)).toFixed(2)}</b> `)
}

// Function to find correlation.
function correlation(expenseData, incomeData) {
    n = incomeData.length > expenseData.length ? incomeData.length : expenseData.length
    let sum = 0;
    let mean_expense = expenseData.reduce((a, b) => a + b) / n;
    let mean_income = incomeData.reduce((a, b) => a + b) / n;
    for (let i = 0; i < n; i++)
        sum = sum + (expenseData[i] - mean_expense) * (incomeData[i] - mean_income);

    let covariance = sum / (n - 1)
    let std_expense = Math.sqrt(expenseData.map(x => Math.pow(x - mean_expense, 2)).reduce((a, b) => a + b) / n)
    let std_income = Math.sqrt(incomeData.map(y => Math.pow(y - mean_income, 2)).reduce((a, b) => a + b) / n)

    let correlation = covariance / (std_expense * std_income);
    document.getElementById('correlation').innerHTML = (`Correlation: <b>${(correlation).toFixed(2)}</b> `)
}

/* Cosine Similarity */
function cosinesim(expenseData, incomeData) {
    var multiply = 0;
    var normexpenseData = 0;
    var normIncomeData = 0;
    for (i = 0; i < expenseData.length; i++) {
        multiply += (expenseData[i] * incomeData[i]);
        normexpenseData += (expenseData[i] * expenseData[i]);
        normIncomeData += (incomeData[i] * incomeData[i]);
    }
    normexpenseData = Math.sqrt(normexpenseData);
    normIncomeData = Math.sqrt(normIncomeData);
    var similarity = (multiply) / ((normexpenseData) * (normIncomeData))

    document.getElementById('cossimilarity').innerHTML = (`Cosine Similarity: <b>${(similarity).toFixed(2)}</b> `)
}

/* Manhattan Distance */
function manhattanDistance(expenseData, incomeData) {
    let sum = 0;
    let n = expenseData.length
    // for each point, finding distance to
    // rest of the point
    for (let i = 0; i < n; i++)
        for (let j = i + 1; j < n; j++)
            sum += (Math.abs(expenseData[i] - expenseData[j]) + Math.abs(incomeData[i] - incomeData[j]));
    document.getElementById('manhattanDistance').innerHTML = (`Manhattan Distance: <b>${(sum).toFixed(2)}</b> `)
}

function eucDistance(expenseData, incomeData) {
    const eucDistance = expenseData.map((x, i) => Math.abs(x - incomeData[i]) ** 2) // square the difference
        .reduce((sum, now) => sum + now) ** (1 / 2) // sum and sqrt

    document.getElementById('eucDistance').innerHTML = (`Euclidean Distance: <b>${(eucDistance).toFixed(2)}</b> `)    
}

//fetch expense and income data


 
getExpenseAndIncomeData();

 
setTimeout(() =>{
    //expense functions
createExpenseTable(expenseData);
getExpenseMean(expenseData);
getExpenseVariance(expenseData);
getExpenseStd(expenseData);

//income functions
createIncomeTable(incomeData);
getIncomeMean(incomeData);
getIncomeVariance(incomeData);
getIncomeStd(incomeData);


covariance(expenseData, incomeData);
correlation(expenseData, incomeData);
cosinesim(expenseData, incomeData);
manhattanDistance(expenseData, incomeData);
eucDistance(expenseData, incomeData);
})

