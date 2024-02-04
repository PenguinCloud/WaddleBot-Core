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
# BUILD IT!
RUN ansible-playbook entrypoint.yml -c local --tags build

# PUT YER ENVS in here
ENV USER_NAME="waddlebot" 
ENV USER_DISCORD_ID="001112223"
ENV USER_DISCORD_NAME="PenguinzRockExample"
ENV DISCORD_TOKEN="123getme"
ENV DISCORD_ENABLE="0"
ENV TWITCH_TOKEN="123getme"
ENV TWITCH_ENABLE="0"


# Switch to non-root user
USER waddlebot

# Entrypoint time (aka runtime)
ENTRYPOINT ["/bin/bash","/opt/manager/entrypoint.sh"]
