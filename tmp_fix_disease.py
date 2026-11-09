from pathlib import Path
p=Path('disease.js')
s=p.read_text(encoding='utf-8')
old='''    const confidence = Number(prediction.confidence) || 0;
    const diseaseInfo = confidence < 40
      ? {
          name: "Low-confidence result",
          severity: "low",
          description: `The model’s closest match was ${getDiseaseInfo(diseaseKey).name}, but the score is low. Retake a clear photo of one leaf and try again.`,
          treatment: "Do not treat based on this result. Compare symptoms with a local agricultural expert.",
        }
      : getDiseaseInfo(diseaseKey);
    const result = {
      disease: confidence < 40 ? "Unknown___Uncertain" : diseaseKey,
      confidence,
      info: diseaseInfo,
    };'''
new='''    const confidence = Number(prediction.confidence) || 0;
    const alternatives = Array.isArray(prediction.alternatives) ? prediction.alternatives : [];
    const runnerUp = alternatives.find((item) => item.class_name !== diseaseKey);
    const margin = runnerUp ? confidence - Number(runnerUp.confidence || 0) : confidence;
    // Softmax scores are not calibrated probabilities. Use a conservative UI
    // gate so moderate/ambiguous scores are not presented as diagnoses.
    const uncertain = confidence < 70 || margin < 15;
    const candidateInfo = getDiseaseInfo(diseaseKey);
    const diseaseInfo = uncertain
      ? {
          name: "Uncertain result — no diagnosis",
          severity: "unknown",
          description: `The model’s closest match was ${candidateInfo.name} (${confidence.toFixed(1)}% raw model score), but this score is not calibrated and is not enough to identify a disease reliably. Take a close, well-lit photo of one leaf showing both healthy and affected areas, then try again.`,
          treatment: "Do not apply pesticides or fungicides based on this result. Compare visible symptoms with a local agricultural expert or extension service.",
        }
      : candidateInfo;
    const result = {
      disease: diseaseKey,
      confidence,
      alternatives,
      info: diseaseInfo,
    };'''
if old not in s: raise SystemExit('target prediction block not found')
s=s.replace(old,new)
s=s.replace('''        <div class="severity ${safeSeverity}">
            Severity: ${safeSeverity.charAt(0).toUpperCase() + safeSeverity.slice(1)}
        </div>''','''        ${safeSeverity === "unknown" ? `<div class="severity">Plant disease severity: Not assessed</div>` : `<div class="severity ${safeSeverity}">Typical disease impact: ${safeSeverity.charAt(0).toUpperCase() + safeSeverity.slice(1)} (not measured from this photo)</div>`}''')
s=s.replace('''        <div class="treatment">
            <h4>🌿 Treatment Recommendations</h4>
            <p>${safeTreatment}</p>
        </div>''','''        <div class="treatment">
            <h4>${safeSeverity === "unknown" ? "🌿 Safe next step" : "🌿 General care guidance"}</h4>
            <p>${safeTreatment}</p>
        </div>
        ${safeSeverity === "unknown" && Array.isArray(result.alternatives) ? `<div class="description"><strong>Other model matches (also unconfirmed):</strong> ${result.alternatives.slice(0, 3).map((item) => `${escapeHtml(getDiseaseInfo(item.class_name).name)} ${escapeHtml(item.confidence)}%`).join(" · ")}</div>` : ""}''')
p.write_text(s,encoding='utf-8')
