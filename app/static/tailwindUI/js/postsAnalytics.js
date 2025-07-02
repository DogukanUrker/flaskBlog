window.Promise ||
  document.write(
    '<script src="https://cdn.jsdelivr.net/npm/promise-polyfill@8/dist/polyfill.min.js"><\/script>',
  );
window.Promise ||
  document.write(
    '<script src="https://cdn.jsdelivr.net/npm/eligrey-classlist-js-polyfill@1.2.20171210/classList.min.js"><\/script>',
  );
window.Promise ||
  document.write(
    '<script src="https://cdn.jsdelivr.net/npm/findindex_polyfill_mdn"><\/script>',
  );

var lineChart;
let postAnalyticsDataTrafficGraphUrl =
  "/api/v1/postTrafficGraphData?postID=" + postID + "&";
let lineChartSpinner = document.getElementById("lineChartSpinner");
lineChartSpinner.classList.remove("hidden");
let lineChartErrorContainer = document.getElementById(
  "lineChartErrorContainer",
);

function startDropDownMenu() {
  document
    .getElementById("durationRangeTab")
    .addEventListener("change", durationRangeCallback, false);
}

window.addEventListener("load", startDropDownMenu, false);

let durationRangeMap = {
  sincePosted: "sincePosted=True",
  last1m: "weeks=4",
  last7d: "days=7",
  last24h: "hours=24",
  last48: "hours=48",
};

function durationRangeCallback() {
  let selectedDurationRange = document.getElementById("durationRangeTab").value;
  let dropDownMenuSpinner = document.getElementById("dropDownMenuSpinner");

  onTabDurationSelection(
    durationRangeMap[selectedDurationRange],
    dropDownMenuSpinner,
  );
}

let initialStateTabId = "last48h";
function changeTabState(tabID) {
  document
    .getElementById(initialStateTabId)
    .classList.remove("bg-rose-500/75", "text-black");
  document
    .getElementById(initialStateTabId)
    .classList.add(
      "text-gray-500",
      "hover:text-rose-500/75",
      "hover:text-gray-700",
    );
  document
    .getElementById(tabID)
    .classList.remove(
      "text-gray-500",
      "hover:text-rose-500/75",
      "hover:text-gray-700",
    );
  document.getElementById(tabID).classList.add("bg-rose-500/75", "text-black");

  initialStateTabId = tabID;

  let spinnerID = document.getElementById(tabID + 1);

  onTabDurationSelection(durationRangeMap[tabID], spinnerID);
}

async function onTabDurationSelection(durationRangeQuery, spinnerID) {
  spinnerID.classList.remove("hidden");

  refreshedLineGraphData = await fetchTrafficGraphData(durationRangeQuery);
  if (refreshedLineGraphData) {
    spinnerID.classList.add("hidden");

    lineChart.updateSeries([
      {
        data: refreshedLineGraphData,
      },
    ]);
  } else {
    lineChartErrorContainer.classList.remove("hidden");
    spinnerID.classList.add("hidden");
  }
}

async function fetchTrafficGraphData(durationRangeQuery) {
  try {
    let response = await fetch(
      postAnalyticsDataTrafficGraphUrl + durationRangeQuery,
    );
    let responseData = await response.json();

    if (response.ok) {
      return responseData.payload;
    } else {
      console.error(responseData.message);
      return null;
    }
  } catch (error) {
    console.error(error);
    return null;
  }
}

async function loadLineChart(durationRangeQuery) {
  lineChartSpinner.classList.remove("hidden");

  let lineGraphData = await fetchTrafficGraphData(durationRangeQuery);
  if (lineGraphData) {
    lineChartSpinner.classList.add("hidden");

    var options = {
      series: [
        {
          name: visitorCounts,
          data: lineGraphData,
        },
      ],
      chart: {
        type: "area",
        stacked: false,
        height: 350,
        zoom: {
          type: "x",
          enabled: true,
          autoScaleYaxis: true,
        },
        toolbar: {
          autoSelected: "zoom",
        },
      },
      dataLabels: {
        enabled: false,
      },
      markers: {
        size: 0,
      },
      title: {
        text: traffic,
        align: "left",
      },
      fill: {
        type: "gradient",
        gradient: {
          shadeIntensity: 1,
          inverseColors: false,
          opacityFrom: 0.5,
          opacityTo: 0,
          stops: [0, 90, 100],
        },
      },
      yaxis: {
        labels: {
          formatter: function (val) {
            return val >= 1000000
              ? (val / 1000000).toFixed(2) + "M"
              : val.toFixed(0);
          },
        },
        title: {
          text: "Visits",
        },
      },
      xaxis: {
        type: "datetime",
      },
      tooltip: {
        shared: false,
        y: {
          formatter: function (val) {
            return val >= 1000000
              ? (val / 1000000).toFixed(2) + "M"
              : val.toFixed(0);
          },
        },
      },
      colors: ["#f43f5e"],
      theme: {
        mode: "light",
      },
    };

    lineChart = new ApexCharts(document.querySelector("#lineChart"), options);
    lineChart.render();
  } else {
    lineChartErrorContainer.classList.remove("hidden");
  }
}

