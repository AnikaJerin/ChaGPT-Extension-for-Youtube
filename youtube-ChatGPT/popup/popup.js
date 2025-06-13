document.getElementById("send").addEventListener("click", async () => {
  const question = document.getElementById("question").value.trim();
  if (!question) return;

  try {
    let [tab] = await chrome.tabs.query({active: true, currentWindow: true});
    if (!tab || !tab.url) return;

    let url = new URL(tab.url);
    let videoId = url.searchParams.get("v");

    if (!videoId) return;

    let chatBox = document.getElementById("chat-box");

    // User message first
    let userMsg = document.createElement("div");

    userMsg.classList.add("msg-user");

    userMsg.textContent = question;

    chatBox.appendChild(userMsg);
    chatBox.scrollTop = chatBox.scrollHeight;

    // Now fetch from API
    let response = await fetch("http://localhost:5004/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ videoId, question })
    });

    let data = await response.json();

    let botMsg = document.createElement("div");

    botMsg.classList.add("msg-bot");

    if (response.ok) {
      botMsg.textContent = data.answer;
    } else {
      botMsg.textContent = `Error: ${data.error}`;
    }

    chatBox.appendChild(botMsg);
    chatBox.scrollTop = chatBox.scrollHeight;

    document.getElementById("question").value = '';
  } catch (err) {
    console.error(err);
    let chatBox = document.getElementById("chat-box");

    let botMsg = document.createElement("div");

    botMsg.classList.add("msg-bot");

    botMsg.textContent = `Error: ${err.message}`;

    chatBox.appendChild(botMsg);
    chatBox.scrollTop = chatBox.scrollHeight;
  }
});
