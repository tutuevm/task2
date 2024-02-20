import asyncio
from enum import Enum
from typing import List
from datetime import timedelta
from dataclasses import dataclass
import aiohttp
timeout_seconds = timedelta(seconds=15).total_seconds()


@dataclass
class Payload:
    data: str


@dataclass
class Address:
    recipient: str


@dataclass
class Event:
    recipients: List[Address]
    payload: Payload


class Result(Enum):
    Accepted = 1
    Rejected = 2


async def read_data() -> Event:
    await asyncio.sleep(1)
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/') as response:
            data = await response.json()
    return Event(recipients=data['recipients'], payload=data['payload'])


async def send_data(dest: Address, payload: Payload) -> Result:
    async with aiohttp.ClientSession() as session:
        async with session.post(dest, data= payload) as response:
            response_data = await response.text()
            return Result(int(response_data))


async def perform_operation() -> None:
    while True:
        event = await read_data()
        tasks = []
        for recipient in event.recipients:
            task = asyncio.create_task(send_data(dest=recipient, payload=event.payload))
            tasks.append(task)

        results = await asyncio.gather(*tasks)

        for result in results:
            if result == Result.Rejected:
                # Повторная попытка отправки данных
                print("Sending data rejected, retrying...")
                await asyncio.sleep(1)  # Ожидание перед повторной попыткой
            else:
                print("Data sent successfully")


asyncio.run(perform_operation())