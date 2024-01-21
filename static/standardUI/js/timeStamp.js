// Get all elements with class "time" and "date"
const timeElements = document.getElementsByClassName("time");
const dateElement = document.getElementsByClassName("date");

// Function to format and display the time from a UNIX timestamp
function formatTimeTimeStamp(element) {
  // Extract UNIX timestamp from the element's innerHTML
  let unixTimeTimeStamp = element.innerHTML;

  // Convert UNIX timestamp to a JavaScript Date object
  let dateTimeTimeStamp = new Date(unixTimeTimeStamp * 1000);

  // Extract hours and minutes, ensuring leading zeros if needed
  let hoursTimeTimeStamp = "0" + dateTimeTimeStamp.getHours();
  let minutesTimeTimeStamp = "0" + dateTimeTimeStamp.getMinutes();

  // Create formatted time string (HH:MM)
  let formattedTimeTimeStamp =
    hoursTimeTimeStamp.substr(-2) + ":" + minutesTimeTimeStamp.substr(-2);

  // Update the element's content with the formatted time
  element.innerHTML = formattedTimeTimeStamp;
}

// Function to format and display the date from a UNIX timestamp
function formatdateElement(element) {
  // Extract UNIX timestamp from the element's innerHTML
  let unixdateElement = element.innerHTML;

  // Convert UNIX timestamp to a JavaScript Date object
  let datedateElement = new Date(unixdateElement * 1000);

  // Extract day, month, and year, ensuring leading zeros if needed
  let day = "0" + datedateElement.getDate();
  let month = "0" + (datedateElement.getMonth() + 1);
  let year = datedateElement.getFullYear().toString();

  // Create formatted date string (DD.MM.YY)
  let formatteddateElement =
    day.substr(-2) + "." + month.substr(-2) + "." + year.slice(-2);

  // Update the element's content with the formatted date
  element.innerHTML = formatteddateElement;
}

// Loop through each element with class "time" and format the time
for (element of timeElements) {
  formatTimeTimeStamp(element);
}

// Loop through each element with class "date" and format the date
for (element of dateElement) {
  formatdateElement(element);
}
