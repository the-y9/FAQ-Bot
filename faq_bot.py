# faq_bot.py
from langgraph.graph import StateGraph
from rapidfuzz import process
from typing import TypedDict
from faq_data import faq_data

class FAQState(TypedDict):
    question: str
    answer: str

def match_faq(state: FAQState) -> FAQState:
    question = state["question"]
    result = process.extractOne(question, [faq["q"].lower() for faq in faq_data])

    if result:
        best_match, score, _ = result
        if score >= 70:
            answer = next(faq["a"] for faq in faq_data if faq["q"].lower() == best_match)
        else:
            answer = "Sorry, I couldn't find an answer to that question."
    else:
        answer = "Sorry, I couldn't find an answer to that question."

    return {"question": question, "answer": answer}


# Build the LangGraph
builder = StateGraph(FAQState)

# Add node
builder.add_node("match_faq", match_faq)

# Set flow: Start → match_faq → End
builder.set_entry_point("match_faq")
builder.set_finish_point("match_faq")

# Compile it
faq_graph = builder.compile()

class FAQBot:
    def __init__(self):
        self.graph = faq_graph

    def get_answer(self, user_input: str) -> str:
        state = {"question": user_input, "answer": ""}
        result = self.graph.invoke(state)
        return result["answer"]

