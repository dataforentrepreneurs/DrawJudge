import asyncio
import time
import logging
from typing import Dict, Any

from services.event_logger import redis_client
from services.snapshot_service import take_room_snapshot

# We import the active_rooms from both services
# Note: We do this inside the function or with try/except to avoid circular imports during startup
import services.state_manager as dj_state
import services.couple_clash_service as cc_state

logger = logging.getLogger("party-games-hub")

ANOMALY_QUEUE_KEY = "anomaly_queue"

async def check_drawjudge_rooms():
    current_time = time.time()
    for room_code, room in list(dj_state.active_rooms.items()):
        try:
            anomaly_detected = False
            issue_type = None
            
            # Check for stuck drawing phase
            if room.status == "drawing":
                # If round_end_time was more than 3 minutes ago
                if room.round_end_time > 0 and current_time > (room.round_end_time + 180):
                    anomaly_detected = True
                    issue_type = "stuck_drawing_phase"
            
            # Check for abandoned room (host disconnected for a long time)
            if not anomaly_detected:
                host_id = room.host_id
                if host_id in room.player_presence:
                    presence = room.player_presence[host_id]
                    if not presence.get("connected", False):
                        last_seen = presence.get("last_seen", current_time)
                        if current_time - last_seen > 900: # 15 minutes
                            anomaly_detected = True
                            issue_type = "abandoned_room"

            if anomaly_detected:
                report_anomaly("DrawJudge", room_code, issue_type, room)
                
        except Exception as e:
            logger.error(f"Error monitoring DrawJudge room {room_code}: {e}")

async def check_coupleclash_rooms():
    current_time = time.time()
    for room_code, room in list(cc_state.active_rooms.items()):
        try:
            anomaly_detected = False
            issue_type = None
            
            # Similar checks tailored for CoupleClash
            if room.status in ["answering", "revealing", "judging"]:
                # Assume a state shouldn't last more than 3 minutes generally
                state_duration = current_time - room.current_state_start_time
                if state_duration > 180:
                    anomaly_detected = True
                    issue_type = f"stuck_{room.status}_phase"
                    
            # Check abandoned
            if not anomaly_detected:
                host_id = room.host_id
                if host_id in room.player_presence:
                    presence = room.player_presence[host_id]
                    if not presence.get("connected", False):
                        last_seen = presence.get("last_seen", current_time)
                        if current_time - last_seen > 900: # 15 minutes
                            anomaly_detected = True
                            issue_type = "abandoned_room"

            if anomaly_detected:
                report_anomaly("CoupleClash", room_code, issue_type, room)
                
        except Exception as e:
            logger.error(f"Error monitoring CoupleClash room {room_code}: {e}")

def report_anomaly(game: str, room_code: str, issue_type: str, room_state: Any):
    """
    Takes a snapshot of the room and pushes the anomaly to the Redis Stream queue.
    """
    if not redis_client:
        return
        
    logger.info(f"Anomaly detected in {game} room {room_code}: {issue_type}")
    
    # 1. Take a fresh snapshot so AI has the exact moment of failure
    take_room_snapshot(room_code, game, room_state)
    
    # 2. Push to anomaly queue
    anomaly_event = {
        "room_code": room_code,
        "game": game,
        "issue_type": issue_type,
        "timestamp": str(int(time.time()))
    }
    
    try:
        redis_client.xadd(ANOMALY_QUEUE_KEY, anomaly_event, maxlen=1000, approximate=True)
    except Exception as e:
        logger.error(f"Failed to push anomaly to queue: {e}")

async def monitor_rooms_loop():
    """
    Background task that runs continuously to monitor room health.
    """
    logger.info("Starting Room Monitoring Agent...")
    while True:
        try:
            await check_drawjudge_rooms()
            await check_coupleclash_rooms()
        except asyncio.CancelledError:
            logger.info("Room Monitoring Agent shutting down.")
            break
        except Exception as e:
            logger.error(f"Error in monitor_rooms_loop: {e}")
            
        # Run every 30 seconds
        await asyncio.sleep(30)
