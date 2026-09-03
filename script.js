const greetingButton = document.querySelector("#greeting-button");
const messageElement = document.querySelector("#message");

greetingButton.addEventListener("click", () => {
  messageElement.textContent = "Hello from JavaScript!";
});