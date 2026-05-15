import json
import logging
from typing import Optional, Dict, Any
from services.event_logger import log_game_event

logger = logging.getLogger("party-games-hub")

def take_room_snapshot(room_code: str, game: str, room_state: Any):
    """
    Takes a snapshot of the current room state and logs it to the event stream.
    This gives the AI a known 'ground truth' state to anchor its event timeline.
    """
    try:
        # Assuming room_state has a to_dict_lite() method (like DrawJudge's RoomState)
        # or can be serialized to a dict.
        
        state_dict = {}
        if hasattr(room_state, 'to_dict_lite'):
            state_dict = room_state.to_dict_lite()
        elif hasattr(room_state, '__dict__'):
            # Fallback for simple objects
            state_dict = {k: v for k, v in room_state.__dict__.items() if not k.startswith('_')}
        else:
            state_dict = {"raw": str(room_state)}
            
        # Clean up any heavy or non-serializable fields if necessary
        # We only need operational context, not the full drawing history.
        if "submissions" in state_dict:
            state_dict["submissions_count"] = len(state_dict["submissions"])
            del state_dict["submissions"]
        if "player_history" in state_dict:
            del state_dict["player_history"]

        log_game_event(
            room_code=room_code,
            game=game,
            event_type="state_snapshot",
            details=state_dict
        )
        logger.debug(f"Snapshot taken for {game} room {room_code}")
    except Exception as e:
        logger.error(f"Failed to take snapshot for {game} room {room_code}: {e}")
