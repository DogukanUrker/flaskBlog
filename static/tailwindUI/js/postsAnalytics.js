//  Apex charts cdn js link for rendering charts starts here 
window.Promise ||
    document.write(
        '<script src="https://cdn.jsdelivr.net/npm/promise-polyfill@8/dist/polyfill.min.js"><\/script>'
    )
window.Promise ||
    document.write(
        '<script src="https://cdn.jsdelivr.net/npm/eligrey-classlist-js-polyfill@1.2.20171210/classList.min.js"><\/script>'
    )
window.Promise ||
    document.write(
        '<script src="https://cdn.jsdelivr.net/npm/findindex_polyfill_mdn"><\/script>'
    )

// Apex charts cdn js link for rendering charts ends here 


// LineChart code starts here
// Initialize variable for line charts
// lineChart
var lineChart;
// api endpoint url for fetching graph data on button events
let postAnalyticsDataTrafficGraphUrl = "/api/v1/postTrafficGraphData?postID=" + postID + "&";  // pass postID
// Get lineChart's spinner div id
let lineChartSpinner = document.getElementById("lineChartSpinner");
lineChartSpinner.classList.remove("hidden"); // Show spinner when page is loading
// Get lineChartError div id
let lineChartErrorContainer = document.getElementById("lineChartErrorContainer")

// Load dropdown menu duration range selector
function startDropDownMenu() {
    document.getElementById("durationRangeTab").addEventListener("change", durationRangeCallback, false);
}

window.addEventListener("load", startDropDownMenu, false);

// DurationRangeMap
let durationRangeMap = {
    sincePosted : "sincePosted=True",
    last1m: "weeks=4",
    last7d: "days=7",
    last24h: "hours=24",
    last48: "hours=48"
}

// Function to fetch traffic data for mobile screens
function durationRangeCallback() {
    // Get the selected option
    let selectedDurationRange = document.getElementById("durationRangeTab").value;
    // Get dropDownMenu spinner id
    let dropDownMenuSpinner = document.getElementById("dropDownMenuSpinner");

    // Match the currently selected duration
    // Call function for new duration range data
    onTabDurationSelection(durationRangeMap[selectedDurationRange], dropDownMenuSpinner);
}

// Initial tab id
let initialStateTabId = "last48h";
// Function to check active tab and update inactive and call fetch data
function changeTabState(tabID) {
    document.getElementById(initialStateTabId).classList.remove("bg-rose-500/75", "text-black"); // Remove existing classes
    document.getElementById(initialStateTabId).classList.add("text-gray-500", "hover:text-rose-500/75", "hover:text-gray-700"); // Add classes 
    document.getElementById(tabID).classList.remove("text-gray-500", "hover:text-rose-500/75", "hover:text-gray-700"); // Remove existing classes
    document.getElementById(tabID).classList.add("bg-rose-500/75", "text-black"); // Add classes 

    // Update the initial tabs to current selected tab
    initialStateTabId = tabID;

    // Spinner id to activate and deactivate circle animation
    let spinnerID = document.getElementById(tabID + 1); // Match spinner ID with associated tab button

    // Check which buttons are pressed and fetch data accordingly

    // Match the currently selected duration
    // Call function for new duration range data
    onTabDurationSelection(durationRangeMap[tabID], spinnerID);
}

// Common function for both duration dropdown and duration tab
async function onTabDurationSelection(durationRangeQuery, spinnerID) {
    spinnerID.classList.remove("hidden"); // Show tab button's spinner 

    refreshedLineGraphData = await fetchTrafficGraphData(durationRangeQuery)
    if (refreshedLineGraphData) {
        spinnerID.classList.add("hidden"); // Hide tab button's spinner

        // Call update method
        lineChart.updateSeries([{
            data: refreshedLineGraphData
        }])
    }
    else {
        lineChartErrorContainer.classList.remove("hidden") // Show Graph Error message
        spinnerID.classList.add("hidden"); // Hide tab button's spinner
    }
}

