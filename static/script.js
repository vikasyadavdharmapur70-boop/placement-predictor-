// Form submit hone par ye function chalega
document.getElementById("predictForm").addEventListener("submit", async function (e) {
  e.preventDefault(); // page reload hone se roko

  // Form ki saari values ek object me lo
  const data = {
    tenth_percent: document.getElementById("tenth_percent").value,
    twelfth_percent: document.getElementById("twelfth_percent").value,
    cgpa: document.getElementById("cgpa").value,
    internships: document.getElementById("internships").value,
    projects: document.getElementById("projects").value,
    aptitude_score: document.getElementById("aptitude_score").value,
    communication_score: document.getElementById("communication_score").value,
    work_experience: document.getElementById("work_experience").value,
  };

  const btn = document.getElementById("submitBtn");
  const resultBox = document.getElementById("result");
  const errorBox = document.getElementById("error");

  btn.disabled = true;
  btn.textContent = "Ruko... ⏳";
  resultBox.classList.add("hidden");
  errorBox.classList.add("hidden");

  try {
    // Flask app ko data bhejo
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (!response.ok || !result.prediction) {
      throw new Error(result.message || "Kuch galat ho gaya!");
    }

    // Result dikhao
    document.getElementById("predictionText").textContent = result.prediction;
    document.getElementById("probText").textContent = result.probability + "% chance";
    document.getElementById("messageText").textContent = result.message;

    resultBox.classList.remove("placed", "not-placed");
    resultBox.classList.add(result.probability >= 50 ? "placed" : "not-placed");
    resultBox.classList.remove("hidden");
  } catch (err) {
    // Error dikhao
    errorBox.textContent = "❌ " + err.message;
    errorBox.classList.remove("hidden");
  } finally {
    btn.disabled = false;
    btn.textContent = "Predict Karo 🔮";
  }
});
