const btn = document.getElementById("check-btn");
const resultBox = document.getElementById("result");
const apiBase = window.API_URL || `${window.location.protocol}//${window.location.hostname}:${window.API_PORT || 8000}`;

function show(message, type) {
  resultBox.textContent = message;
  resultBox.className = `result ${type}`;
}

btn.addEventListener("click", async () => {
  const subject = document.getElementById("subject").value;
  const body = document.getElementById("body").value;

  if (!body.trim()) {
    show("Please enter the email body.", "error");
    return;
  }

  btn.disabled = true;
  btn.textContent = "Checking...";

  try {
    const res = await fetch(`${apiBase}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ subject, body }),
    });
    if (!res.ok) throw new Error(`Server returned ${res.status}`);
    const data = await res.json();
    const pct = (data.confidence * 100).toFixed(1);
    show(
      data.is_spam ? `🚫 Spam (${pct}% confident)` : `✅ Not spam (${pct}% confident)`,
      data.is_spam ? "spam" : "ham"
    );
  } catch (err) {
    show(`Could not reach the API: ${err.message}`, "error");
  } finally {
    btn.disabled = false;
    btn.textContent = "Check email";
  }
});
