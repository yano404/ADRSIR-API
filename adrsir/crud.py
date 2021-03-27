from sqlalchemy.orm import Session

from . import models, schemas


def get_device(db: Session, device_id: int):
    """
    Get Device by ID
    """
    return db.query(models.Device).filter(models.Device.id == device_id).first()


def get_devices(db: Session, skip: int = 0, limit: int = 100):
    """
    Get Device list (default: up to 100 devices)
    """
    return db.query(models.Device).offset(skip).limit(limit).all()


def get_devices_by_name(db: Session, name: str):
    """
    Get Device by Name
    """
    return db.query(models.Device).filter(models.Device.name == name).all()


def get_devices_by_group(db: Session, group: str, skip: int = 0, limit: int = 100):
    """
    Get Devices by Group
    """
    return (
        db.query(models.Device)
        .filter(models.Device.group == group)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_groups(db: Session):
    """
    Get Groups
    """
    groups = db.query(models.Device.group).all()
    return list(set(groups))


def create_device(db: Session, device: schemas.DeviceCreate):
    """
    Create Device
    """
    db_device = models.Device(**device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


def update_device(db: Session, device_id: int, device: schemas.DeviceUpdate):
    """
    Update Device Info
    """
    db_device = db.query(models.Device).filter(models.Device.id == device_id).one()
    db_device.name = device.name
    db_device.group = device.group
    db_device.desc = device.desc
    db.commit()
    return db.query(models.Device).filter(models.Device.id == device_id).first()


def delete_device(db: Session, device_id: int):
    """
    Delete Device by ID
    """
    # Delete all codes od the device
    target_codes = (
        db.query(models.Code).filter(models.Code.device_id == device_id).all()
    )
    for code in target_codes:
        db.delete(target_codes)
        db.commit()
    # Delete Device
    target_device = db.query(models.Device).filter(models.Device.id == device_id).one()
    db.delete(target_device)
    db.commit()

    return target_device


def get_code(db: Session, code_id: int):
    """
    Get Code by ID
    """
    return db.query(models.Code).filter(models.Code.id == code_id).first()


def get_code_by_code_str(db: Session, code_str: str):
    """
    Get Code by code string
    """
    return db.query(models.Code).filter(models.Code.code == code_str).first()


def get_codes(db: Session, skip: int = 0, limit: int = 1000):
    """
    Get Codes list (default: up to 1000)
    """
    return db.query(models.Code).offset(skip).limit(limit).all()


def get_codes_of_device(db: Session, device_id: int):
    """
    Get Codes list of Device
    """
    return db.query(models.Code).filter(models.Code.device_id == device_id).all()


def get_code_of_device(db: Session, device_id: int, code_id: int):
    """
    Get Code of Device
    """
    return (
        db.query(models.Code)
        .filter(models.Code.device_id == device_id)
        .filter(models.Code.id == code_id)
        .first()
    )


def create_code(db: Session, code: schemas.CodeCreate):
    """
    Create Code
    """
    db_code = models.Code(**code.dict())
    db.add(db_code)
    db.commit()
    db.refresh(db_code)
    return db_code


def update_code(db: Session, code_id: int, code: schemas.CodeUpdate):
    """
    Update Code
    """
    db_code = db.query(models.Code).filter(models.Code.id == code_id).one()
    db_code.name = code.name
    db_code.device_id = code.device_id
    db_code.code = code.code
    db_code.desc = code.desc
    db.commit()
    return db.query(models.Code).filter(models.Code.id == code_id).first()


def delete_code(db: Session, code_id: int):
    """
    Delete Code
    """
    target_code = db.query(models.Code).filter(models.Code.id == code_id).one()
    db.delete(target_code)
    db.commit()
    return target_code


def delete_code_of_device(db: Session, device_id: int, code_id: int):
    """
    Delete Code
    """
    target_code = (
        db.query(models.Code)
        .filter(models.Code.device_id == device_id)
        .filter(models.Code.id == code_id)
        .one()
    )
    db.delete(target_code)
    db.commit()
    return target_code
