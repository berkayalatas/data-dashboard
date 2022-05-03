const renderChart = (chartData, chartLabel) => {
    // const labels = [
    //     'Red',
    //     'Blue',
    //     'Yellow'
    // ];

    const data = {
        labels: chartLabel,
        datasets: [{
            label: 'My First Dataset',
            data: chartData,
            backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 205, 86)'
            ],
            hoverOffset: 4
        }]
    };

    const config = {
        type: 'pie',
        data: data,
    };

    const myChart = new Chart(
        document.getElementById('myChart'),
        config
    );
}

const getChartData = () => {
    fetch('/expense_category_summary').then((res) => res.json()).then((result) => {
        console.log(result);
        const category_data = result.expense_category_data
        const [labels, data] = [Object.keys(category_data), Object.values(category_data), ]
        console.log(data, labels)
        renderChart(data, labels)
    })
}

document.onload = getChartData();