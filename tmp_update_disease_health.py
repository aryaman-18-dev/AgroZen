from pathlib import Path
p=Path('disease.js')
s=p.read_text(encoding='utf-8')
# Carry uncertain state to the card via data flag, so users can explicitly label images they have inspected.
s=s.replace('''      alternatives,
      info: diseaseInfo,
    };''','''      alternatives,
      uncertain,
      info: diseaseInfo,
    };''',1)
s=s.replace('''        ${safeSeverity === "unknown" && Array.isArray(result.alternatives) ? `<div class="description"><strong>Other model matches (also unconfirmed):</strong> ${result.alternatives.slice(0, 3).map((item) => `${escapeHtml(getDiseaseInfo(item.class_name).name)} ${escapeHtml(item.confidence)}%`).join(" · ")}</div>` : ""}
    </div>''','''        ${result.uncertain && Array.isArray(result.alternatives) ? `<div class="description"><strong>Other model matches (also unconfirmed):</strong> ${result.alternatives.slice(0, 3).map((item) => `${escapeHtml(getDiseaseInfo(item.class_name).name)} ${escapeHtml(item.confidence)}%`).join(" · ")}</div><button type="button" class="mark-healthy-btn" id="markHealthyBtn">I checked this leaf — mark it healthy</button>` : ""}
    </div>''')
s=s.replace('''  savePredictionRecord(result, currentPreviewDataUrl);

  // Show action buttons bar''','''  savePredictionRecord(result, currentPreviewDataUrl);
  const markHealthyBtn = document.getElementById("markHealthyBtn");
  if (markHealthyBtn) markHealthyBtn.addEventListener("click", markCurrentImageHealthy);

  // Show action buttons bar''')
# Adjust severity message to distinguish health label from a severity estimate.
s=s.replace('''  const severityEmoji = {
    low: "✅",
    medium: "⚠️",
    high: "🚨",
  };

  resultsDiv.innerHTML = `''','''  const severityEmoji = {
    low: "✅",
    medium: "⚠️",
    high: "🚨",
  };
  const isHealthy = /___healthy$/i.test(disease);
  const severityDisplay = safeSeverity === "unknown" || isHealthy
    ? "Plant disease severity: Not assessed"
    : `Typical disease impact: ${safeSeverity.charAt(0).toUpperCase() + safeSeverity.slice(1)} (not measured from this photo)`;

  resultsDiv.innerHTML = `''')
s=s.replace('''        ${safeSeverity === "unknown" ? `<div class="severity">Plant disease severity: Not assessed</div>` : `<div class="severity ${safeSeverity}">Typical disease impact: ${safeSeverity.charAt(0).toUpperCase() + safeSeverity.slice(1)} (not measured from this photo)</div>`}''','''        <div class="severity ${isHealthy || safeSeverity === "unknown" ? "" : safeSeverity}">${escapeHtml(severityDisplay)}</div>''')
# Add handler before Modal functionality
marker='// Modal functionality\n'
handler='''function markCurrentImageHealthy() {
  if (!currentPredictionRecord) return;

  const reviewedInfo = {
    name: "Healthy leaf (user confirmed)",
    severity: "unknown",
    description: "You reviewed this image and marked the leaf as healthy. This is your visual label; the model did not confirm it.",
    treatment: "No disease treatment is indicated by your review. Continue routine monitoring and seek local advice if symptoms appear.",
  };
  currentPredictionRecord.diseaseKey = `${currentPredictionRecord.crop.replace(/ /g, "_")}___healthy`;
  currentPredictionRecord.name = reviewedInfo.name;
  currentPredictionRecord.severity = "unknown";
  currentPredictionRecord.description = reviewedInfo.description;
  currentPredictionRecord.treatment = reviewedInfo.treatment;
  currentPredictionRecord.userReviewedHealth = true;

  try {
    const history = getPredictionHistory().map((item) =>
      item.id === currentPredictionRecord.id ? currentPredictionRecord : item
    );
    localStorage.setItem(HISTORY_STORAGE_KEY, JSON.stringify(history));
  } catch (error) {
    console.warn("Could not update prediction history:", error);
  }

  const title = resultsDiv.querySelector(".disease-name");
  const severity = resultsDiv.querySelector(".severity");
  const description = resultsDiv.querySelector(".description");
  const treatment = resultsDiv.querySelector(".treatment p");
  if (title) title.textContent = `✅ ${reviewedInfo.name}`;
  if (severity) severity.textContent = "Plant disease severity: Not assessed";
  if (description) description.textContent = reviewedInfo.description;
  if (treatment) treatment.textContent = reviewedInfo.treatment;
  document.getElementById("markHealthyBtn")?.remove();
  updateHistoryUI();
}

'''
if marker not in s: raise SystemExit('modal marker missing')
s=s.replace(marker,handler+marker,1)
p.write_text(s,encoding='utf-8')
# Version the page script so browsers do not keep serving the old diagnosis UI.
h=Path('disease.html'); html=h.read_text(encoding='utf-8'); html=html.replace('<script src="disease.js"></script>','<script src="disease.js?v=20261107-healthy-review"></script>'); h.write_text(html,encoding='utf-8')
