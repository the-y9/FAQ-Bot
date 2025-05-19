from v2.faq_bot import FAQBot
from v2.viz_utils import visualize_embeddings_cosine
import gradio as gr
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from PIL import Image

def main_gradio():
    # Initialize the bot
    bot = FAQBot()

    # Function to handle Gradio interface
    def answer_question(user_input):
        # Get the answer and embeddings using FAQBot
        chat, user_embedding, matched_embedding = bot.get_answer(user_input)

        # Generate the cosine similarity visualization plot
        try:
            if user_embedding is None or matched_embedding is None:
                print("Embeddings are not valid.")
                return chat["answer"], None
            
            fig = visualize_embeddings_cosine(
                user_embedding=user_embedding,
                matched_embedding=matched_embedding,
                labels=["User Input", "Matched Question"]
            )
        except Exception as e:
            print(f"Error in visualization: {e}")
            return chat["answer"], None  # Return only the answer if visualization fails

        # Convert the plot to an image that Gradio can display
        if fig is None:
            print("No figure generated.")
            return chat["answer"], None  # Return only the answer if the plot is not generated
        
        img = BytesIO()
        fig.savefig(img, format='png')
        img.seek(0)  # Reset the pointer to the beginning of the image
        pil_img = Image.open(img)

        return chat["answer"], pil_img  # Return both the FAQ answer and the image of the cosine similarity

    # Define some CSS styles to apply
    css = """
    /* Background color and padding */
    .gradio-container {
        background-color: #f7f7f7;
        padding: 30px;
    }

    /* Styling for the header */
    .gr-markdown h1 {
        text-align: center;
        font-size: 2.5rem;
        color: #4CAF50;
        margin-bottom: 20px;
    }

    .gr-markdown h2 {
        text-align: center;
        font-size: 2rem;
        color: #333;
        margin-bottom: 15px;
    }

    /* Styling for the text input */
    .gr-textbox input {
        border-radius: 8px;
        border: 2px solid #ddd;
        padding: 10px;
        font-size: 1.2rem;
    }

    .gr-textbox input:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 5px rgba(0, 194, 122, 0.5);
    }

    /* Styling for the buttons */
    .gr-button {
        background-color: #4CAF50;
        color: white;
        font-size: 1rem;
        padding: 12px 20px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        margin-top: 10px;
    }

    .gr-button:hover {
        background-color: #45a049;
    }

    /* Styling for the columns */
    .gr-column {
        margin: 20px 0;
    }

    /* Styling for the image container */
    .gr-image-container {
        border-radius: 8px;
        overflow: hidden;
        background-color: #fff;
        padding: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }

    /* Markdown styling */
    .gr-markdown {
        font-size: 1rem;
        line-height: 1.6;
        color: #333;
    }

    /* Add some spacing between sections */
    .gr-row {
        margin-bottom: 30px;
    }

    /* Insights section style */
    .gr-markdown label {
        font-size: 1.1rem;
        font-weight: bold;
        color: #333;
    }
    """

    # Create Gradio interface
    with gr.Blocks(css=css) as demo:
        gr.Markdown("# FAQ Bot with Cosine Similarity Visualization")
        gr.Markdown("Ask a question and see the cosine similarity between your input and the matched question.")    

        # Define the left and right columns
        with gr.Row():
            with gr.Column(scale=1):  # Left side - Chat
                gr.Markdown("### FAQ Bot - Ask a Question")
                chat_input = gr.Textbox(label="Ask your question", placeholder="Type here...", interactive=True)
                chat_output = gr.Textbox(label="Answer", interactive=False)
                gr.Markdown(value="""
### ℹ️ Embedding Visualization

This plot compares a query to its matched entry using AI-generated embeddings.

* 🔵 **Blue Arrow** – Represents the user query, normalized to unit length.
* 🔴 **Red Arrow** – Represents the matched query from the dataset.

#### Key Concepts:

* **Cosine Similarity**: The cosine similarity between the blue and red arrows indicates how **semantically similar** the queries are. A value close to 1 means the queries are highly similar.

* **Length = Confidence**: The length of the red arrow indicates how **strong** or **meaningful** the match is. Longer = clearer match, shorter = weaker match.

#### Perfect Match:

If the **blue** and **red arrows** are exactly same (cosine similarity = 1, with equal lengths), it means the model found a **perfect match** for the user query in the data. For example, the query "hi" produces the same vector.

""", label="Insights")

            with gr.Column(scale=1):  # Right side - Image visualization
                gr.Markdown("### Cosine Similarity Visualization")
                cosine_image = gr.Image(label="Cosine Similarity Plot", interactive=False)

        # Link the inputs and outputs
        chat_input.submit(answer_question, inputs=chat_input, outputs=[chat_output, cosine_image])

    # Launch the Gradio interface
    demo.launch(pwa=True)

# This is used to only launch Gradio if this script is run directly
if __name__ == "__main__":
    main_gradio()
