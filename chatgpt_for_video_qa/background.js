// chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
//   if (msg.action === "getTranscriptAndChat") {
//     // Call backend API with videoId and question
//     fetch("http://localhost:8000/chat", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ videoId: msg.videoId, question: msg.question })
//     })
//       .then((res) => res.json()) 
//       .then((data) => sendResponse({ answer: data.answer }))
//       .catch((error) => sendResponse({ answer: "Error retrieving answer." }));

//     return true; // Keep port alive for asynchronous response
//   }
// });
