// Main JS logic
const notificationCloseButtons = document.querySelectorAll("[data-notification-close]");
const modalCloseButtons = document.querySelectorAll("[data-modal-close]");

modalCloseButtons.forEach((button) => {
  button.addEventListener("click", (event) => {
    const dialog = event.target.closest("dialog");
    if (dialog) {
      dialog.close();
    }
  });
});

notificationCloseButtons.forEach((button) => {
  button.addEventListener("click", (event) => {
    const notification = event.target.closest("[data-component='notification']");
    if (notification) {
      notification.hidden = true;
    }
  });
});
