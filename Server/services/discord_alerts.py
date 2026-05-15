import os
import httpx
import logging
import json
from typing import Optional, Dict, Any, List

logger = logging.getLogger("party-games-hub")

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

class Severity:
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"

SEVERITY_COLORS = {
    Severity.LOW: 0x808080, # Gray
    Severity.MEDIUM: 0xFFA500, # Orange
    Severity.HIGH: 0xFF4500, # Red-Orange
    Severity.CRITICAL: 0xFF0000, # Red
    Severity.REVIEW_REQUIRED: 0xFFFF00 # Yellow
}

async def send_discord_alert(
    title: str,
    description: str,
    severity: str = Severity.LOW,
    fields: Optional[List[Dict[str, Any]]] = None
):
    """
    Sends a structured alert to a Discord Webhook.
    """
    if not DISCORD_WEBHOOK_URL:
        logger.warning("Discord webhook URL not configured. Skipping alert.")
        return

    color = SEVERITY_COLORS.get(severity, SEVERITY_COLORS[Severity.LOW])

    embed = {
        "title": f"[{severity}] {title}",
        "description": description,
        "color": color,
    }

    if fields:
        embed["fields"] = fields

    payload = {
        "embeds": [embed]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5.0)
            if response.status_code >= 400:
                logger.error(f"Failed to send Discord alert: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Error sending Discord alert: {e}")

async def send_ai_anomaly_alert(
    room_code: str,
    game: str,
    duration_secs: int,
    player_count: int,
    severity: str,
    probable_cause: str,
    recommended_action: str,
    confidence: float
):
    """
    Helper to send standard human-friendly anomaly reports from the AI Ops Agent.
    """
    if confidence < 0.65:
        severity = Severity.REVIEW_REQUIRED
        
    title = f"🚨 {game} Room Anomaly"
    
    description = (
        f"**Room:** {room_code} | **Players:** {player_count} | **Duration:** {duration_secs}s\n\n"
        f"**Probable Cause:**\n{probable_cause}\n\n"
        f"**Recommended Action:**\n{recommended_action}\n\n"
        f"**Confidence:** {int(confidence * 100)}%"
    )
    
    await send_discord_alert(title=title, description=description, severity=severity)
