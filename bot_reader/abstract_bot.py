from abc import ABC, abstractmethod
from typing import Dict
from telegram.ext import Application
import os
import csv

class AbstractReadBot(ABC):
    PARAMETERS = {
        "length": "Длина",
        "width": "Ширина", 
        "thickness": "Толщина",
        "time": "Время"
    }
    
    def __init__(self, app: Application):
        self.app = app
    
    @abstractmethod
    def run(self) -> None:
        pass
        
    @staticmethod
    def save_data(user_id: int, user_data: Dict) -> None:
        os.makedirs("data", exist_ok=True)
        file_exists = os.path.isfile("data/data.csv")
        
        try:
            with open("data/data.csv", "a", newline='') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["user_id"] + list(user_data.keys()))
                writer.writerow([str(user_id)] + [str(v) for v in user_data.values()])
                
        except Exception as e:
            print(f"Ошибка при сохранении в CSV: {e}")
            raise