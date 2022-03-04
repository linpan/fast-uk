import asyncio
import random
import time

import aiohttp
from pydantic import BaseModel
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from qa import qa
from sse_starlette.sse import EventSourceResponse

app = FastAPI()
BASE_URL = 'http://120.92.91.137:3000/agent/xiaodai/query_plain_qa'

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def numbers(minimum, maximum):
    for i in range(minimum, maximum + 1):
        await asyncio.sleep(random.randint(3, 18))
        yield '{"bot": false, "message": "我是清华大学的虚拟学生华智", "id": "2"}'


@app.get("/qa", summary="qa list")
async def qa_list():
    return qa[:10]


@app.get('/status/stream')
async def runStatus(request: Request):
    event_generator = numbers(1, 100)
    return EventSourceResponse(event_generator)


class BotModel(BaseModel):
    query: str = "美国漫威漫画公司旗下超级英雄"


@app.post("/bot", summary="bot回复")
async def bot(item: BotModel):
    async with aiohttp.ClientSession() as session:
        body = {"query": item.query,
                "appname": "xdai_siemens",
                "history": [],
                "suggested_qa": [],
                "injected_desc": ""
                }
        headers = {
            'Authorization': 'U8QAAHsp3SuTL1GJmuGKS6UM-8Mt1bdVlkc134w0jio'
        }
        async with session.post(BASE_URL, json=body, headers=headers, timeout=6.5) as resp:
            if resp.status == 200:
                reply = await resp.json()
                return reply['data']['reply']
            else:
                return "我....."
