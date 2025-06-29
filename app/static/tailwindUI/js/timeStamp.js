// Get all elements with class "time" and "date"
const timeElements = document.getElementsByClassName("time");
const dateElements = document.getElementsByClassName("date");

// Function to format and display the time from a UNIX timestamp
function formatTimeElement(element) {
  // Extract UNIX timestamp from the element's innerText
  let unixTimeStamp = element.innerText;

  // Convert UNIX timestamp to a JavaScript Date object
  let dateObject = new Date(unixTimeStamp * 1000);

  // Extract hours and minutes, ensuring leading zeros if needed
  let hours = "0" + dateObject.getHours();
  let minutes = "0" + dateObject.getMinutes();

  // Create formatted time string (HH:MM)
  let timeElement = hours.substr(-2) + ":" + minutes.substr(-2);

  // Update the element's content with the formatted time
  element.innerHTML = timeElement;
}

// Function to format and display the date from a UNIX timestamp
function formatDateElement(element) {
  // Extract UNIX timestamp from the element's innerText
  let unixTimeStamp = element.innerText;

  // Convert UNIX timestamp to a JavaScript Date object
  let dateObject = new Date(unixTimeStamp * 1000);

  // Extract day, month, and year, ensuring leading zeros if needed
  let day = "0" + dateObject.getDate();
  let month = "0" + (dateObject.getMonth() + 1);
  let year = dateObject.getFullYear().toString();

  // Create formatted date string (DD.MM.YY)
  let dateElement =
    day.substr(-2) + "." + month.substr(-2) + "." + year.slice(-2);

  // Update the element's content with the formatted date
  element.innerHTML = dateElement;
}

// Loop through each element with class "time" and format the time
for (element of timeElements) {
  formatTimeElement(element);
}

// Loop through each element with class "date" and format the date
for (element of dateElements) {
  formatDateElement(element);
}
