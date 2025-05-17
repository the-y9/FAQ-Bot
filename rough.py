#%%
from v2.faq_bot import FAQBot

def bot(user_input = "Hi"):
    # Initialize the bot
    bot = FAQBot()

    # Get the bot's response
    answer = bot.get_answer(user_input)
    return answer

print(bot("ur target?"))

# %%
from v2.faq_data import faq_data
print(faq_data[2]["embedding"])

# %%
