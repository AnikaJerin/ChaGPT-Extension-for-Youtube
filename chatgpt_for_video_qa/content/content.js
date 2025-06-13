// (function(){
//   // create root for React or plain UI
//   const root = document.createElement('div');
//   root.id = 'chatbot-root';
  
//   root.innerHTML = `
//     <h3>Chatbot</h3>
//     <input id='chat-question' placeholder='Ask a question...' /><br/>
//     <button id='send-question'>Send</button>
//     <ul id='chat-messages'></ul>
//   `;

//   document.body.appendChild(root);

//   document.getElementById('send-question').addEventListener('click', async () => {
//     const question = document.getElementById('chat-question').value.trim();

//     if (question.length > 0) {
//       // Acquire video transcript first
//       const videoId = new URL(window.location.href).searchParams.get("v");

//       // Display user's question first
//       document.getElementById('chat-messages').innerHTML += "<li>Question: " + question + "</li>";

//       chrome.runtime.sendMessage({ 
//         action: "getTranscriptAndChat",
//         videoId,
//         question 
//       }, response => {
//         // Display chatbot's answer
//         document.getElementById('chat-messages').innerHTML += "<li>Answer: " + response.answer + "</li>";
//       });
//     }
//   });


// })();

