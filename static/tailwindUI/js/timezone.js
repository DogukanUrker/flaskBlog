/**
 * sets the user's timezone in local storage
 * @param {string} timezone - the user's timezone
 */
const setTimezone = (timezone) => {
  localStorage.setItem("timezone", timezone);
};

/**
 * gets the user's timezone from local storage
 * @returns {string} the user's timezone
 */
const getTimezone = () => {
  return localStorage.getItem("timezone");
};

// set the user's timezone on page load
setTimezone(Intl.DateTimeFormat().resolvedOptions().timeZone);
