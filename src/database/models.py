"""
This module defines the SQLAlchemy ORM models for the Weight-in-Motion (WIM) application. 

It creates a structured representation of the database tables and their relationships,
enabling the application to interact with the database in an object-oriented manner.
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean, BigInteger
from sqlalchemy.orm import relationship

Base = declarative_base()

class Measurement(Base):
    """
    Represents the 'measurements' table in the database.
    
    Each instance of this class corresponds to a row in the 'measurements' table.
    """
    __tablename__ = 'measurements'

    pkMeasurement = Column(Integer, primary_key=True)
    id = Column(Integer)
    timestamp = Column(DateTime)

    # Relationship to VDRs
    vdrs = relationship("VDR", back_populates="measurement")

class VDR(Base):
    """
    Represents the 'vdr' table in the database.
    
    Each instance of this class corresponds to a row in the 'vdr' table.
    """
    __tablename__ = 'vdrs'

    vdr_id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String)
    measurement_id = Column(Integer, ForeignKey('measurements.pkMeasurement'))
    MetrologicalID = Column(String)
    LaneNo = Column(Integer)
    ErrorFlag = Column(Integer)
    WarningFlag = Column(Integer)
    Direction = Column(Integer)
    MoveStatus = Column(Integer)
    FrontToFront = Column(Float)
    BackToFront = Column(Float)
    FrontOverhang = Column(Float)
    Duration = Column(Float)
    VehicleLength = Column(Float)
    GrossWeight = Column(Integer)
    LeftWeight = Column(Integer)
    RightWeight = Column(Integer)
    Velocity = Column(Float)
    WheelBase = Column(Float)
    AxlesCount = Column(Integer)
    MassUnit = Column(String)
    VelocityUnit = Column(String)
    DistanceUnit = Column(String)
    Marked = Column(Boolean)
    MarkedViolations = Column(Boolean)
    VehicleID = Column(String)
    StartTime = Column(BigInteger)
    StartTimeStr = Column(String)
    
    # Relationship to Measurements
    measurement = relationship("Measurement", back_populates="vdrs")
    # Relationship to Axles
    axles = relationship("Axle", back_populates="vdr")

class Axle(Base):
    """
    Represents the 'axle' table in the database.
    
    Each instance of this class corresponds to a row in the 'axle' table.
    """

    __tablename__ = 'axles'

    axle_id = Column(Integer, primary_key=True, autoincrement=True)
    vdr_id = Column(Integer, ForeignKey('vdrs.vdr_id'))
    ID = Column(Integer)
    GroupID = Column(Integer)
    Velocity = Column(Float)
    Weight = Column(Integer)
    LeftWheelWeight = Column(Integer)
    RightWheelWeight = Column(Integer)
    LeftRightImbalance = Column(Float)
    Distance = Column(Float)
    Track = Column(Integer)
    PatchLengthRight = Column(Float)
    PatchLengthLeft = Column(Float)
    PatchWidthRight = Column(Float)
    PatchWidthLeft = Column(Float)
    PositionRight = Column(Float)
    PositionLeft = Column(Float)
    SDTireRight = Column(String(1))
    SDTireLeft = Column(String(1))
    TireStatusRight = Column(String)
    TireStatusLeft = Column(String)

    # Relationship to VDRs
    vdr = relationship("VDR", back_populates="axles")