"""
This module implements a simplistic Flask server simulating part of the data from a weight-in-motion (WIM) station. 
It provides functionalities for generating simulated sensor data, persisting the measurement ID,
and serving the data through a REST API. The server periodically updates sensor data, mimicking 
real-time measurements from a WIM system. 

The simulated data includes axle weights, gross weights, and other related measurements, 
structured in a predefined JSON format. Persistence of measurement IDs is achieved using file-based 
storage to maintain state between server restarts.
"""

from flask import Flask, jsonify
import time
from datetime import datetime
from config.wim_server_config import FLASK_PORT
import threading
import random
import os


class WeightInMotionServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.id_lock = threading.Lock()

        self.current_id = 0
        self.current_pkMeasurement = 0
        self.timestamp = 0
        self.gross_weight = 0
        self.gross_left_weight = 0
        self.gross_right_weight = 0

        self.weight_gid0 = 0
        self.left_wheel_weight_gid0 = 0
        self.right_wheel_weight_gid0 = 0

        self.weight_gid1 = 0
        self.left_wheel_weight_gid1 = 0
        self.right_wheel_weight_gid1 = 0
        self.weight_gid1_2 = 0
        self.left_wheel_weight_gid1_2 = 0
        self.right_wheel_weight_gid1_2 = 0

        self.weight_gid2 = 0
        self.left_wheel_weight_gid2 = 0
        self.right_wheel_weight_gid2 = 0
        self.weight_gid2_2 = 0
        self.left_wheel_weight_gid2_2 = 0
        self.right_wheel_weight_gid2_2 = 0

        self.setup_routes()

        # File to store the current_id
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.id_file = os.path.join(base_dir, "measurementID.cfg")

    def save_current_id(self):
        """
        Save the current measurement ID to a file.

        This method takes the current measurement ID and writes it to a file to persist the state.
        The measurement ID represents the unique identifier for the latest sensor data measurement.
        It is for maintaining continuity in the simulated data flow.

        Args:
        current_id (int): The current measurement ID to be saved.

        Raises:
        PermissionError: If there are permission issues while writing to the file.
        IOError: If there are any input/output errors during the file write operation.

        Note:
        Proper error handling should be implemented to handle potential issues when saving the
        measurement ID to the file. Ensure that the file path for storing the measurement ID is
        accessible and writable.
        """
        # Acquiring lock to ensure thread-safe access to the file
        with self.id_lock:
            try:
                # Writing the current ID to the file
                with open(self.id_file, "w") as file:
                    file.write(str(self.current_id))
            except Exception as e:
                print("Error while saving current ID: {}".format(e))

    def load_current_id(self):
        """
        Load the current measurement ID from a persisted file.

        This method reads the current measurement ID from a file where it was previously saved. The
        measurement ID represents the unique identifier for the latest sensor data measurement. It
        is used to maintain continuity in the simulated data flow.

        Returns:
        int: The current measurement ID read from the file.

        Raises:
        FileNotFoundError: If the file containing the current measurement ID does not exist.
        ValueError: If the content of the file is not a valid integer.

        Note:
        It's important to ensure that the file path for storing the measurement ID exists and is
        accessible. Proper exception handling should be used to address any potential issues when
        loading the measurement ID.
        """
        # Acquiring lock to ensure thread-safe access to the file
        with self.id_lock:
            try:
                if not os.path.exists(self.id_file):
                    # The file does not exist, create it and initialize the ID to 0
                    with open(self.id_file, "w") as file:
                        file.write("0")

                # At this point, the file exists, either from before or newly created
                with open(self.id_file, "r") as file:
                    return int(file.read())

            except Exception as e:
                print(f"Error while loading current ID: {e}")
                return 0

    def update_data(self):
        """
        Periodically updates the simulated sensor data.

        This method simulates the process of receiving new sensor data from a WIM station by
        periodically generating random values for various measurements. It updates variables
        representing sensor data, such as axle weights and vehicle velocities. The method also
        increments and persists the current measurement ID to simulate continuous data flow.

        This is a long-running method intended to be run in a background thread. It has an internal
        loop that waits for a predefined interval (defined by `time_to_wait`) between updates,
        simulating real-time data collection.

        Exception Handling:
        - KeyboardInterrupt: Catches and logs a message when the update process is interrupted by the user.

        Side Effects:
        - Modifies global state by updating sensor data variables.
        - Writes to a file to persist the current measurement ID.
        - Prints to the console each time new data is generated and when the thread is sleeping or waking up.

        Returns:
        None: As a procedure meant for continuous execution in a background thread, it does not return a value.

        Note:
        This method should be carefully managed to ensure that it does not conflict with other parts of the
        application that read sensor data, particularly regarding thread safety and synchronization.
        """

        try:
            while True:
                self.current_id = self.load_current_id()
                self.current_id += 1
                print(f"WIM Server: Update data...Current ID: {self.current_id}")
                self.save_current_id()
                self.current_pkMeasurement = self.current_id
                # Generate the timestamp in the desired format
                # Current time as a datetime object
                now = datetime.now()
                # ISO format string
                # Convert to Unix timestamp
                self.timestamp = int(now.timestamp())
                self.time_iso_format = now.isoformat()

                self.left_wheel_weight_gid0 = random.randint(2000, 2300)
                self.right_wheel_weight_gid0 = random.randint(2000, 2300)
                self.weight_gid0 = (
                    self.left_wheel_weight_gid0 + self.right_wheel_weight_gid0
                )

                self.left_wheel_weight_gid1 = random.randint(2400, 2600)
                self.right_wheel_weight_gid1 = random.randint(2400, 2600)
                self.weight_gid1 = (
                    self.left_wheel_weight_gid1 + self.right_wheel_weight_gid1
                )

                self.left_wheel_weight_gid1_2 = random.randint(2400, 2600)
                self.right_wheel_weight_gid1_2 = random.randint(2400, 2600)
                self.weight_gid1_2 = (
                    self.left_wheel_weight_gid1_2 + self.right_wheel_weight_gid1_2
                )

                self.left_wheel_weight_gid2 = random.randint(2400, 2600)
                self.right_wheel_weight_gid2 = random.randint(2400, 2600)
                self.weight_gid2 = (
                    self.left_wheel_weight_gid2 + self.right_wheel_weight_gid2
                )

                self.left_wheel_weight_gid2_2 = random.randint(2400, 2600)
                self.right_wheel_weight_gid2_2 = random.randint(2400, 2600)
                self.weight_gid2_2 = (
                    self.left_wheel_weight_gid2_2 + self.right_wheel_weight_gid2_2
                )

                self.gross_left_weight = (
                    self.left_wheel_weight_gid0
                    + self.left_wheel_weight_gid1
                    + self.left_wheel_weight_gid1_2
                    + self.left_wheel_weight_gid2
                    + self.left_wheel_weight_gid2_2
                )
                self.gross_right_weight = (
                    self.right_wheel_weight_gid0
                    + self.right_wheel_weight_gid1
                    + self.right_wheel_weight_gid1_2
                    + self.right_wheel_weight_gid2
                    + self.right_wheel_weight_gid2_2
                )
                self.gross_weight = self.gross_left_weight + self.gross_right_weight

                with self.app.test_request_context():
                    response = self.get_data()
                    # Converting the response object to a string
                    data_str = response.get_data(as_text=True)
                    #print(data_str)

                #print(f"Sleeping at: {datetime.now()}")
                time_to_wait = 6  # random.randint(5, 10)
                time.sleep(time_to_wait)
                #print(f"Woke up at: {datetime.now()}")
        except KeyboardInterrupt:
            print("WIM Server: Program interrupted by user, closing RESTful server")
        finally:
            print("WIM Server: Closing RESTful server")

    def setup_routes(self):
        """
        Configures the URL routes for the Flask server.

        This method defines the endpoints for the server's RESTful API, mapping URL patterns
        to the functions that should be executed when these endpoints are requested. It includes
        routes for fetching data and performing health checks on the server.

        Endpoints:
        - '/data': Handles GET requests to retrieve the latest WIM data.
        - '/health': Handles GET requests for server health checks and returns a status message.

        The functions associated with these endpoints are defined within the scope of this method.

        Side Effects:
        - Modifies the Flask app instance by adding URL rules.
        - Establishes view functions that will be called when the endpoints are accessed.

        Raises:
        - AssertionError: If a route is defined with invalid parameters, Flask raises an assertion error.

        Returns:
        None: This method modifies the Flask app's state by setting up routes but does not return a value.
        """
        @self.app.route("/data", methods=["GET"])
        def get_data_route():
            return self.get_data()
        @self.app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({"status": "OK"}), 200


    def get_data(self):
        """
        Retrieves the latest WIM sensor data in JSON format.

        This method constructs a JSON object representing the current state of the WIM sensor data.
        It includes details such as measurement ID, timestamp, axle weights, vehicle velocities,
        and other relevant metrics. The data is structured to conform with the expected schema for
        client applications consuming this API.

        The method ensures that the data reflects the most recent readings from the simulated WIM sensors.
        It's typically called internally when the '/data' endpoint of the server is accessed.

        Returns:
        flask.Response: A Flask response object containing the JSON data and a 200 HTTP status code,
        making it ready for HTTP transmission.

        Note:
        This method is intended to be used as an endpoint for an HTTP GET request and should be
        bound to a route using Flask's routing mechanism. It does not handle any request parameters
        and will always return the current state of the server's simulated data.
        """

        # Constructing the response JSON object with current sensor data
        data = {
            "pkMeasurement": self.current_pkMeasurement,
            "id": str(self.current_id),
            "timestamp": self.time_iso_format,
            "vdRs": [
                {
                    "source": "WIM DL",
                    "data": {
                        "ID": 2576333,
                        "MetrologicalID": "0x13844B5D",
                        "LaneNo": 1,
                        "LaneName": "Lane_1",
                        "ErrorFlag": 0,
                        "WarningFlag": 0,
                        "Direction": 0,
                        "MoveStatus": -1,
                        "FrontToFront": 5.731,
                        "BackToFront": 4.478,
                        "FrontOverhang": 0,
                        "Duration": 2.175,
                        "VehicleLength": 25.13,
                        "GrossWeight": self.gross_weight,
                        "LeftWeight": self.gross_left_weight,
                        "RightWeight": self.gross_right_weight,
                        "Velocity": 53.40000000000001,
                        "WheelBase": 18.5,
                        "AxlesCount": 5,
                        "MassUnit": "kg",
                        "VelocityUnit": "km/h",
                        "DistanceUnit": "m",
                        "Axles": [
                            {
                                "ID": 12339142,
                                "GroupID": 0,
                                "Velocity": 53.5,
                                "Weight": self.weight_gid0,
                                "LeftWheelWeight": self.left_wheel_weight_gid0,
                                "RightWheelWeight": self.right_wheel_weight_gid0,
                                "LeftRightImbalance": 52.19298245614035,
                                "Distance": 0,
                                "Track": 0,
                                "PatchLengthRight": 0.16,
                                "PatchLengthLeft": 0.18,
                                "PatchWidthRight": 0,
                                "PatchWidthLeft": 0,
                                "PositionRight": 0,
                                "PositionLeft": 0,
                                "SDTireRight": "N",
                                "SDTireLeft": "N",
                                "TireStatusRight": "N/A",
                                "TireStatusLeft": "N/A",
                            },
                            {
                                "ID": 12339143,
                                "GroupID": 1,
                                "Velocity": 53.6,
                                "Weight": self.weight_gid1,
                                "LeftWheelWeight": self.left_wheel_weight_gid1,
                                "RightWheelWeight": self.right_wheel_weight_gid1,
                                "LeftRightImbalance": 50.80321285140563,
                                "Distance": 5.59,
                                "Track": 0,
                                "PatchLengthRight": 0.13,
                                "PatchLengthLeft": 0.16,
                                "PatchWidthRight": 0,
                                "PatchWidthLeft": 0,
                                "PositionRight": 0,
                                "PositionLeft": 0,
                                "SDTireRight": "N",
                                "SDTireLeft": "N",
                                "TireStatusRight": "N/A",
                                "TireStatusLeft": "N/A",
                            },
                            {
                                "ID": 12339144,
                                "GroupID": 1,
                                "Velocity": 53.6,
                                "Weight": self.weight_gid1_2,
                                "LeftWheelWeight": self.left_wheel_weight_gid1_2,
                                "RightWheelWeight": self.right_wheel_weight_gid1_2,
                                "LeftRightImbalance": 49.38775510204081,
                                "Distance": 1.27,
                                "Track": 0,
                                "PatchLengthRight": 0.14,
                                "PatchLengthLeft": 0.15,
                                "PatchWidthRight": 0,
                                "PatchWidthLeft": 0,
                                "PositionRight": 0,
                                "PositionLeft": 0,
                                "SDTireRight": "N",
                                "SDTireLeft": "N",
                                "TireStatusRight": "N/A",
                                "TireStatusLeft": "N/A",
                            },
                            {
                                "ID": 12339145,
                                "GroupID": 2,
                                "Velocity": 53.2,
                                "Weight": self.weight_gid2,
                                "LeftWheelWeight": self.left_wheel_weight_gid2,
                                "RightWheelWeight": self.right_wheel_weight_gid2,
                                "LeftRightImbalance": 50.86805555555556,
                                "Distance": 10.43,
                                "Track": 0,
                                "PatchLengthRight": 0.15,
                                "PatchLengthLeft": 0.18,
                                "PatchWidthRight": 0,
                                "PatchWidthLeft": 0,
                                "PositionRight": 0,
                                "PositionLeft": 0,
                                "SDTireRight": "N",
                                "SDTireLeft": "N",
                                "TireStatusRight": "N/A",
                                "TireStatusLeft": "N/A",
                            },
                            {
                                "ID": 12339146,
                                "GroupID": 2,
                                "Velocity": 53.1,
                                "Weight": self.weight_gid2_2,
                                "LeftWheelWeight": self.left_wheel_weight_gid2_2,
                                "RightWheelWeight": self.right_wheel_weight_gid2_2,
                                "LeftRightImbalance": 48.01381692573403,
                                "Distance": 1.21,
                                "Track": 0,
                                "PatchLengthRight": 0.17,
                                "PatchLengthLeft": 0.17,
                                "PatchWidthRight": 0,
                                "PatchWidthLeft": 0,
                                "PositionRight": 0,
                                "PositionLeft": 0,
                                "SDTireRight": "N",
                                "SDTireLeft": "N",
                                "TireStatusRight": "N/A",
                                "TireStatusLeft": "N/A",
                            },
                        ],
                        "Marked": False,
                        "MarkedViolations": False,
                        "VehicleID": "",
                        "StartTime": self.timestamp,
                        "StartTimeStr": self.time_iso_format,
                        "StartTimeFirstAxleFirstSensor": "1638457729376",
                        "StartTimeFirstAxleFirstSensorStr": "2021-12-02T16:08:49.376+01:00",
                        "StartTimeFirstAxleLastSensor": "1638457729442",
                        "StartTimeFirstAxleLastSensorStr": "2021-12-02T16:08:49.442+01:00",
                        "StartTimeLastAxleFirstSensor": "1638457730621",
                        "StartTimeLastAxleFirstSensorStr": "2021-12-02T16:08:50.621+01:00",
                        "StartTimeLastAxleLastSensor": "1638457730689",
                        "StartTimeLastAxleLastSensorStr": "2021-12-02T16:08:50.689+01:00",
                        "StartTimeFirstPresenceRise": "1638457729150",
                        "StartTimeFirstPresenceRiseStr": "2021-12-02T16:08:49.15+01:00",
                        "StartTimeFirstPresenceFall": "1638457730909",
                        "StartTimeFirstPresenceFallStr": "2021-12-02T16:08:50.909+01:00",
                        "StartTimeLastPresenceRise": "1638457729551",
                        "StartTimeLastPresenceRiseStr": "2021-12-02T16:08:49.551+01:00",
                        "StartTimeLastPresenceFall": "1638457731325",
                        "StartTimeLastPresenceFallStr": "2021-12-02T16:08:51.325+01:00",
                        "SelectedSchemaName": "AUSTROADS",
                        "MappedClassCategoryID": "13",
                        "InternalBaseClassID": 1,
                        "TimeSyncStatus": "ntp-sync",
                    },
                }
            ],
        }

        return jsonify(data)

    def run(self, port=5000):
        update_thread = threading.Thread(target=self.update_data, daemon=True)
        update_thread.start()
        self.app.run(debug=False, port=port)


if __name__ == "__main__":
    server = WeightInMotionServer()
    server.run(port=FLASK_PORT)
