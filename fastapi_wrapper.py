from typing import List
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from v2.faq_bot import FAQBot
from v2.viz_utils import get_projections_cosine, plot_embeddings_cosine
from io import BytesIO
import matplotlib.pyplot as plt
from PIL import Image
import uvicorn

app = FastAPI(title="FAQ Bot API with Cosine Similarity")

bot = FAQBot()  # Initialize bot once

@app.get("/")
async def root():
    return {"message": "Welcome to the FAQ Bot API! Use /ask to ask a question."}
# Pydantic model for request
class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(payload: QuestionRequest):
    try:
        chat, user_embedding, matched_embedding, score = bot.get_answer(payload.question)

        response = {
            "answer": chat["answer"],
            "user_embedding": user_embedding.tolist(),
            "matched_embedding": matched_embedding.tolist(),
            "score": score
        }

        return JSONResponse(content=response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {e}")
    
class EmbeddingRequest(BaseModel):
    user_embedding: List[float]
    matched_embedding: List[float]

@app.post("/projections")
async def get_projections(payload: EmbeddingRequest) -> dict:
    try:
        # chat, user_embedding, matched_embedding = bot.get_answer(payload.question)

        # if user_embedding is None or matched_embedding is None:
        #     raise HTTPException(status_code=400, detail="Embeddings not available.")

        return get_projections_cosine(
            user_embedding=payload.user_embedding,
            matched_embedding=payload.matched_embedding,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing embeddings: {e}")

class VisualizationRequest(BaseModel):
    user_proj: List[float]
    rotated_vec: List[float]
    cos_sim: float
    angle_deg: float

@app.post("/visualization")
async def get_visualization(payload: VisualizationRequest):
    try:
        fig = plot_embeddings_cosine(
            labels=["User Input", "Matched Question"],
            user_proj=payload.user_proj,
            rotated_vec=payload.rotated_vec,
            cos_sim=payload.cos_sim,
            angle_deg=payload.angle_deg,
            title="Cosine-Based Embedding Visualization"
        )

        buf = BytesIO()
        fig.savefig(buf, format='jpeg')
        buf.seek(0)
        plt.close(fig)

        return StreamingResponse(buf, media_type="image/jpeg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Visualization error: {e}")

# # Run with: uvicorn fastapi_app:app --host 0.0.0.0
# if __name__ == "__main__":
#     uvicorn.run("fastapi_wrapper:app", host="127.0.0.1", reload=True)
