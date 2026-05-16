from fastapi import APIRouter, Request, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Any
import time
import logging
from services.event_logger import redis_client

logger = logging.getLogger("party-games-hub")
router = APIRouter(tags=["Telemetry"])

ANOMALY_QUEUE_KEY = "anomaly_queue"

class FrontendCrashPayload(BaseModel):
    message: str
    stack_trace: Optional[str] = None
    url: Optional[str] = None
    browser_info: Optional[str] = None
    room_code: Optional[str] = None
    player_id: Optional[str] = None
    game: Optional[str] = None

@router.post("/api/telemetry/frontend-error")
async def report_frontend_error(payload: FrontendCrashPayload, background_tasks: BackgroundTasks):
    """
    Ingests frontend crash reports and forwards them to the AI Ops Anomaly Queue.
    """
    if not redis_client:
        return {"status": "ignored", "reason": "Redis not configured"}

    def push_to_queue():
        try:
            event_data = {
                "room_code": payload.room_code or "UNKNOWN",
                "game": payload.game or "UNKNOWN",
                "issue_type": "frontend_crash",
                "timestamp": str(int(time.time())),
                "error_details": payload.model_dump_json()
            }
            redis_client.xadd(ANOMALY_QUEUE_KEY, event_data, maxlen=1000, approximate=True)
            logger.info(f"Pushed frontend crash to anomaly queue: {payload.message[:50]}...")
        except Exception as e:
            logger.error(f"Failed to push frontend telemetry to queue: {e}")

    background_tasks.add_task(push_to_queue)
    return {"status": "received"}
