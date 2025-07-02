let initialSpendTime = 0;

if (visitorID != null) {
  setInterval(() => {
    initialSpendTime += 5;

    const data = {
      visitorID: visitorID,
      spendTime: initialSpendTime,
    };

    fetch("/api/v1/timeSpendsDuration", {
      method: "POST",
      headers: { "X-CSRFToken": csrfToken, "Content-Type": "application/json" },
      body: JSON.stringify(data),
      keepalive: true,
    });
  }, 5000);
}
