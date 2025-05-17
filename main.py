# main.py
from faq_bot import FAQBot

bot = FAQBot()
print("Welcome to the FAQ Bot! Type 'exit' or 'quit' to end the conversation.")
while True:
    user_input = input("You: ")
    if user_input.lower() in {"exit", "quit"}:
        break
    answer = bot.get_answer(user_input)
    print("Bot:", answer)
