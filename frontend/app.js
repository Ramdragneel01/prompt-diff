const baselineEl = document.getElementById("baseline");
const candidateEl = document.getElementById("candidate");
const compareBtn = document.getElementById("compare");
const summaryEl = document.getElementById("summary");
const diffEl = document.getElementById("diff");

compareBtn.addEventListener("click", async () => {
  const baseline = baselineEl.value.trim();
  const candidate = candidateEl.value.trim();
  if (!baseline || !candidate) {
    alert("Provide both baseline and candidate prompts");
    return;
  }

  compareBtn.disabled = true;
  compareBtn.textContent = "Comparing...";

  try {
    const response = await fetch("/v1/diff", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ baseline, candidate })
    });

    if (!response.ok) {
      throw new Error(`Diff request failed: ${response.status}`);
    }

    const data = await response.json();

    summaryEl.textContent = JSON.stringify(
      {
        summary: data.summary,
        risk: data.risk,
        metrics: data.metrics,
        placeholders_added: data.placeholders_added,
        placeholders_removed: data.placeholders_removed
      },
      null,
      2
    );

    diffEl.textContent = data.unified_diff || "(no unified diff)";
  } catch (err) {
    summaryEl.textContent = JSON.stringify({ error: (err && err.message) || "Unknown error" }, null, 2);
    diffEl.textContent = "";
  } finally {
    compareBtn.disabled = false;
    compareBtn.textContent = "Compare";
  }
});
