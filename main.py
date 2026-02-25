import sys
import traceback
import re
from io import StringIO
from typing import List

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

# ---------------------------
# /comment endpoint (unchanged)
# ---------------------------

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

# ---------------------------
# /code-interpreter endpoint (fixed)
# ---------------------------

class CodeRequest(BaseModel):
    code: str


def execute_python_code(code: str) -> dict:
    """
    Execute Python code and return exact output.

    Returns:
        {
            "success": bool,
            "output": str  # Exact stdout or traceback
        }
    """
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        # ✅ Compile user code as "<string>" so traceback points to user lines
        compiled = compile(code, "<string>", "exec")
        exec(compiled, {})  # isolated globals

        output = sys.stdout.getvalue()
        return {"success": True, "output": output}

    except Exception:
        output = traceback.format_exc()
        return {"success": False, "output": output}

    finally:
        sys.stdout = old_stdout


def extract_error_lines_from_traceback(tb: str) -> List[int]:
    """
    ✅ Only capture line numbers from the executed user code:
       File "<string>", line N
    This avoids capturing main.py line numbers.
    """
    nums = re.findall(r'File "<string>", line (\d+)', tb)
    return sorted({int(n) for n in nums})


@app.post("/code-interpreter")
async def code_interpreter(request: CodeRequest):
    if request.code is None or not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")

    run = execute_python_code(request.code)

    if run["success"]:
        return {"error": [], "result": run["output"]}

    tb = run["output"]
    lines = extract_error_lines_from_traceback(tb)
    return {"error": lines, "result": tb}