const tempChartContainer = document.getElementById('temperatureChartContainer');
const humidityChartContainer = document.getElementById('humidityChartContainer');
const lightLevelChartContainer = document.getElementById('lightLevelChartContainer');

let sensorData1 = [];
let sensorData2 = [];
let sensorData3 = [];

document.addEventListener("DOMContentLoaded", function () {
    initializeCharts();
    setInterval(fetchDataAndUpdateCharts, 5000); // Fetch data every 5 seconds
});

let tempChart, humidityChart, lightLevelChart;

function initializeCharts() {
    // Temperature Chart
    const tempCanvas = document.createElement('canvas');
    tempCanvas.id = 'tempChart';
    tempChartContainer.appendChild(tempCanvas);

    tempChart = new Chart(tempCanvas, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Temperature',
                data: sensorData1,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1,
                fill: false,
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'second'
                    },
                    title: {
                        display: true,
                        text: 'Time'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Temperature (°C)'
                    }
                }
            }
        }
    });

    // Humidity Chart
    const humidityCanvas = document.createElement('canvas');
    humidityCanvas.id = 'humidityChart';
    humidityChartContainer.appendChild(humidityCanvas);

    humidityChart = new Chart(humidityCanvas, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Humidity',
                data: sensorData2,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1,
                fill: false,
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'second'
                    },
                    title: {
                        display: true,
                        text: 'Time'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Humidity (%)'
                    }
                }
            }
        }
    });

    // Light Level Chart
    const lightLevelCanvas = document.createElement('canvas');
    lightLevelCanvas.id = 'lightLevelChart';
    lightLevelChartContainer.appendChild(lightLevelCanvas);

    lightLevelChart = new Chart(lightLevelCanvas, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Light Level',
                data: sensorData3,
                backgroundColor: 'rgba(255, 206, 86, 0.2)',
                borderColor: 'rgba(255, 206, 86, 1)',
                borderWidth: 1,
                fill: false,
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'second'
                    },
                    title: {
                        display: true,
                        text: 'Time'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Light Level (lx)'
                    }
                }
            }
        }
    });
}

async function fetchDataAndUpdateCharts() {
    try {
        const response = await fetch(`/sensor_data`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const json = await response.json();

        // Clear existing data
        sensorData1.length = 0;
        sensorData2.length = 0;
        sensorData3.length = 0;

        // Add new data points to sensorData arrays
        Object.values(json).forEach(entry => {
            let tempValue = entry.temperature;
            let humidValue = entry.humidity;
            let llValue = entry.light_level;
            let timestamp = new Date(entry.timestamp);
            sensorData1.push({ x: timestamp, y: tempValue });
            sensorData2.push({ x: timestamp, y: humidValue });
            sensorData3.push({ x: timestamp, y: llValue });
        });

        // Update charts with new data
        tempChart.update();
        humidityChart.update();
        lightLevelChart.update();

    } catch (error) {
        console.error("Error querying data: ", error);
    }
}