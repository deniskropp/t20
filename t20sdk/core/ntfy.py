import asyncio
import logging
import json
import httpx
from typing import Optional

logger = logging.getLogger(__name__)

class NtfyClient:
    """
    Client for interacting with Ntfy (https://ntfy.sh) for HITL notifications.
    """
    def __init__(self, topic: str):
        self.topic = topic
        self.base_url = "https://ntfy.violass.club"

    async def send_confirmation_request(self, task_description: str) -> bool:
        """
        Sends a notification with "Yes"/"No" actions and waits for a response.
        
        Args:
            task_description: The description of the task asking for approval.
            
        Returns:
            True if approved (Yes), False if rejected (No).
        """
        import uuid
        import time

        request_id = str(uuid.uuid4())
        # Filter messages since 1 second ago to avoid race conditions with clock skew, 
        # but primarily we rely on the request_id.
        start_time = int(time.time()) 

        # Construct the notification with actions
        headers = {
            "Title": "T20 Task Approval Required",
            "Priority": "high",
            "Tags": "question",
            "Actions": json.dumps([
                {
                    "action": "http",
                    "label": "Yes, Proceed",
                    "url": f"{self.base_url}/{self.topic}",
                    "method": "POST",
                    "body": f"approved {request_id}"
                },
                {
                    "action": "http",
                    "label": "No, Stop",
                    "url": f"{self.base_url}/{self.topic}",
                    "method": "POST",
                    "body": f"rejected {request_id}"
                }
            ])
        }
        
        message = f"Approve task execution?\n\nTask: {task_description}\nID: {request_id}"
        
        async with httpx.AsyncClient() as client:
            # 1. Send the question
            resp = await client.post(f"{self.base_url}/{self.topic}", content=message, headers=headers)
            resp.raise_for_status()
            logger.info(f"Sent Ntfy request (ID: {request_id}) to topic '{self.topic}'. Waiting for answer...")
            
            # 2. Poll for the answer
            # We listen for new messages on the same topic properly filtering by time and request_id
            poll_url = f"{self.base_url}/{self.topic}/json?since={start_time}"

            # 3. Wait for the answer
            while True:
                try:
                    async with client.stream("GET", poll_url) as response:
                        async for line in response.aiter_lines():
                            if not line:
                                continue
                        
                            try:
                                data = json.loads(line)
                                event = data.get("event")
                                if event == "message":
                                    body = data.get("message", "").strip().lower()
                                    
                                    # Check if this message is a response to our specific request ID
                                    # The format expected is "approved <uuid>" or "rejected <uuid>"
                                    parts = body.split()
                                    if len(parts) >= 2:
                                        action = parts[0]
                                        msg_req_id = parts[1]
                                        
                                        if msg_req_id == request_id:
                                            if action == "approved":
                                                logger.info(f"Received approval for request {request_id}.")
                                                return True
                                            elif action == "rejected":
                                                logger.info(f"Received rejection for request {request_id}.")
                                                return False
                                    # Ignore messages that don't match our ID
                            except json.JSONDecodeError:
                                continue
                except httpx.ReadTimeout as e:
                    logger.info(f"Timed out waiting for approval for request {request_id}.")
                    continue
                except httpx.RequestError as e:
                    logger.error(f"Ntfy communication error: {e}")
                    raise Exception("Ntfy communication error: {e}")
