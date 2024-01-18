#!/bin/bash
# Start PostgreSQL
echo "Starting postgresql server..."
sudo service postgresql start &

# Wait for PostgreSQL to be ready (adjust the sleep as needed)
#sleep 30

# Start Grafana
echo "Starting grafana server..."
sudo service grafana-server start &

# Keep the container running
tail -f /dev/null