loadLineChart("hours=48");

var options = {
  series: osGraphData["osCountList"],
  chart: {
    width: 380,
    type: "pie",
  },
  labels: osGraphData["osNameList"],
  responsive: [
    {
      breakpoint: 480,
      options: {
        chart: {
          width: 200,
        },
        legend: {
          position: "bottom",
        },
      },
    },
  ],
  theme: {
    palette: "palette6",
  },
};

var pieChart = new ApexCharts(document.querySelector("#pieChart"), options);
pieChart.render();

let barChart;
let postAnalyticsDataCountryGraphUrl =
  "/api/v1/postCountryGraphData?postID=" + postID + "&";

let barChartSpinner = document.getElementById("barChartSpinner");
barChartSpinner.classList.remove("hidden");
let viewAllSpinner = document.getElementById("viewAllSpinner");
let barChartErrorContainer = document.getElementById("barChartErrorContainer");

async function fetchCountryGraphData(dataLimit) {
  try {
    let response = await fetch(postAnalyticsDataCountryGraphUrl + dataLimit);
    let responseData = await response.json();
    if (response.ok) {
      return responseData.payload;
    } else {
      console.error(responseData.message);
      return null;
    }
  } catch (error) {
    console.error(error);
    return null;
  }
}

async function loadBarChart(dataLimit) {
  const countryGraphData = await fetchCountryGraphData(dataLimit);
  let lengthOfCountryList = countryGraphData["countryCountList"].length;

  let _height = 110;
  if (lengthOfCountryList > 50) {
    _height = lengthOfCountryList * 28;
  } else if (lengthOfCountryList > 20) {
    _height = lengthOfCountryList * 32;
  } else if (lengthOfCountryList > 15) {
    _height = lengthOfCountryList * 35;
  } else if (lengthOfCountryList > 10) {
    _height = lengthOfCountryList * 40;
  } else if (lengthOfCountryList > 5) {
    _height = lengthOfCountryList * 50;
  } else if (lengthOfCountryList >= 2) {
    _height = lengthOfCountryList * 60;
  }

  if (countryGraphData) {
    barChartSpinner.classList.add("hidden");

    var options = {
      series: [
        {
          name: visitor,
          data: countryGraphData["countryCountList"],
        },
      ],
      chart: {
        type: "bar",
        height: _height,
      },
      plotOptions: {
        bar: {
          borderRadius: 4,
          borderRadiusApplication: "end",
          horizontal: true,
        },
      },
      dataLabels: {
        enabled: false,
      },
      xaxis: {
        categories: countryGraphData["countryNameList"],
      },
      theme: {
        mode: "light",
        palette: "palette7",
      },
    };

    barChart = new ApexCharts(document.querySelector("#barChart"), options);
    barChart.render();
  } else {
    barChartSpinner.classList.add("hidden");
    barChartErrorContainer.classList.remove("hidden");
  }
}

async function onViewAllClick() {
  viewAllSpinner.classList.remove("hidden");
  let refreshedCountryData = await fetchCountryGraphData("viewAll=True");

  if (refreshedCountryData) {
    viewAllSpinner.classList.add("hidden");
    document.getElementById("viewAll").classList.add("hidden");

    barChart.updateOptions({
      series: [
        {
          name: visitor,
          data: refreshedCountryData["countryCountList"],
        },
      ],
      xaxis: {
        categories: refreshedCountryData["countryNameList"],
      },
    });
  } else {
    viewAllSpinner.classList.add("hidden");
    barChartErrorContainer.classList.remove("hidden");
  }
}

loadBarChart("viewAll=False");
