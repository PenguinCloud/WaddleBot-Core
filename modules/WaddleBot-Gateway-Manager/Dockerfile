FROM ghcr.io/penguincloud/core:v5.0.1 AS BUILD
LABEL company="Penguin Tech Group LLC"
LABEL org.opencontainers.image.authors="info@penguintech.group"
LABEL license="GNU AGPL3"

# GET THE FILES WHERE WE NEED THEM!
COPY . /opt/manager/
WORKDIR /opt/manager


# PUT YER ARGS in here
ARG APP_TITLE="waddlebot-core" 
ARG MATTERBRIDGE_VERSION="1.26.0"


# PUT YER ENVS in here
ENV GATEWAY_CREATION_URL="http://127.0.0.1:8000/WaddleDBM/routing_gateways/create_gateway.json"
ENV GATEWAY_DELETION_URL="http://127.0.0.1:8000/WaddleDBM/routing_gateways/delete_by_channel_id_and_gateway_type.json/"
ENV GATEWAY_SERVER_GET_URL="http://127.0.0.1:8000/WaddleDBM/gateway_servers/get_all.json"
ENV GATEWAY_SERVER_CREATE_URL="http://127.0.0.1:8000/WaddleDBM/gateway_servers/create_gateway_server.json"
ENV GATEWAY_SERVER_DELETE_URL="http://127.0.0.1:8000/WaddleDBM/gateway_servers/delete_by_name.json/"
ENV TWITCH_HOST="irc.chat.twitch.tv"
ENV TWITCH_PORT="6667"
ENV TWITCH_PASS=""
ENV TWITCH_NICK="mjtestbot"
ENV DISCORD_TOKEN=""
ENV DISCORD_BOT_INVITE_URL=""

# Python related commands to install dependencies, create a virtual environment, and run the application
RUN apt-get update 
RUN apt-get install -y python3-dev
RUN apt-get install -y libpq-dev
RUN apt-get install -y postgresql


# Set the working directory to the WaddleBot-Configurator directory
WORKDIR /opt/manager/app

# # Install the dependencies in the virtual environment, located in the WaddleBot-Configurator directory
RUN pip install psycopg2-binary
RUN pip install --ignore-installed blinker
# RUN pip install -r requirements.txt

# Set the working directory back to the manager directory
WORKDIR /opt/manager

# BUILD IT!
RUN ansible-playbook entrypoint.yml -c local --tags "build"


# Switch to non-root user
USER waddlebot

# Entrypoint time (aka runtime)
ENTRYPOINT ["/bin/bash","/opt/manager/entrypoint.sh"]
