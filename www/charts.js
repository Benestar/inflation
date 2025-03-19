(async function () {
    const res = await fetch("./data/data-table-61111-0002.json")
    const data = await res.json();

    new Chart(
        document.getElementById('chart'),
        {
            type: 'line',
            data: {
                labels: data.map(row => row.label),
                datasets: [
                    {
                        label: 'Inflation zum Vorjahr',
                        data: data.map(row => row.prev_year),
                        yAxisID: 'y1'
                    },
                    {
                        label: 'Verbraucherpreisindex',
                        data: data.map(row => row.price),
                        yAxisID: 'y2'
                    }
                ]
            },
            options: {
                scales: {
                    y1: {
                        position: 'left'
                    },
                    y2: {
                        position: 'right',
                        grid: {
                            drawOnChartArea: false
                        }
                    }
                }
            }
        }
    );
})();