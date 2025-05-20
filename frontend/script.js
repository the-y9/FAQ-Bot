let loading = false;
// const BASE_URL = "https://faq-bot-u90z.onrender.com";
const BASE_URL = "http://127.0.0.1:5000";


async function getAnswer() {
    let loading = false;

    const questionInput = document.getElementById("question");
    const loadingIndicator = document.getElementById("loading");
    const answerElement = document.getElementById("answer");
    const cosinePlotElement = document.getElementById("cosine-plot");

    const question = questionInput.value;
    if (!question) return;
    answerElement.innerText = "Bot: ";

    // Show loading indicator
    loadingIndicator.style.display = "block";
    loading = true;

    console.time("Total Time");
    console.time("Fetch Answer Time");

    try {
        // Get answer from backend
        const answerData = await fetchAnswer(question);
        console.timeEnd("Fetch Answer Time");
        console.log("Answer received at:", new Date().toISOString());

        answerElement.innerText = "Bot: " + answerData.answer;

        console.time("Projection + Visualization Time");

        // Get projections and visualization
        fetchProjections(answerData.user_embedding, answerData.matched_embedding)
            .then(projectionData => {
                console.log("Projection data received at:", new Date().toISOString());
                return fetchVisualization(
                    projectionData.user_proj,
                    projectionData.rotated_vec,
                    projectionData.cos_sim,
                    projectionData.angle_deg,
                    cosinePlotElement
                );
            })
            .then(() => {
                console.log("Visualization rendered at:", new Date().toISOString());
                console.timeEnd("Projection + Visualization Time");
                console.timeEnd("Total Time");
            })
            .catch(error => {
                console.error("Plot Error:", error);
                console.timeEnd("Projection + Visualization Time");
                console.timeEnd("Total Time");
            });

    } catch (error) {
        console.error("Error:", error);
        answerElement.innerText = "Error: " + error.message;
        console.timeEnd("Fetch Answer Time");
        console.timeEnd("Total Time");
    } finally {
        // Hide loading indicator
        loadingIndicator.style.display = "none";
        loading = false;
    }
}


async function fetchAnswer(question) {
    const response = await fetch(`${BASE_URL}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
    });

    if (!response.ok) {
        throw new Error(`Error: ${response.status} - ${response.statusText}`);
    }

    return await response.json();
}

async function fetchProjections(userEmbedding, matchedEmbedding) {
    const response = await fetch(`${BASE_URL}/projections`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_embedding: userEmbedding, matched_embedding: matchedEmbedding }),
    });

    if (!response.ok) {
        throw new Error(`Error: ${response.status} - ${response.statusText}`);
    }

    return await response.json();
}

async function fetchVisualization(userProj, rotatedVec, cosSim, angleDeg, cosinePlotElement) {
    const response = await fetch(`${BASE_URL}/visualization`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_proj: userProj, rotated_vec: rotatedVec, cos_sim: cosSim, angle_deg: angleDeg }),
    });

    if (!response.ok) {
        throw new Error(`Error: ${response.status} - ${response.statusText}`);
    }

    const imageBlob = await response.blob();
    const imageUrl = URL.createObjectURL(imageBlob);

    // Display the visualization image
    cosinePlotElement.src = imageUrl;
}
