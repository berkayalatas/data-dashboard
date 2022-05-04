const getExpenseData = () => {
    fetch('/expense_category_summary').then((res) => res.json()).then((result) => {
        //console.log('expense', result);
        const category_data = result.expense_category_data
        const [expenseLabels, expenseData] = [Object.keys(category_data), Object.values(category_data)]
        console.log(expenseData, expenseLabels)
    })
    return expenseData
}

const getIncomeData = () => {
    fetch('/income/income_source_summary').then((res) => res.json()).then((result) => {
        //console.log('income', result);
        const category_data = result.income_source_data
        const [incomeLabels, incomeData] = [Object.keys(category_data), Object.values(category_data)]
        console.log(incomeData, incomeLabels)
    })
}

getIncomeData();
getExpenseData();
