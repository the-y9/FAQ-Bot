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
            

        # Convert the plot to an image that Gradio can display
        if not fig:
            print("no fig")
            return chat["answer"], None  # Return the answer without an image if visualization fails
        
        img = BytesIO()
        fig.savefig(img, format='png')
        img.seek(0)  # Reset the pointer to the beginning of the image
        pil_img = Image.open(img)

        return chat["answer"], pil_img  # Return both the FAQ answer and the image of the cosine similarity

    # Create Gradio interface
    with gr.Blocks() as demo:
        # Define the left and right columns
        with gr.Row():
            with gr.Column(scale=1):  # Left side - Chat
                gr.Markdown("### FAQ Bot - Ask a Question")
                chat_input = gr.Textbox(label="Ask your question", placeholder="Type here...")
                chat_output = gr.Textbox(label="Answer", interactive=False)

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
