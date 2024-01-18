"""
The data_processor module contains the DataTransformer class, which converts the raw JSON data from the WIM server into a format that can be stored in the database.
"""

import json

class DataTransformer:
    """
    Transforms raw JSON data from the WIM server into structured data suitable for database storage.
    """
    def __init__(self):        
        pass

    def transform_data(self, json_data):
        """
        Transforms raw JSON data from the WIM server into structured data for database insertion.

        This method processes the JSON object by extracting relevant data for measurements,
        vehicle data recorders (VDRs), and axles. It organizes this data into tuples that
        align with the schema of the respective database tables.

        Parameters:
        json_data (dict): A dictionary containing the raw data from the WIM server. It is expected
        to have specific keys such as 'pkMeasurement', 'id', 'timestamp', and 'vdRs',
        where 'vdRs' is a list of dictionaries containing VDR data.

        Returns:
        tuple of (list, list, list): A 3-element tuple where the first element is a list of tuples
        for measurements, the second is a list of tuples for VDRs,
        and the third is a list of tuples for axles. Each tuple contains
        fields corresponding to the columns of the database tables.

        Raises:
        KeyError: If an expected key is missing in the JSON data.
        TypeError: If the data types of the values are not as expected (e.g., 'id' is not an integer).
        ValueError: If the data contains invalid values (e.g., a negative 'timestamp').

        Note:
        The method assumes that the JSON data structure adheres to the expected format provided by the WIM server.
        Any deviation from this format may result in exceptions or incorrect data transformations.
        """
        measurements_data = [
            (json_data["pkMeasurement"], json_data["id"], json_data["timestamp"])]

        vdrs_data = []
        axles_data = []

        for vdr in json_data["vdRs"]:
            vdr_data = vdr["data"]
            vdr_entry = (
                vdr["source"],
                # measurement_id (foreign key to Measurements)
                json_data["pkMeasurement"],
                vdr_data["MetrologicalID"],
                vdr_data["LaneNo"],
                vdr_data["ErrorFlag"],
                vdr_data["WarningFlag"],
                vdr_data["Direction"],
                vdr_data["MoveStatus"],
                vdr_data["FrontToFront"],
                vdr_data["BackToFront"],
                vdr_data["FrontOverhang"],
                vdr_data["Duration"],
                vdr_data["VehicleLength"],
                vdr_data["GrossWeight"],
                vdr_data["LeftWeight"],
                vdr_data["RightWeight"],
                vdr_data["Velocity"],
                vdr_data["WheelBase"],
                vdr_data["AxlesCount"],
                vdr_data["MassUnit"],
                vdr_data["VelocityUnit"],
                vdr_data["DistanceUnit"],
                vdr_data["Marked"],
                vdr_data["MarkedViolations"],
                vdr_data["VehicleID"],
                vdr_data["StartTime"],
                vdr_data["StartTimeStr"]
                # Add other fields if necessary
            )
            vdrs_data.append(vdr_entry)

            for axle in vdr_data["Axles"]:
                axle_entry = (
                    None,  # Placeholder for vdr_id (to be set later)
                    axle["ID"],
                    axle["GroupID"],
                    axle["Velocity"],
                    axle["Weight"],
                    axle["LeftWheelWeight"],
                    axle["RightWheelWeight"],
                    axle["LeftRightImbalance"],
                    axle["Distance"],
                    axle["Track"],
                    axle["PatchLengthRight"],
                    axle["PatchLengthLeft"],
                    axle["PatchWidthRight"],
                    axle["PatchWidthLeft"],
                    axle["PositionRight"],
                    axle["PositionLeft"],
                    axle["SDTireRight"],
                    axle["SDTireLeft"],
                    axle["TireStatusRight"],
                    axle["TireStatusLeft"]
                    # Add other fields if necessary
                )
                axles_data.append(axle_entry)

        return measurements_data, vdrs_data, axles_data