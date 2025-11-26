# app.py
from typing import List, Union
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, Field
import uvicorn
import logging
from sum_engine import compute_sum, InvalidNumberError

app = FastAPI()
logger = logging.getLogger("sum_service")
logger.setLevel(logging.INFO)


class SumRequest(BaseModel):
    numbers: List[Union[int, float, str]] = Field(..., min_items=1)


class SumResponse(BaseModel):
    request_id: str
    sum: Union[str, float]
    count: int


@app.post("/sum", response_model=SumResponse)
async def sum_endpoint(req: Request, payload: SumRequest):
    request_id = req.headers.get("X-Request-ID") or "req-" + __import__("uuid").uuid4().hex
    try:
        result = compute_sum(payload.numbers, strategy="auto")
    except InvalidNumberError as e:
        logger.error("Invalid input %s %s", request_id, e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        logger.exception("Unexpected error %s", request_id)
        raise HTTPException(status_code=500, detail=f"Internal error. Request id {request_id}")

    s = result["sum"]
    if hasattr(s, "to_eng_string"):
        s = str(s)

    return {"request_id": request_id, "sum": s, "count": result["count"]}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="info")
