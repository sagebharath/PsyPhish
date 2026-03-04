async function analyzeURL() {
  const url = document.getElementById("urlInput").value;
  const resultDiv = document.getElementById("result");
  const progressDiv = document.getElementById("progress");

  if (!url) {
    alert("Please enter a URL");
    return;
  }

  resultDiv.innerHTML = "";
  progressDiv.classList.remove("hidden");

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url }),
    });

    const data = await response.json();
    progressDiv.classList.add("hidden");

    let statusClass = data.status.toLowerCase();

    resultDiv.innerHTML = `
            <div class="result-card ${statusClass}">
                <h3>${data.status}</h3>
                <p><strong>Risk Score:</strong> ${data.risk_score}%</p>
                <p><strong>Reasons:</strong></p>
                <ul>
                    ${data.reasons.map((r) => `<li>${r}</li>`).join("")}
                </ul>
            </div>
        `;
  } catch (err) {
    progressDiv.classList.add("hidden");
    resultDiv.innerHTML = "<p>Error analyzing the website.</p>";
  }
}