// Call function for new duration range data
async function fetchTrafficGraphData(durationRangeQuery) {

    try {
        // Fetch data
        let response = await fetch(postAnalyticsDataTrafficGraphUrl + durationRangeQuery);
        // Parse data into json
        let responseData = await response.json();

        // Check response status
        if (response.ok) {
            // Return data
            return responseData.payload;
        } else {
            // Print error on console
            console.error(responseData.message);
            // Return null
            return null;
        }
    } catch (error) {
        // Print error on console
        console.error(error);
        // Return null
        return null;
    }
}

// Function to line graph when page loads
async function loadLineChart(durationRangeQuery) {
    lineChartSpinner.classList.remove("hidden"); // Show line chart graph spinner

    // Call fetchTrafficGraphData method
    let lineGraphData = await fetchTrafficGraphData(durationRangeQuery);
    if (lineGraphData) {
        // Hide line chart graph spinner
        lineChartSpinner.classList.add("hidden");

        // Line Graph 
        var options = {
            series: [{
                name: visitorCounts, // 'Visitor Counts'
                data: lineGraphData
            }],
            chart: {
                type: 'area',
                stacked: false,
                height: 350,
                zoom: {
                    type: 'x',
                    enabled: true,
                    autoScaleYaxis: true
                },
                toolbar: {
                    autoSelected: 'zoom'
                }
            },
            dataLabels: {
                enabled: false
            },
            markers: {
                size: 0,
            },
            title: {
                text: traffic, // 'Traffic'
                align: 'left'
            },
            fill: {
                type: 'gradient',
                gradient: {
                    shadeIntensity: 1,
                    inverseColors: false,
                    opacityFrom: 0.5,
                    opacityTo: 0,
                    stops: [0, 90, 100]
                },
            },
            yaxis: {
                labels: {
                    formatter: function (val) {
                        // Convert to millions with 2 decimal places
                        // Keep whole numbers for smaller values
                        return val >= 1000000 ? (val / 1000000).toFixed(2) + "M" : val.toFixed(0);
                    },
                },
                title: {
                    text: 'Visits'
                },
            },
            xaxis: {
                type: 'datetime'
            },
            tooltip: {
                shared: false,
                y: {
                    formatter: function (val) {
                        // Convert to millions with 2 decimal places
                        // Keep whole numbers for smaller values
                        return val >= 1000000 ? (val / 1000000).toFixed(2) + "M" : val.toFixed(0);
                    }
                }
            },
            colors: ['#f43f5e'],
            theme: {
                mode: "light" // todo: implement dark and light mode adjust dynamically
            }
        };

        // Render Line Graph
        lineChart = new ApexCharts(document.querySelector("#lineChart"), options);
        lineChart.render();
    } else {
        //Show Graph Error message
        lineChartErrorContainer.classList.remove("hidden");
    }
}

// Load LineChart when page loads
loadLineChart("hours=48")
// Line Chart code ends here


// PieChart code starts here
var options = {
    series: osGraphData["osCountList"], // visitor's computer os count
    chart: {
        width: 380,
        type: 'pie',
    },
    labels: osGraphData["osNameList"], // visitor's computers os
    responsive: [{
        breakpoint: 480,
        options: {
            chart: {
                width: 200
            },
            legend: {
                position: 'bottom'
            }
        }
    }],
    theme: {
        palette: 'palette6' // upto palette10
    }
};

var pieChart = new ApexCharts(document.querySelector("#pieChart"), options);
pieChart.render();
// PieChart code ends here


// BarChar code starts here

// Initialize  variables
// barChart
let barChart;
// api endpoint url for fetching graph data on button events
let postAnalyticsDataCountryGraphUrl = "/api/v1/postCountryGraphData?postID=" + postID + "&"; // pass postID

