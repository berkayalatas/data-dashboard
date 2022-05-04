const renderPieChart = (chartData, chartLabel) => {
    const data = {
        labels: chartLabel,
        datasets: [{
            label: 'Expenses and Categories',
            data: chartData,
            backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 205, 86)',
                'rgba(2,228,43,0.6278886554621849)',
                '#00d4ff'
            ],
            hoverOffset: 4
        }]
    };
    const config = {
        type: 'pie',
        data: data,
    };
    const incomePieChart = new Chart(
        document.getElementById('incomePieChart'),
        config
    );
}

const renderBarChart = (chartData, chartLabel) => {
    const data = {
        labels: chartLabel,
        datasets: [{
            label: 'Expenses and Categories',
            data: chartData,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 205, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(201, 203, 207, 0.2)'
            ],
            borderColor: [
                'rgb(255, 99, 132)',
                'rgb(255, 159, 64)',
                'rgb(255, 205, 86)',
                'rgb(75, 192, 192)',
                'rgb(54, 162, 235)',
                'rgb(153, 102, 255)',
                'rgb(201, 203, 207)'
            ],
            hoverOffset: 4
        }]
    };
    const config = {
        type: 'bar',
        data: data,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        },
    };
    const incomeBarChart = new Chart(
        document.getElementById('incomeBarChart'),
        config
    );
}


const renderLineChart = (chartData, chartLabel) => {
    const data = {
        labels: chartLabel,
        datasets: [{
            label: 'Expenses and Categories',
            data: chartData,
            backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 205, 86)',
                '#e4e202',
                '#02ace4'
            ],
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }]
    };
    const config = {
        type: 'line',
        data: data,
    };
    const incomeLineChart = new Chart(
        document.getElementById('incomeLineChart'),
        config
    );
}


const renderPolarChart = (chartData, chartLabel) => {
    const data = {
        labels: chartLabel,
        datasets: [{
            data: chartData,
            backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(75, 192, 192)',
                'rgb(255, 205, 86)',
                'rgb(201, 203, 207)',
                'rgb(54, 162, 235)'
            ],
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }]
    };
    const config = {
        type: 'polarArea',
        data: data,
        options: {}
    };
    const incomePolarChart = new Chart(
        document.getElementById('incomePolarChart'),
        config
    );
}

const getChartData = () => {
    fetch('/income/income_source_summary').then((res) => res.json()).then((result) => {
        console.log('Result',result);
        const category_data = result.income_source_data
        const [labels, data] = [Object.keys(category_data), Object.values(category_data) ]
        console.log(data, labels)
        renderPieChart(data, labels);
        renderBarChart(data, labels);
        renderLineChart(data, labels);
        renderPolarChart(data, labels);
    })
}

document.onload = getChartData();