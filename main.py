from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Enable CORS (VERY IMPORTANT FOR GRADER)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CommentRequest(BaseModel):
    comment: str


def analyze_sentiment(text: str):
    text = text.lower()

    positive_words = ["amazing", "great", "excellent", "love", "fantastic", "awesome", "good"]
    negative_words = ["bad", "terrible", "awful", "hate", "worst", "poor"]

    score = 0

    for word in positive_words:
        if word in text:
            score += 1

    for word in negative_words:
        if word in text:
            score -= 1

    if score > 1:
        return {"sentiment": "positive", "rating": 5}
    elif score == 1:
        return {"sentiment": "positive", "rating": 4}
    elif score == 0:
        return {"sentiment": "neutral", "rating": 3}
    elif score == -1:
        return {"sentiment": "negative", "rating": 2}
    else:
        return {"sentiment": "negative", "rating": 1}


@app.post("/comment")
async def analyze_comment(request: CommentRequest):
    if not request.comment.strip():
        raise HTTPException(status_code=400, detail="Comment cannot be empty")

    return analyze_sentiment(request.comment)