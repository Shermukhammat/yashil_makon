from abc import ABC, abstractmethod
from datetime import datetime


class CommandBase(ABC):
    def __init__(self, name: str):
        self.name = name 
    
    @abstractmethod
    def data(self) -> dict:
        return {}



class ScedualeWatering(CommandBase):
    def __init__(self, name: str, start_time: datetime = None, duration: int = None):
        super().__init__(name)
        self.start_time = start_time
        self.duration = duration 

    def data(self) -> dict:
        return {
            'start_time': self.start_time,
            'duration': self.duration
        }
    
