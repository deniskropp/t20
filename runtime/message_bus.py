import logging
import re
from collections import defaultdict
from typing import Callable, Dict, List, Any, Optional
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class SpaceMessage(BaseModel):
    name: str
    type: str
    place: str
    index: str
    content: Any

    def to_string(self) -> str:
        return f"⫻{self.name}/{self.type}:{self.place}/{self.index}\n{self.content}"

    @staticmethod
    def parse(text: str) -> Optional['SpaceMessage']:
        # Basic regex to parse Space Format header
        match = re.match(r"⫻(\w+)/(\w+):(\w+)/(\w+)\n(.*)", text, re.DOTALL)
        if match:
            return SpaceMessage(
                name=match.group(1),
                type=match.group(2),
                place=match.group(3),
                index=match.group(4),
                content=match.group(5)
            )
        return None

class MessageBus:
    def __init__(self):
        self.subscriptions: Dict[str, List[Callable]] = defaultdict(list)

    def subscribe(self, topic: str, callback: Callable):
        self.subscriptions[topic].append(callback)

    def publish(self, topic: str, message: Any):
        # Validate if it's a SpaceMessage or try to convert
        if isinstance(message, str) and message.startswith("⫻"):
            parsed = SpaceMessage.parse(message)
            if parsed:
                logger.debug(f"Valid Space Message on {topic}: {parsed.name}")
            else:
                logger.warning(f"Invalid Space Message format on {topic}: {message[:50]}...")
        
        for callback in self.subscriptions.get(topic, []):
            try:
                callback(message)
            except Exception as e:
                logger.error(f"Error in subscriber callback for topic {topic}: {e}")
