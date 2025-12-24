function sendQuestion() {
    const input = document.getElementById("question");
    const question = input.value.trim();
    if (!question) return;

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ question })
    })
    .then(res => res.json())
    .then(data => {
        const chatBox = document.getElementById("chat-box");
        chatBox.innerHTML = "";

        data.history.forEach(msg => {
            chatBox.innerHTML += `
                <div class="user">You: ${msg.user}</div>
                <div class="bot">Bot: ${msg.bot}</div>
            `;
        });

        input.value = "";
        chatBox.scrollTop = chatBox.scrollHeight;
    });
}
