(async function () {

    async function load_data_table(name) {
        const res = await fetch(`./data/data-table-${name}.json`)
        return res.json();
    }

    const data_inflation = await load_data_table('61111-0002');
    const data_wages = await load_data_table('62221-0002');

    const inflation = {
        label: 'Inflation zum Vorjahr',
        data: data_inflation.map(row => ({x: row[0], y: row[2]})),
        yAxisID: 'y1'
    };

    const prices = {
        label: 'Verbraucherpreisindex',
        data: data_inflation.map(row => ({x: row[0], y: row[1]})),
        yAxisID: 'y2'
    };

    const wages = {
        label: 'Löhne (Gesamtwirtchaft)',
        data: data_wages.filter(row => row[3] == 'Gesamtwirtschaft').map(row => ({x: row[0], y: row[1]})),
        yAxisID: 'y2'
    };

    const real_wages = {
        label: 'Reallöhne (Gesamtwirtschaft)',
        data: data_wages.filter(row => row[3] == 'Gesamtwirtschaft').map(row => ({x: row[0], y: 100 * row[1] / data_inflation.find(el => el[0] == row[0])[1]})),
        yAxisID: 'y2'
    };

    const options = {
        elements: {
            point: {
                pointStyle: false
            }
        },
        interaction: {
            mode: 'nearest',
            intersect: false
        },
        plugins: {
            colors: {
                forceOverride: true
            }
        },
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'year',
                    tooltipFormat: 'MMM YYYY'
                },
                min: '2010-04-01T00:00:00Z',
                grid: {
                    display: false
                },
                ticks: {
                    stepSize: 1
                }
            },
            y1: {
                position: 'left'
            },
            y2: {
                position: 'right',
                grid: {
                    display: false
                }
            },
            y3: {
                display: false
            },
            y4: {
                display: false
            },
            y5: {
                display: false
            }
        }
    };

    const plugin = {
        beforeInit(chart) {
            // Get a reference to the original fit function
            const origFit = chart.legend.fit;
            chart.legend.fit = function fit() {
                origFit.bind(chart.legend)();
                // Change the height to any desired value
                this.height += 20;
            }
        }
    }

    function chart(id, datasets) {
        new Chart(
            document.getElementById(id),
            {
                type: 'line',
                data: {
                    datasets: datasets
                },
                options: options,
                plugins: [plugin]
            }
        );
    }

    chart('chart01', [prices, inflation]);
    chart('chart02', [prices, wages, real_wages]);
})();