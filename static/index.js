const queryForm = document.getElementById("queryForm");
const interpolateButton = document.getElementById("interpolateButton");
const chartContainer = document.getElementById('dataChartContainer');
const userID = "A17323782";
var dataChart;

document.addEventListener("DOMContentLoaded", function () {
    queryForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        let sensorData = [];

        const selectedLoc = document.getElementById("location_select").value;         //retrieving form inputs
        const selectedSensor = document.getElementById("sensor_select").value;
        const startTime = new Date(document.getElementById("startTime").value);
        const endTime = new Date(document.getElementById("endTime").value);
        var ylabel = 'Value';
        var chartLabel = 'Sensor Values over Time';

        if (selectedSensor == "temperature"){                       //setting chart labels based on sensor type
            ylabel = "Value (C)";
            chartLabel = 'Temperature Sensor Values over Time';
        }
        if (selectedSensor == "humidity"){
            ylabel = "Value (%)";
            chartLabel = 'Humidity Sensor Values over Time';
        }
        if (selectedSensor == "light"){
            ylabel = "Value (lx)";
            chartLabel = 'Light Sensor Values over Time';
        }
        if (selectedSensor == "pressure"){
            ylabel = "Value (hPa)";
            chartLabel = 'Pressure Sensor Values over Time';
        }

        try {
            const response = await fetch(`https://ece140.frosty-sky-f43d.workers.dev/api/query?auth=${userID}&sensorType=${selectedSensor}`);        //retrives sensor data
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const json = await response.json();
            const responseData = json["results"];

            responseData.forEach(entry => {
                let time = new Date(entry.time);
                let value = entry.value;
                let unit = entry.unit;
                let location = entry.location.replace(/[^a-zA-Z]/g, "").toLowerCase();   //removes all characters that are not letters and converts to lowercase to account for different methods used to represent location name
                if ((time >= startTime) && (time <= endTime) && (location == selectedLoc)){            //filters sensor data based on time and location
                    sensorData.push({x: time.getTime(), y: value}); 
                }
            });

            if (chartContainer.firstChild) {                                             //removes old chart to replace it
                chartContainer.removeChild(chartContainer.firstChild);
            }
            const canvas = document.createElement('canvas');
            canvas.id = 'dataChart';
            chartContainer.appendChild(canvas);

            dataChart = new Chart(document.getElementById('dataChart'), {                //creates a new chart with the filtered sensor data
                type: 'line',
                data: {
                    datasets: [{
                        label: chartLabel,
                        data: sensorData,
                        backgroundColor: 'rgba(0, 60, 120, 0.3)', 
                        fill: false,
                        borderColor: 'rgba(0, 60, 120, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                unit: 'minute'
                            },
                            title: {
                                display: true,
                                text: 'Time'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: ylabel
                            }
                        }
                    }
                }
            });
        } catch (error) {
            console.error("Error querying data: ", error);
        }
    });

    interpolateButton.addEventListener("click", function () {                 //button to switch to interpolate page
        window.location.href = "/interpolate";
    });
});