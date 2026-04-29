const form = document.getElementById("projection-form");
const output = document.getElementById("output");
const submitButton = document.getElementById("submit-btn");
const modal = document.getElementById("example-modal");
const modalOpenButton = document.getElementById("open-modal-button");
const notificationCloseButtons = document.querySelectorAll("[data-notification-close]");
const modalCloseButtons = document.querySelectorAll("[data-modal-close]");

if (form && output && submitButton) {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const payload = {
      away_team: form.away_team?.value?.trim() ?? "",
      home_team: form.home_team?.value?.trim() ?? "",
    };

    submitButton.disabled = true;
    output.textContent = "Loading projection...";

    try {
      const response = await fetch("/projection", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const rawBody = await response.text();
      let body = {};
      if (rawBody) {
        try {
          body = JSON.parse(rawBody);
        } catch (_ignored) {
          body = { error: rawBody };
        }
      }

      if (!response.ok) {
        output.textContent = body.error || "Request failed.";
        return;
      }

      output.textContent = JSON.stringify(body, null, 2);
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unknown error";
      output.textContent = `Network error: ${message}`;
    } finally {
      submitButton.disabled = false;
    }
  });
}

if (modal && modalOpenButton) {
  modalOpenButton.addEventListener("click", () => {
    modal.showModal();
  });
}

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
