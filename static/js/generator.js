const form = document.getElementById("blog-form");
const loading = document.getElementById("loading");
const errorBox = document.getElementById("error-box");
const result = document.getElementById("result");
const compareResult = document.getElementById("compare-result");
const generateBtn = document.getElementById("generate-btn");
const saveBtn = document.getElementById("save-btn");
const saveStatus = document.getElementById("save-status");

let lastGeneratedPost = null;
let lastGroqPost = null;
let lastGeminiPost = null;

form.addEventListener("submit", async function (e) {
  e.preventDefault();

  const topic = document.getElementById("topic").value;
  const provider = document.getElementById("provider").value;

  errorBox.classList.add("hidden");
  result.classList.add("hidden");
  compareResult.classList.add("hidden");
  saveBtn.classList.add("hidden");
  saveStatus.innerText = "";
  document.getElementById("save-groq-btn").classList.add("hidden");
  document.getElementById("save-gemini-btn").classList.add("hidden");
  document.getElementById("save-groq-status").innerText = "";
  document.getElementById("save-gemini-status").innerText = "";
  loading.classList.remove("hidden");
  generateBtn.disabled = true;

  try {
    if (provider === "compare") {
      const response = await fetch("/compare_blog", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: topic })
      });

      const data = await response.json();
      loading.classList.add("hidden");
      generateBtn.disabled = false;

      if (data.success) {
        const groq = data.results.groq;
        const gemini = data.results.gemini;

        document.getElementById("groq-output").innerText = groq.success
          ? `${groq.data.title}\n\n${groq.data.body_markdown}`
          : "Error: " + groq.error;

        document.getElementById("gemini-output").innerText = gemini.success
          ? `${gemini.data.title}\n\n${gemini.data.body_markdown}`
          : "Error: " + gemini.error;

        if (groq.success) {
          lastGroqPost = { ...groq.data, provider: "groq" };
          document.getElementById("save-groq-btn").classList.remove("hidden");
        }
        if (gemini.success) {
          lastGeminiPost = { ...gemini.data, provider: "gemini" };
          document.getElementById("save-gemini-btn").classList.remove("hidden");
        }

        compareResult.classList.remove("hidden");
      } else {
        errorBox.innerText = "Error: " + data.error;
        errorBox.classList.remove("hidden");
      }

    } else {
      const response = await fetch("/generate_blog", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: topic, provider: provider })
      });

      const data = await response.json();
      loading.classList.add("hidden");
      generateBtn.disabled = false;

      if (data.success) {
        document.getElementById("result-title").innerText = data.title;
        document.getElementById("result-meta").innerText = data.meta_description;
        document.getElementById("result-tags").innerText = "Tags: " + data.tags.join(", ");
        document.getElementById("result-body").innerText = data.body_markdown;
        result.classList.remove("hidden");

        lastGeneratedPost = data;
        saveBtn.classList.remove("hidden");

      } else {
        errorBox.innerText = "Error: " + (data.error || "Something went wrong.");
        errorBox.classList.remove("hidden");
      }
    }

  } catch (err) {
    loading.classList.add("hidden");
    generateBtn.disabled = false;
    errorBox.innerText = "Network error: " + err.message;
    errorBox.classList.remove("hidden");
  }
});

saveBtn.addEventListener("click", async function () {
  if (!lastGeneratedPost) return;
  saveStatus.innerText = "Saving...";

  try {
    const response = await fetch("/save_post", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(lastGeneratedPost)
    });
    const data = await response.json();
    saveStatus.innerText = data.success ? "✅ Saved!" : "❌ Failed to save";
  } catch (err) {
    saveStatus.innerText = "❌ Network error";
  }
});

document.getElementById("save-groq-btn").addEventListener("click", async function () {
  if (!lastGroqPost) return;
  const statusEl = document.getElementById("save-groq-status");
  statusEl.innerText = "Saving...";

  try {
    const response = await fetch("/save_post", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(lastGroqPost)
    });
    const data = await response.json();
    statusEl.innerText = data.success ? "✅ Saved!" : "❌ Failed";
  } catch (err) {
    statusEl.innerText = "❌ Network error";
  }
});

document.getElementById("save-gemini-btn").addEventListener("click", async function () {
  if (!lastGeminiPost) return;
  const statusEl = document.getElementById("save-gemini-status");
  statusEl.innerText = "Saving...";

  try {
    const response = await fetch("/save_post", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(lastGeminiPost)
    });
    const data = await response.json();
    statusEl.innerText = data.success ? "✅ Saved!" : "❌ Failed";
  } catch (err) {
    statusEl.innerText = "❌ Network error";
  }
});