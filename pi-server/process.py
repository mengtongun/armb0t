from fastapi.middleware.cors import CORSMiddleware
from typing import Union

from fastapi import FastAPI
import arm_control as arm
import requests as req
import time
app = FastAPI()
piCameraServer = 'http://localhost:3002'

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"msg": "Welcome To PI Server"}


@app.get('/engine-status')
def get_engine_status():
    isStarting = arm.move_to_base()
    if isStarting:
        return {'engine_status': 'starting'}
    else:
        return {'engine_status': 'error'}


@app.post('/to-base')
def to_base():
    isStarting = arm.move_to_base()
    if isStarting:
        return {'engine_status': 'starting'}
    else:
        return {'engine_status': 'error'}


@app.post('/move-arm-bot')
def move_arm_bot(x: int, y: int, color: str):
    isMoving = arm.move_arm_bot(x, y, color)
    if isMoving:
        return {'msg': 'isMoving'}
    else:
        return {'msg': 'error'}


@app.get('/pick-red')
def pick_red():
    data = req.get(piCameraServer)
    rgby = data.json()
    print(rgby)
    if rgby['red'] is not None:
        # isMoving = arm.move_arm_bot(rgby['red'][0], rgby['red'][1], 'red')
        isMoving = arm.pick_red_static()
        if isMoving:
            return {'msg': 'isMoving'}
        else:
            return {'msg': 'error'}
    else:
        return {'msg': 'color not found'}


@app.get('/red-bin')
def move_red_bin():
    isMoving = arm.move_to_red_bin()
    if isMoving:
        return {'msg': 'isMoving'}
    else:
        return {'msg': 'error'}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("process:app", host="0.0.0.0",
                port=3001, reload=True, workers=1)
