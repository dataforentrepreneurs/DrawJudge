import uuid
import time
import json
import logging
from typing import Dict, Any, Optional
import os

logger = logging.getLogger("party-games-hub")

# Optional redis import
try:
    import redis
    import fakeredis
except ImportError:
    redis = None
    fakeredis = None

# Initialize Redis client
REDIS_URL = os.environ.get("REDIS_URL")
if REDIS_URL and redis:
    redis_client = redis.from_url(REDIS_URL)
elif fakeredis:
    redis_client = fakeredis.FakeStrictRedis()
else:
    redis_client = None

def log_game_event(
    room_code: str, 
    game: str, 
    event_type: str, 
    user_id: Optional[str] = None, 
    details: Optional[Dict[str, Any]] = None,
    session_id: Optional[str] = None,
    connection_id: Optional[str] = None
):
    """
    Logs a structured game event to a Redis Stream for chronological AI analysis.
    Uses XADD with MAXLEN to auto-trim old events.
    """
    if not redis_client:
        return

    stream_key = f"events:{room_code.upper()}"
    
    event_data = {
        "event_id": str(uuid.uuid4()),
        "timestamp": str(int(time.time())),
        "event": event_type,
        "room_code": room_code.upper(),
        "game": game
    }
    
    if user_id:
        event_data["user_id"] = user_id
    if session_id:
        event_data["session_id"] = session_id
    if connection_id:
        event_data["connection_id"] = connection_id
    if details:
        event_data["details"] = json.dumps(details)

    try:
        # XADD with approximate MAXLEN of 500 to prevent memory bloat
        # In python redis: xadd(name, fields, id='*', maxlen=None, approximate=True)
        redis_client.xadd(stream_key, event_data, maxlen=500, approximate=True)
    except Exception as e:
        logger.error(f"Failed to log game event to stream {stream_key}: {e}")

def get_room_events(room_code: str, count: int = 100) -> list:
    """
    Retrieves the most recent events for a room.
    """
    if not redis_client:
        return []
        
    stream_key = f"events:{room_code.upper()}"
    try:
        # XREVRANGE to get newest first, then reverse or keep as is.
        # Format: xrevrange(name, max='+', min='-', count=None)
        raw_events = redis_client.xrevrange(stream_key, count=count)
        
        events = []
        for event_id, event_dict in raw_events:
            # redis returns byte keys/values, we decode them
            decoded_event = {k.decode('utf-8') if isinstance(k, bytes) else k: 
                             v.decode('utf-8') if isinstance(v, bytes) else v 
                             for k, v in event_dict.items()}
            
            # parse details if present
            if "details" in decoded_event and isinstance(decoded_event["details"], str):
                try:
                    decoded_event["details"] = json.loads(decoded_event["details"])
                except:
                    pass
                    
            # Add sequence/id context
            decoded_event["redis_event_id"] = event_id.decode('utf-8') if isinstance(event_id, bytes) else event_id
            events.append(decoded_event)
            
        # Reverse to return chronological order (oldest -> newest in the requested window)
        return events[::-1]
    except Exception as e:
        logger.error(f"Failed to fetch events for {stream_key}: {e}")
        return []
