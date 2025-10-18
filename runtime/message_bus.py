from collections import defaultdict
from typing import Callable, Dict, List

class MessageBus:
    def __init__(self):
        self.subscriptions: Dict[str, List[Callable]] = defaultdict(list)

    def subscribe(self, topic: str, callback: Callable):
        self.subscriptions[topic].append(callback)

    def publish(self, topic: str, message: any):
        for callback in self.subscriptions.get(topic, []):
            callback(message)
