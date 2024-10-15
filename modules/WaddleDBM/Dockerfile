FROM  ghcr.io/penguincloud/web2py-core:latest AS BUILD
LABEL company="Penguin Tech Group LLC"
LABEL org.opencontainers.image.authors="info@penguintech.group"
LABEL license="GNU AGPL3"

# GET THE FILES WHERE WE NEED THEM!
COPY . /opt/manager/waddledbm/
WORKDIR /opt/manager/waddledbm


# PUT YER ARGS in here
ARG APP_TITLE="WB-dbm" #Change this to actual title for Default

# BUILD IT!
RUN ansible-playbook entrypoint.yml -c local --tags "build,run"

# PUT YER ENVS in here
ENV HELLO="WORLD"

WORKDIR /var/www/html/web2py/

# Switch to non-root user
# USER waddlebot

# Entrypoint time (aka runtime)
ENTRYPOINT ["/bin/bash","/opt/manager/waddledbm/entrypoint.sh"]