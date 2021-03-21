from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Path, Query
from sqlalchemy.orm import Session

from . import adrsir, crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
adrsir = adrsir.AdrsirCtrl()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
CRUD Device
===========
POST /devices             --> add device
GET  /devices/            --> list devices
GET  /devices/{device_id} --> show device info
PUT  /devices/            --> update device
DEL  /devices/{device_id} --> remove device and its codes
"""


@app.post("/devices/", response_model=schemas.Device)
def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    """
    Create Device
    """
    return crud.create_device(db=db, device=device)


@app.get("/devices/", response_model=List[schemas.Device])
def read_devices(
    skip: int = 0,
    limit: int = 100,
    group: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Get Devices
    """
    if group:
        devices = crud.get_devices_by_group(db=db, skip=skip, limit=limit, group=group)
    else:
        devices = crud.get_devices(db=db, skip=skip, limit=limit)
    return devices


@app.get("/devices/{device_id}", response_model=schemas.Device)
def read_device(device_id: int, db: Session = Depends(get_db)):
    """
    Get Device by ID
    """
    device = crud.get_device(db=db, device_id=device_id)
    return device


@app.put("/devices/", response_model=schemas.Device)
def update_device(device: schemas.DeviceUpdate, db: Session = Depends(get_db)):
    """
    Update Device
    """
    return crud.update_device(db=db, device=device)


@app.delete("/devices/{device_id}", response_model=schemas.Device)
def delete_device(device_id: int, db: Session = Depends(get_db)):
    """
    Delete Device
    """
    db_code = crud.get_codes_of_device(db=db, device_id=device_id)
    for code in db_code:
        crud.delete_code(db=db, code_id=code.id)
    return crud.delete_device(db=db, device_id=device_id)


@app.get("/groups/")
def read_groups(db: Session = Depends(get_db)):
    """
    Get Groups
    """
    return crud.get_groups(db=db)


"""
CRUD Code
"""


@app.post("/codes/", response_model=schemas.Code)
def create_code(code: schemas.CodeCreate, db: Session = Depends(get_db)):
    """
    Create Code
    """
    device = crud.get_device(db=db, device_id=code.device_id)
    if not device:
        raise HTTPException(status_code=400, detail="Device does NOT exist")

    db_code = crud.get_code_by_code_str(db=db, code_str=code.code)
    if db_code:
        raise HTTPException(status_code=400, detail="Code already registered")
    return crud.create_code(db=db, code=code)


@app.post("/devices/{device_id}/codes", response_model=schemas.Code)
def create_device_code(
    device_id: int, code: schemas.CodeBase, db: Session = Depends(get_db)
):
    """
    Create Code
    """
    device = crud.get_device(db=db, device_id=device_id)
    if not device:
        raise HTTPException(status_code=400, detail="Device does NOT exist")

    db_code = crud.get_code_by_code_str(db=db, code_str=code.code)
    if db_code:
        raise HTTPException(status_code=400, detail="Code already registered")

    code_dict = code.dict()
    code_dict.update({"device_id": device_id})
    return crud.create_code(db=db, code=schemas.CodeCreate(**code_dict))


@app.get("/codes/", response_model=List[schemas.Code])
def read_codes(
    skip: int = 0,
    limit: int = 1000,
    device_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """
    Get Codes
    """
    if device_id:
        codes = crud.get_codes_of_device(db=db, device_id=device_id)
    else:
        codes = crud.get_codes(db=db, skip=skip, limit=limit)
    return codes


@app.get("/codes/{code_id}", response_model=schemas.Code)
def read_code(
    code_id: int,
    db: Session = Depends(get_db),
):
    """
    Get Code
    """
    return crud.get_code(db=db, code_id=code_id)


@app.get("/devices/{device_id}/codes", response_model=List[schemas.Code])
def read_device_codes(device_id: int, db: Session = Depends(get_db)):
    """
    Get Codes
    """
    codes = crud.get_codes_of_device(db=db, device_id=device_id)
    return codes


@app.get("/devices/{device_id}/codes/{code_id}", response_model=schemas.Code)
def read_device_code(device_id: int, code_id: int, db: Session = Depends(get_db)):
    """
    Get Code
    """
    return crud.get_code_of_device(db=db, device_id=device_id, code_id=code_id)


@app.put("/codes/", response_model=schemas.Code)
def update_code(code: schemas.CodeUpdate, db: Session = Depends(get_db)):
    """
    Update Code
    """
    return crud.update_code(db=db, code=code)


@app.put("/devices/{device_id}/codes/", response_model=schemas.Code)
def update_device_code(
    device_id: int, code: schemas.CodeUpdateDevice, db: Session = Depends(get_db)
):
    """
    Update Code
    """
    db_code = crud.get_code_of_device(db=db, device_id=device_id, code_id=code.id)
    if not db_code:
        return None
    code_dict = code.dict()
    code_dict.update({"device_id": device_id})
    return crud.update_code(db=db, code=schemas.CodeUpdate(**code_dict))


@app.delete("/codes/{code_id}", response_model=schemas.Code)
def delete_code(code_id: int, db: Session = Depends(get_db)):
    """
    Delete Code
    """
    db_code = crud.get_code(db=db, code_id=code_id)
    if not db_code:
        # raise HTTPException(status_code=400, detail="Code does NOT exist")
        return None
    return crud.delete_code(db=db, code_id=code_id)


@app.delete("/devices/{device_id}/codes/{code_id}")
def delete_device_code(device_id: int, code_id: int, db: Session = Depends(get_db)):
    """
    Delete Code
    """
    db_code = crud.get_code_of_device(db=db, device_id=device_id, code_id=code_id)
    if not db_code:
        # raise HTTPException(status_code=400, detail="Code does NOT exist")
        return None
    return crud.delete_code(db=db, code_id=code_id)


"""
Read & Transmit the Code
"""


@app.get("/read/{mem_id}")
def read_mem(mem_id: int = Path(..., ge=0, le=9)):
    """
    Read the code
    """
    return {"mem_id": mem_id, "code": adrsir.read(mem_id)}


@app.post("/write/{mem_id}")
def write_mem(
    mem_id: int = Path(..., ge=0, le=9),
    code: str = Query(min_length=2, max_length=600, regex=r"^[0-9A-Fa-f]+$"),
):
    """
    Write the code to the memory
    """
    adrsir.write(mem_id, code)
    return {"mem_id": mem_id, "code": code}


@app.post("/transmit/")
def transmit(code: str = Query(min_length=2, max_length=600)):
    """
    Transmit the code
    """
    adrsir.transmit(code)
    return {"code": code}


@app.post("/codes/{code_id}/transmit")
def transmit_code(code_id: int):
    """
    Transmit the code
    """
    code = crud.get_code(code_id=code_id)
    adrsir.transmit(code.code)
    return {"device_id": code.device_id, "code_id": code.id}


@app.post("/devices/{device_id}/codes/{code_id}/transmit")
def transmit_device_code(device_id: int, code_id: int):
    """
    Transmit the code
    """
    code = crud.get_code_of_device(device_id=device_id, code_id=code_id)
    adrsir.transmit(code.code)
    return {"device_id": device_id, "code_id": code_id}
