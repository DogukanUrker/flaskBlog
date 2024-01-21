/**
 * @param {string} token The reCAPTCHA token.
 * @description This function is called when the reCAPTCHA form is submitted.
 */
function onSubmit(token) {
  document.getElementById("recaptchaForm").submit();
}
