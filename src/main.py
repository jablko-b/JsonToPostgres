"""
The main module of the Weight-in-Motion (WIM) data processing application. 

This module initializes and manages the components necessary for the application's operation,
including the simulated WIM server, API client for data retrieval, data transformation, and database management.
It orchestrates the process of fetching data from the server, transforming it, and inserting it into the database.
"""
from utils.api_client import APIClient
from database.data_processor import DataTransformer
from database.database import DatabaseManager
from WIMRestfulServer.wim_restful_server import WeightInMotionServer
import config.wim_server_config as wim_config
import time
import threading


class WIMDataProcessingApp:
    """
    This class encapsulates the main application logic for the WIM data processing application.
    """

    def __init__(self):
        """
        Initializes the WIMDataProcessingApp with the components required to process data.
        """
        self.server = WeightInMotionServer()
        self.api_client = APIClient(base_url=wim_config.RESTAPI_BASE_URL)
        self.transformer = DataTransformer()
        self.db_manager = DatabaseManager()
        self.last_current_id = None
        self.max_retries = 10
        self.retry_delay = 5

    def is_server_running(self):
        """Checks if the WIM server is running by making a request 
        to the /health endpoint and validating the response."""
        
        response = self.api_client.fetch_data("health")
        return response and response.get("status") == "OK"

    def start_server(self):
        """Starts the WIM server in a separate thread.

        Spawns a new thread to run the WIM server, marks it as a daemon thread so it does not block program exit,
        and starts the thread. Returns a handle to the thread.
        """
        server_thread = threading.Thread(
            target=lambda: self.server.run(wim_config.FLASK_PORT)
        )
        server_thread.daemon = True
        server_thread.start()
        return server_thread

    def run(self):
        """
        Start and manage the Weight In Motion (WIM) data processing application.

        This method performs the following steps:
        - Starts the WIM server on a separate thread.
        - Continuously checks for the server's health status until it's running.
        - Initiates the process of creating the necessary database tables.
        - Enters a loop to fetch, transform, and insert data from the WIM server into the database.
        This loop also handles exceptions and retries based on defined maximum retries and delay.

        The method handles two types of exceptions:
        - General exceptions during data fetching, processing, or insertion,
        with a retry mechanism implemented.
        - KeyboardInterrupt for graceful shutdown on user interruption.

        The loop for fetching and processing data continues until either the maximum number of retries
        is reached after consecutive failures or the program is manually interrupted by the user.
        """
        self.start_server()

        while not self.is_server_running():
            print("WIM App: Waiting for wim server to start...")
            time.sleep(1)

        print("WIM App: Server started. Now starting the main application...")
        self.db_manager.create_tables()

        retries = self.max_retries
        while retries > 0:
            try:
                self.fetch_and_process_data()
            except Exception as e:
                print(f"Error fetching data: {e}")
                if retries > 0:
                    print(f"WIM App: Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                    retries -= 1
                else:
                    print("WIM App: Maximum retries reached. Exiting.")
                    break
            except KeyboardInterrupt:
                print("WIM App: Program interrupted by user")
                break

    def fetch_and_process_data(self):
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

        print("WIM App: Fetching data from the WIM server...")
        json_data = self.api_client.fetch_data("data")

        current_id = json_data.get("id")
        if current_id != self.last_current_id:
            print(f"WIM App: New data found. Transforming data with current ID: {current_id}")

            transformed_data = self.transformer.transform_data(json_data)

            print("WIM App: Inserting data to database...")
            self.db_manager.insert_data(transformed_data)

            self.last_current_id = current_id
        else:
            print(f"WIM App: No new data, skipping database insertion. Current ID: {current_id}")

        time.sleep(5)


if __name__ == "__main__":
    app = WIMDataProcessingApp()
    app.run()
