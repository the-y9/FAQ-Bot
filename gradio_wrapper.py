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
    demo = gr.Interface(fn=answer_question, 
                        inputs="text", 
                        outputs=["text", "image"],  # Output both text (answer) and image (cosine plot)
                        title="FAQ Bot with Cosine Similarity Visualization",
                        description="Ask a frequently asked question, and get the best matching answer with a visualization of cosine similarity between your question and the matched answer.")

    demo.launch()

# This is used to only launch Gradio if this script is run directly
if __name__ == "__main__":
    main_gradio()
