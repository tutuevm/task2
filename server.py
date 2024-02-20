import random

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


'''Сервер для тестирования'''

# uvicorn server:app --reload --port 8000  - команда для запуска сервера


class Item(BaseModel):
    payload: str


@app.get('/')
async def sent_data():
    answer = {
        'recipients' :['http://127.0.0.1:8000/sent_data'],
        'payload': 'data'
    }
    return answer

@app.post('/sent_data')
async def read_root():
    answer = random.randint(1,2)
    return answer