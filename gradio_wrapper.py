from v2.faq_bot import FAQBot
import gradio as gr

def main_gradio():
    # Initialize the bot
    bot = FAQBot()

    # Function to handle Gradio interface
    def answer_question(user_input):
        return bot.get_answer(user_input)

    # Create Gradio interface
    demo = gr.Interface(fn=answer_question, 
                        inputs="text", 
                        outputs="text", 
                        title="FAQ Bot",
                        description="Ask a frequently asked question, and get the best matching answer.")

    # Launch Gradio interface
    demo.launch()

# This is used to only launch Gradio if this script is run directly
if __name__ == "__main__":
    main_gradio()
