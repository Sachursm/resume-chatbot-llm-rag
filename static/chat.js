const chatBox = document.getElementById("chat-box");
const input = document.getElementById("question");

function appendMessage(text, sender) {
    const msg = document.createElement("div");
    msg.className = `message ${sender}`;

    const content = document.createElement("div");
    content.className = "message-content";
    content.innerHTML = text.replace(/\n/g, "<br>");

    msg.appendChild(content);
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendQuestion() {
    const question = input.value.trim();
    if (!question) return;

    appendMessage(question, "user");
    input.value = "";

    // Typing indicator
    const typing = document.createElement("div");
    typing.className = "message bot";
    typing.innerHTML = `
        <div class="typing-indicator">
            <span></span><span></span><span></span>
        </div>
    `;
    chatBox.appendChild(typing);
    chatBox.scrollTop = chatBox.scrollHeight;

    const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question })
    });

    const data = await res.json();

    chatBox.removeChild(typing);
    appendMessage(data.answer, "bot");
}
