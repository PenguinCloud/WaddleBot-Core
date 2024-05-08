FROM ghcr.io/penguincloud/core AS BUILD
LABEL company="Penguin Tech Group LLC"
LABEL org.opencontainers.image.authors="info@penguintech.group"
LABEL license="GNU AGPL3"

# GET THE FILES WHERE WE NEED THEM!
COPY . /opt/manager/
WORKDIR /opt/manager


# PUT YER ARGS in here
ARG APP_TITLE="waddlebot" 
ARG MATTERBRIDGE_VERSION="1.26.0"


# PUT YER ENVS in here
ENV APP_TITLE="waddlebot" 
ENV USER_NAME="waddlebot" 
ENV USER_DISCORD_ID=""
ENV USER_DISCORD_NAME="PenguinzRockExample"
ENV DISCORD_TOKEN=""
ENV DISCORD_CHANNEL=""
ENV DISCORD_ENABLE="1"
ENV TWITCH_NAME="TwitchExample"
ENV TWITCH_CHANNEL=""
ENV TWITCH_TOKEN=""
ENV TWITCH_ENABLE="1"
ENV API_NAME="WaddleAPI"
ENV API_ADDRESS="127.0.0.1:4242"
ENV API_ENABLE="1"
ENV TELEGRAM_NAME="TelegramExample"
ENV TELEGRAM_TOKEN=""
ENV TELEGRAM_CHANNEL=""
ENV TELEGRAM_ENABLE="0"
ENV GATEWAY_NAME="GatewayExample"

# BUILD IT!
RUN ansible-playbook entrypoint.yml -c local --tags "build,configure"


# Switch to non-root user
USER waddlebot

# Entrypoint time (aka runtime)
ENTRYPOINT ["/bin/bash","/opt/manager/entrypoint.sh"]
