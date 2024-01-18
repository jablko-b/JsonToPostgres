"""
This module contains the DatabaseManager class that handles all database operations for the WIM application.

It is responsible for setting up the database connection, creating tables, and managing the insertion of data.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.database_config import DB_URI
from .models import Base, Measurement, VDR, Axle


class DatabaseManager:
    """
    Manages database interactions, encapsulating connection handling, session management,
    and transaction control to ensure data integrity.
    """

    def __init__(self):
        """
        Initializes the DatabaseManager with a connection to the specified database.
        """
        self.engine = create_engine(DB_URI)
        self.Session = sessionmaker(bind=self.engine)
    
    def create_tables(self):
        """Creates all tables defined in the Base model in the database."""
        Base.metadata.create_all(self.engine)

    def insert_data(self, transformed_data):
        """
        Inserts transformed data into the database within a session.

        The method begins a transaction and attempts to insert data into the 'measurements',
        'vdrs', and 'axles' tables based on the structured data provided. If an exception occurs
        during the insertion process, the transaction is rolled back to ensure data integrity.

        Parameters:
        transformed_data (tuple): A tuple containing three elements: a list of measurement data,
        a list of vehicle data recorder (VDR) entries, and a list of axle data.
        Each list contains tuples representing the rows to be inserted into their respective tables.
        
        Raises:
        Exception: Propagates any exceptions that occur during database operations after rolling back
        the session to ensure no partial data is committed.

        Returns:
        None: This method does not return any value. It either successfully commits the data to the database
        or raises an exception.
        """
        session = self.Session()
        try:
            measurements_data, vdrs_data, axles_data = transformed_data

            # Insert Measurements
            for m_data in measurements_data:
                measurement = Measurement(
                    pkMeasurement=m_data[0], id=m_data[1], timestamp=m_data[2]
                )
                session.add(measurement)
            session.commit()

            # Debug prints for VDR and Axle data
            #print("VDR Data:", vdrs_data)

            for vdr_data in vdrs_data:
                vdr = VDR(
                    source=vdr_data[0],
                    measurement_id=vdr_data[1],
                    MetrologicalID=vdr_data[2],
                    LaneNo=vdr_data[3],
                    ErrorFlag=vdr_data[4],
                    WarningFlag=vdr_data[5],
                    Direction=vdr_data[6],
                    MoveStatus=vdr_data[7],
                    FrontToFront=vdr_data[8],
                    BackToFront=vdr_data[9],
                    FrontOverhang=vdr_data[10],
                    Duration=vdr_data[11],
                    VehicleLength=vdr_data[12],
                    GrossWeight=vdr_data[13],
                    LeftWeight=vdr_data[14],
                    RightWeight=vdr_data[15],
                    Velocity=vdr_data[16],
                    WheelBase=vdr_data[17],
                    AxlesCount=vdr_data[18],
                    MassUnit=vdr_data[19],
                    VelocityUnit=vdr_data[20],
                    DistanceUnit=vdr_data[21],
                    Marked=vdr_data[22],
                    MarkedViolations=vdr_data[23],
                    VehicleID=vdr_data[24],
                    StartTime=vdr_data[25],
                    StartTimeStr=vdr_data[26],
                )
                session.add(vdr)
                session.flush()  # This will generate vdr_id

                # Insert Axles with correct vdr_id
                for axle_data in axles_data:
                    axle = Axle(
                        vdr_id=vdr.vdr_id,
                        ID=axle_data[1],
                        GroupID=axle_data[2],
                        Velocity=axle_data[3],
                        Weight=axle_data[4],
                        LeftWheelWeight=axle_data[5],
                        RightWheelWeight=axle_data[6],
                        LeftRightImbalance=axle_data[7],
                        Distance=axle_data[8],
                        Track=axle_data[9],
                        PatchLengthRight=axle_data[10],
                        PatchLengthLeft=axle_data[11],
                        PatchWidthRight=axle_data[12],
                        PatchWidthLeft=axle_data[13],
                        PositionRight=axle_data[14],
                        PositionLeft=axle_data[15],
                        SDTireRight=axle_data[16],
                        SDTireLeft=axle_data[17],
                        TireStatusRight=axle_data[18],
                        TireStatusLeft=axle_data[19],
                    )
                    session.add(axle)

            session.commit()
            print("WIM App: Data inserted successfully")
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