// Get barChart's spinner div id
let barChartSpinner = document.getElementById("barChartSpinner");
barChartSpinner.classList.remove("hidden") // Show spinner when page is loading
// Get button's spinner div id
let viewAllSpinner = document.getElementById("viewAllSpinner");
// Get barChartError div id
let barChartErrorContainer = document.getElementById("barChartErrorContainer")

// Function for to fetch country graph data
async function fetchCountryGraphData(dataLimit) {
    try {
        // Fetch data 
        let response = await fetch(postAnalyticsDataCountryGraphUrl + dataLimit);
        // Convert response into json
        let responseData = await response.json();
        // Check response status
        if (response.ok) {
            // Return fetch data
            return responseData.payload;
        } else {
            console.error(responseData.message)
            // Return null
            return null;
        }
    } catch (error) {
        console.error(error);
        // Return null
        return null;
    }
}

// Load barChart when page loads
async function loadBarChart(dataLimit) {
    // Fetch graph data
    const countryGraphData = await fetchCountryGraphData(dataLimit);
    let lengthOfCountryList = countryGraphData["countryCountList"].length

    // Calculate line graph height
    let _height = 110
    if(lengthOfCountryList>50){
        _height = lengthOfCountryList*28;
    }else if(lengthOfCountryList>20){
        _height = lengthOfCountryList*32;
    }else if(lengthOfCountryList>15){
        _height = lengthOfCountryList*35;
    }else if(lengthOfCountryList>10){
        _height = lengthOfCountryList*40;
    }else if(lengthOfCountryList>5){
        _height = lengthOfCountryList* 50;
    }else if(lengthOfCountryList>=2){
            _height = lengthOfCountryList * 60;
    }
    
    if (countryGraphData) {
        //  // Hide Bar Chart spinner
        barChartSpinner.classList.add("hidden");

        // BarChart 
        var options = {
            series: [{
                name: visitor, // 'Visitor'
                data: countryGraphData["countryCountList"] // e.g. data: [400, 430, 448, 470, 540, 580, 690, 1100, 1200, 1380]
            }],
            chart: {
                type: 'bar',
                height: _height
            },
            plotOptions: {
                bar: {
                    borderRadius: 4,
                    borderRadiusApplication: 'end',
                    horizontal: true,
                }
            },
            dataLabels: {
                enabled: false
            },
            xaxis: {
                categories: countryGraphData["countryNameList"] // e.g. categories: ['South Korea', 'Canada', 'United Kingdom', 'Netherlands', 'Italy', 'France', 'Japan','United States', 'China', 'Germany']
            },
            theme: {
                mode: "light", // todo: implement dark and light mode adjust dynamically
                palette: 'palette7' // upto palette10
            }
        };
        
        // Render Bar Charts
        barChart = new ApexCharts(document.querySelector("#barChart"), options);
        barChart.render();
    } else {
        // Hide Bar Chart spinner
        barChartSpinner.classList.add("hidden");
        // Show Bar Chart Error message 
        barChartErrorContainer.classList.remove("hidden")
    }
}

// onViewAllClick button function
async function onViewAllClick() {
    viewAllSpinner.classList.remove("hidden"); // Show button's spinner
    // Fetch all data
    let refreshedCountryData = await fetchCountryGraphData("viewAll=True");

    // Update Bar Chart
    if (refreshedCountryData) {
        viewAllSpinner.classList.add("hidden") // Hide spinner
        document.getElementById("viewAll").classList.add("hidden") // Hide button after data is fetch successfully

        // Update Bar Chart
        barChart.updateOptions({
            series: [{
                name: visitor, // 'Visitor'
                data: refreshedCountryData["countryCountList"],
            }],
            xaxis: {
                categories: refreshedCountryData["countryNameList"],
            },
        })
    } else {
        viewAllSpinner.classList.add("hidden"); // Hide button's spinner
        // Show Error message
        barChartErrorContainer.classList.remove("hidden")
    }
}

// Call the function when page loads and pass empty string
loadBarChart("viewAll=False")