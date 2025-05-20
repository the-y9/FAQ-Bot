# v2/faq_bot.py
from sentence_transformers import util
from v2.faq_data import faq_data, model
from typing import TypedDict
from torch import Tensor
import torch

# Define a TypedDict to specify the structure of FAQ state
class FAQState(TypedDict):
    question: str
    answer: str

# Function to match user question with the closest FAQ using semantic search
def match_faq(state: FAQState) -> FAQState:
    user_question = state["question"]
    
    # Encode the user's question to create its embedding
    user_embedding: Tensor = model.encode(user_question, convert_to_tensor=True)

        # Stack all precomputed FAQ embeddings into a tensor
    faq_embeddings = torch.stack([faq["embedding"] for faq in faq_data])

    # Compute cosine similarity in one batch
    similarities = util.cos_sim(user_embedding, faq_embeddings).squeeze(0)  # Shape: (num_faqs,)
    
    # Get best match index and score
    best_score, best_idx = torch.max(similarities, dim=0)

    
    # If the best score is above a threshold (0.6 here), return the corresponding answer
    if best_score >= 0.3:
        answer = faq_data[best_idx]["a"]
    else:
        answer = "Sorry, I couldn't find an answer to that question. Type 'exit' or 'quit' to end the conversation."

    return {"question": user_question, "answer": answer}, user_embedding, faq_data[best_idx]["embedding"], best_score.item() # matched_embedding

# FAQBot class for handling interactions
class FAQBot:
    def __init__(self):
        pass  # No initialization needed for now
    
    # Method to get the bot's response
    def get_answer(self, user_input: str) -> str:
        # Ensure the state is typed correctly as FAQState
        state: FAQState = {"question": user_input, "answer": ""}
        chat, user_embedding, matched_embedding, score = match_faq(state)
        return chat, user_embedding, matched_embedding, score
