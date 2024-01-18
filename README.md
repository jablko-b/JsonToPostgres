# Weight-in-Motion (WIM) Data Processing Application

## Overview
This Weight-in-Motion (WIM) Data Processing Application, developed within GitHub Codespaces, is designed to simulate data processing within a WIM station from the sensor to the visualization layer. The application integrates a WIM server simulation, an API for data retrieval, data transformation, and database management. It includes a PostgreSQL database for data storage and a Grafana server for data visualization.

## GitHub Codespaces
This project is configured for development or use in GitHub Codespaces. To use this code:
1. Fork the project to your GitHub account.
2. Start the project as your own Codespace in GitHub.

The Codespace container includes a pre-configured PostgreSQL database and a Grafana server. Upon booting up, the container automatically installs Python dependencies from the `requirements.txt` file.

## Structure
The application is organized into several modules:
- `main.py`: Manages the application workflow and starts the WIM server on a separate thread.
- `WIMRestfulServer`: Contains the Flask server simulating WIM data.
- `utils`: Implements the API client for fetching data from the WIM server.
- `database`: Handles data transformation and database operations.
- `config`: Provides server and database configurations.
- `../test` : Provides test examples for the project code
- `../docs` : Allows for generating API documention using Sphinx

## Tools and Extensions

### SQLTools - Database Inspection
This project's Codespace is equipped with the SQLTools extension, which allows for convenient inspection and interaction with the database tables. SQLTools provides a user-friendly interface to query, visualize, and manage your database directly within the Codespace environment.

#### Using SQLTools
1. Open the SQLTools extension from the Vistual Studio Code left active bar in your Codespace.
2. Connect to the PostgreSQL database using the pre-configured connection settings. The created default database is called 'wim'. The default user is 'dev'. The default password is also 'dev'.
3. Explore the database schema, run queries, and inspect table records.

Note: You can also access the database from the terminal using the pre-installed psql tool.

### Grafana - Platform for data visualization and monitoring

### How to open Grafana
1. In the GitHub Codespace environment, locate the 'Ports' tab at the bottom pane.
2. Find the port on which Grafana is running (3000).
3. Hover over the row where Grafana's port is listed to reveal additional options.
4. Click on the globe icon (🌐) with the tooltip "Open in browser" to open Grafana in a new browser tab.
5. A new tab will open with the Grafana login page where you can log in with your credentials. Defaults are admin:admin

## Getting Started
### Prerequisites
- A GitHub account.

### Running the Application in Codespaces
1. Fork and open the project in GitHub Codespaces. You can get to Codespaces through the hamburger menu in the left upper corner on your Github account.
2. The Codespace environment will automatically set up the necessary Python packages and services.
3. Before running the application, start the PostgreSQL and Grafana services. Wait for about 45 seconds for PostgreSQL to fully start and ignore the false failure message for Grafana, it should be running properly: 
   ```bash
   sudo service postgresql start   
   sudo service grafana-server start
   ```
4. Run `main.py` in the Codespace terminal:
   ```bash
   python src/main.py
   ```
   
## Documentation

### Generating API Documentation with Sphinx

This project uses Sphinx for generating comprehensive API documentation, facilitating an easy understanding of the application's codebase.

#### Building the Documentation
To generate the documentation:
1. Navigate to the `docs` directory:
   ```bash
   cd docs
   make html
   ```

### Viewing the Documentation
For a better viewing experience, it's recommended to use a standard HTTP server to serve the generated HTML documentation:
   ```bash
   cd build/html
   python -m http.server
   ```
Open your web browser and navigate to http://localhost:8000. You can now browse the Sphinx-generated documentation.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Authors

- Boguslaw Jablkowski jablkowski@bast.de

