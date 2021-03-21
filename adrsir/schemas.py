from typing import List, Optional

from pydantic import BaseModel, Field


class CodeBase(BaseModel):
    name: str
    code: str = Field(..., regex=r"^[0-9A-Fa-f]+$")
    desc: Optional[str] = None


class CodeCreate(CodeBase):
    device_id: int


class CodeUpdate(CodeBase):
    device_id: int


class CodeUpdateDevice(CodeBase):
    pass


class Code(CodeBase):
    id: int
    device_id: int

    class Config:
        orm_mode = True


class DeviceBase(BaseModel):
    name: str
    group: str
    desc: Optional[str] = None


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(DeviceBase):
    pass


class Device(DeviceBase):
    id: int
    codes: List[Code] = []

    class Config:
        orm_mode = True
