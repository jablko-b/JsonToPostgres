# Basierend auf einem offiziellen Python-Image
ARG VARIANT=3-bookworm
FROM python:${VARIANT}

RUN apt-get update && apt-get install -y sudo
RUN apt-get install iputils-ping -y

# Installieren Sie benötigte Pakete und PostgreSQL
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y postgresql postgresql-contrib \
    # Grafana hinzufügen
    && apt-get install -y apt-transport-https software-properties-common wget \
    && mkdir -p /etc/apt/keyrings/ \
    && wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null \
    && echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list \
    && apt-get update \
    && apt-get install -y grafana-enterprise \
    # Entfernen Sie imagemagick (aus Sicherheitsgründen)
    && apt-get purge -y imagemagick imagemagick-6-common 

# PostgreSQL Konfiguration anpassen und initialisieren
RUN echo "host all all all md5" >> /etc/postgresql/15/main/pg_hba.conf \
    && echo "listen_addresses='*'" >> /etc/postgresql/15/main/postgresql.conf \
    && sed -i -e 's/local   all             all                                     peer/local   all             all                                     md5/' /etc/postgresql/15/main/pg_hba.conf \
    && sed -i -e 's/host    all             all             127.0.0.1\/32            peer/host    all             all             127.0.0.1\/32            md5/' /etc/postgresql/15/main/pg_hba.conf \
    && sudo service postgresql start \    
    && sudo -u postgres psql -c "CREATE USER dev WITH SUPERUSER PASSWORD 'dev';" \
    && sudo -u postgres createdb -O dev wim 
    #&& sudo -u postgres -d wim -f /workspaces/JsonToPostgres/mock_data/wim.sql


# Sicherstellen, dass PostgreSQL bei jedem Start des Containers ausgeführt wird
# Copy the entrypoint script into the image
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# Set the entrypoint
#ENTRYPOINT ["entrypoint.sh"]
#CMD ["/usr/local/bin/entrypoint.sh"]

# Optional: Installieren Sie zusätzliche Pakete oder führen Sie weitere Schritte aus
