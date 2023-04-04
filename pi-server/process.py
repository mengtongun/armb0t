from typing import Union

from fastapi import FastAPI
import arm_control as arm
import requests as req
import time
app = FastAPI()
piCameraServer = 'http://localhost:3002'


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
    arm.move_arm_bot(x, y, color)
    return {'msg': 'success'}


@app.get('/pick-red')
def pick_red():
    data = req.get(piCameraServer)
    rgby = data.json()
    print(rgby)
    if rgby['red'] is not None:
        isMoving = arm.move_arm_bot(rgby['red'][0], rgby['red'][1], 'red')
        if isMoving:
            return {'msg': 'success'}
        else:
            return {'msg': 'error'}
    else:
        return {'msg': 'color not found'}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("process:app", host="0.0.0.0",
                port=3001, reload=True, workers=1)
