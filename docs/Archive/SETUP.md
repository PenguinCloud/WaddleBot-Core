
1. Ensure that docker is installed on your local machine. URL:
https://www.docker.com/products/docker-desktop/

2. Ensure that the docker client application is running in the background.

3. Open a terminal in the root folder of "WaddleBot-Core"

4. Run the following command to build the docker container:

`docker build -t waddlebot-core .`

5. Check that the Image is available in the docker client after a successful build in the "Images" tab.

6. To run the image, click on the "start" button next to the image.

7. A new prompt should appear with options.

8. For other components to work with the matterbridge component of the core system, the port 4200 of the image must be exposed. In the prompt that appeared, in the "Ports" section, type "4200" in the "Host Port" part of the settings prompt.

9. Navigate to "http://localhost:4200/api/messages" to check if the port is exposed.

10. If you dont get an error and get a result such as "[]" or a json object between those brackets, then that means the image/container is running.
