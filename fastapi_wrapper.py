from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from v2.faq_bot import FAQBot
from v2.viz_utils import visualize_embeddings_cosine
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
        chat, user_embedding, matched_embedding = bot.get_answer(payload.question)

        response = {
            "answer": chat["answer"],
            "has_visual": user_embedding is not None and matched_embedding is not None
        }

        return JSONResponse(content=response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {e}")

@app.post("/visualization")
async def get_visualization(payload: QuestionRequest):
    try:
        chat, user_embedding, matched_embedding = bot.get_answer(payload.question)

        if user_embedding is None or matched_embedding is None:
            raise HTTPException(status_code=400, detail="Embeddings not available.")

        fig = visualize_embeddings_cosine(
            user_embedding=user_embedding,
            matched_embedding=matched_embedding,
            labels=["User Input", "Matched Question"]
        )

        buf = BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig)

        return StreamingResponse(buf, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Visualization error: {e}")

# Run with: uvicorn fastapi_app:app --host 0.0.0.0
if __name__ == "__main__":
    uvicorn.run("fastapi_wrapper:app", host="0.0.0.0", reload=True)
