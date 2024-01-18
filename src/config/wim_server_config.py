# Port configuration for the Flask server and the RESTful services
FLASK_PORT = 5000  # Or any other port of your choice

# API configuration
RESTAPI_BASE_URL = "http://localhost:{port}/".format(port=FLASK_PORT)
RESTAPI_DATA_URL = "http://localhost:{port}/data".format(port=FLASK_PORT)
RESTAPI_STATUS_URL = "http://localhost:{port}/health".format(port=FLASK_PORT)