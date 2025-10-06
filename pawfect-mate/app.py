import db
import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag import rag

app = FastAPI()

# In-memory store (replace later with a DB)
conversations = {}


# Request/Response models
class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    conversation_id: str
    answer: dict

class FeedbackRequest(BaseModel):
    conversation_id: str
    feedback: int


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    if not request.question:
        raise HTTPException(status_code=400, detail="Question is required")

    answer_data = rag(request.question)
    conversation_id = str(uuid.uuid4())

    conversations[conversation_id] = {
        "question": request.question,
        "answer": answer_data['answer'],
        "feedback": None
    }
    db.save_conversation(
        conversation_id,
        request.question,
        answer_data,
    )
    return AskResponse(conversation_id=conversation_id, answer=answer_data)


@app.post("/feedback")
def feedback(request: FeedbackRequest):
    if request.conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Invalid conversation_id")

    if request.feedback not in [-1, 1]:
        raise HTTPException(status_code=400, detail="Feedback must be -1 or 1")
    
    db.save_feedback(
        conversation_id=request.conversation_id,
        feedback=request.feedback
    )

    conversations[request.conversation_id]["feedback"] = request.feedback

    return {"message": "Feedback received"}
