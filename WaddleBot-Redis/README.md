# Waddlebot Testing Redis Cache

For testing purposes, a docker compose file has been supplied to create a local Redis chache to test the main listener's capabilities of executing commands dynamically from Redis. The compose file creates a local docker container that exposes certain ports and runs in the background for redis.

To get the container running, do:

1. Ensure that docker is installed on your local machine. URL:
https://www.docker.com/products/docker-desktop/

2. Ensure that docker compose is working on your system by typing:

`docker compose version`

It should display something like:

`Docker Compose version v2.23.3-desktop.2`

3. Run the following command to install and run the container (assuming you are in the WaddleBot-Redis folder with the terminal):

`docker compose -f redis-docker-compose.yml up`

4. The instance should have exposed 2 ports for Redis, namely 6379 and 8001. To check if the container is running, open your web browser and navigate to http://localhost:8001/. It should open the resdisinsights interface.

