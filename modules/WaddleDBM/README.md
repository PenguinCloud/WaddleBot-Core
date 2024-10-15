[![Publish Docker image](https://github.com/PenguinCloud/project-template/actions/workflows/docker-image.yml/badge.svg)](https://github.com/PenguinCloud/core/actions/workflows/docker-image.yml) [![version](https://img.shields.io/badge/version-5.1.1-blue.svg)](https://semver.org) 

# Project Overview
<< This is a template. Copy this templated repository to make new projects. Once done, add a 1 paragraph introduction / elevator speech about your project.
>>
# Why this image vs others
## Built in self testing and healing
All PTG builds have unit and dynamic tests as part of the build of their images, as well as during runtime to ensure the system keeps running as expected. If the system falls out of bounds of the test, the images have some self healing capabilities fix common minor problems.

## Secured... even if the software isn'template
All PTG images under go a 8 stage security check to ensure not only is the PTG portion of the code secure, but to also identify and help remediate the underlying libraries and software security. 

## Updated daily
All of our images are checked daily for updates from upstream sources.

## Designed for air-gapped or for internet facing
All PTG images are designed to be ran inside of air gapped environments with no internet, allowing datacenters to use a local cache as well saving bandwidth.

## Active contribution and maintenance
PTG is a company with funding and full time contributors to ensure our images aren't stale.

## Scalable
ALl PTG images are designs to be micro-containers, ensuring easy verical and horizontal scaling is possible.

## PTG drinks it's own koolaid
PTG actively uses it's own images for everything so we can identify bugs which our automation misses.

## Beta testing
PTG relies on volunteer customers and community members to beta test images, ensuring our stable / production images are well baked and as bug free as possible solutions.

# Contributors
## PTG
Maintainer: creatorsemailhere@penguintech.group
General: info@penguintech.group

## community

* Insert list of community collaborators


# Resources
Documentation: ./docs/
Premium Support: https://support.penguintech.group 
Community Bugs / Issues: -/issues

# How to setup for testing

To setup and run this module for testing puproses in web2py, do the following:

1. Ensure that you have web2py downloaded somewhere on your system. Source files of web2py can be found at http://www.web2py.com/init/default/download

2. Navigate to the "applications" folder of web2py, found in its root directory.

3. Copy the top level folder of this project (in this case its "WaddleDBM") into the "applications" folder.

4. In the root folder of web2py, run web2py.exe

5. In the next prompt that appears, leave the settings as is and provide a root password to web2py.

6. Click on "start server"

7. Web2py should be running now. To view that the application is setup correctly, navigate to: http://127.0.0.1:8000/WaddleDBM/default/index
