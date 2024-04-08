#!/bin/bash

DOCKER_IMAGE=zenoh-carla-bridge
DOCKER_FILE=container/Dockerfile_carla_bridge
ROCKER_PATH=container/rocker

if [ ! "$(docker images -q ${DOCKER_IMAGE})" ]; then
    echo "${DOCKER_IMAGE} does not exist. Creating..."
    docker build -f ${DOCKER_FILE} -t ${DOCKER_IMAGE} .
fi

${ROCKER_PATH} --nvidia --network host --privileged --x11 --user --volume $(pwd):$HOME/autoware_carla_launch -- ${DOCKER_IMAGE}

