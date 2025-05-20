async function getAnswer() {
    const question = document.getElementById("question").value;
    if (!question) return;

    // Call FastAPI backend
    const response = await fetch("https://faq-bot-u90z.onrender.com/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question })
    });

    const data = await response.json();
    console.log(data);
    document.getElementById("answer").innerText = "Answer: " + data.answer;

    if (data.image_base64) {
    document.getElementById("cosine-plot").src = "data:image/png;base64," + data.image_base64;
    } else {
    document.getElementById("cosine-plot").src = "";
    }
}
