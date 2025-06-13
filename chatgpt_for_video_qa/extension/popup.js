async function getTranscript() {
  // Better extraction can be done with YouTube API, but as a fallback:
  return document.body.innerText.slice(0, 5000);
}

document.getElementById("askBtn").addEventListener("click", async () => {
  const question = document.getElementById("question").value.trim();
  const responseEl = document.getElementById("response");

  if (!question) {
    responseEl.textContent = "Please enter a question.";
    return;
  }

  responseEl.textContent = "Thinking...";

  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    const [{ result: transcript }] = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: getTranscript,
    });

    if (!transcript || transcript.trim().length < 20) {
      responseEl.textContent = "Transcript not found or too short.";
      return;
    }

    const res = await fetch("http://localhost:5003/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, transcript }),
    });

    if (!res.ok) {
      responseEl.textContent = `Server error: ${res.statusText}`;
      return;
    }

    const data = await res.json();

    if (data.answer) {
      responseEl.textContent = data.answer;
    } else {
      responseEl.textContent = data.error || "No response received.";
    }
  } catch (err) {
    responseEl.textContent = "Error: Unable to connect to backend.";
  }
});
