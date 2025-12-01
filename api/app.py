from typing import Union
from fastapi import FastAPI
from config import TOKEN
from commands import CommandBase, ScedualeWatering 


COMMANDS : list[CommandBase] = []
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}




@app.get('/info')
def command(token: str, id: int):
    if token != TOKEN:
        return {"error": True, "message": "Invalid token"}
    
    return {'error': False, 
            'message': 'Command sent',
            'commands': []}
