from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    group = Column(String, index=True)
    desc = Column(String)

    codes = relationship("Code", back_populates="device")


class Code(Base):
    __tablename__ = "codes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    code = Column(String)
    desc = Column(String)

    device = relationship("Device", back_populates="codes")
