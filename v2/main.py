# v2/main.py
from v2.faq_bot import FAQBot

def main():
    # Initialize the bot
    bot = FAQBot()

    print("Welcome to the FAQ Bot! Type 'exit' or 'quit' to end the conversation.")
    
    while True:
        # Take user input
        user_input = input("You: ")
        
        # Exit condition
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        
        # Get the bot's response
        answer = bot.get_answer(user_input)
        print("Bot:", answer)  # Output the bot's response

if __name__ == "__main__":
    main()
