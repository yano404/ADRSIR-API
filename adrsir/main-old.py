from datetime import datetime
from typing import Optional

import uvicorn
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field


class Device(BaseModel):
    name: str
    group: str
    desc: Optional[str] = None


class Code(BaseModel):
    name: str
    code: str = Field(..., regex=r"^[0-9A-Fa-f]+$")
    desc: Optional[str] = None


app = FastAPI()


@app.get("/")
def index(name: str = "World"):
    return {"user": name, "message": f"Hello {name} !!"}


"""
Devices
=======
GET  /devices             --> list devices
GET  /devices/{device_id} --> show device info
POST /devices             --> add device
PUT  /devices/{device_id} --> update device
DEL  /devices/{device_id} --> remove device and its codes
"""


@app.get("/devices")
def list_device(query: str):
    return {"query": query}


@app.get("/devices/{device_id}")
def device_info(device_id: int):
    return {"id": device_id}


@app.post("/devices")
def add_device(device: Device):
    # give device_id
    device_id = int(datetime.now().timestamp())
    return {"device_id": device_id, "device": device}


@app.put("/devices/{device_id}")
def update_device(device_id: int, device: Device):
    return {"device_id": device_id, "device": device}


@app.delete("/devices/{device_id}")
def remove_device(device_id: int):
    return {"id": device_id}


"""
Codes
=====
GET  /devices/{device_id}/codes           --> list codes
GET  /devices/{device_id}/codes/{code_id} --> show code info
POST /devices/{device_id}/codes           --> add code
PUT  /devices/{device_id}/codes/{code_id} --> update code
DEL  /devices/{device_id}/codes/{code_id} --> remove code
"""


@app.get("/deveices/{device_id}/codes")
def list_code(device_id: int):
    return {"device_id": device_id}


@app.get("devices/{device_id}/codes/{code_id}")
def code_info(device_id: int, code_id: int):
    return {"device_id": device_id, "code_id": code_id}


@app.post("/devices/{device_id}/codes")
def add_code(device_id: int, code: Code):
    # give code_id
    code_id = int(datetime.now().timestamp())
    return {"device_id": device_id, "code_id": code_id, "code": code}


@app.put("/devices/{device_id}/codes/{code_id}")
def update_code(device_id: int, code_id: int, code: Code):
    return {"device_id": device_id, "code_id": code_id, "code": code}


@app.delete("/device/{device_id}/codes/{code_id}")
def remove_code(device_id: str, code_id: str):
    return {"device_id": device_id, "code_id": code_id}


# Transmit the code
@app.post("/devices/{device_id}/codes/{code_id}/transmit")
def transmit(device_id: int, code_id: int):
    return {"device_id": device_id, "code": code_id}


# read the code
@app.get("/read")
def read_mem(mem_id: int = Query(0, ge=0, le=9)):
    return {"mem_id": mem_id}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
