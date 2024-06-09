#!/usr/bin/env bash

DOCKER_IMAGE="ghcr.io/cochaviz/academic_markdown"
PREAMBLE="academic_markdown (check_health.sh):"

GOOD="✅"
BAD="⚠️"
INFO="ℹ️ "

HEALTH=0

check_in_path() {
    if [[ $(type -P "$1") ]]; then
        echo "$PREAMBLE $GOOD Found ($1) in path"
        return 0
    else
        echo "$PREAMBLE $BAD Could not find ($1) in path"
        return 1
    fi
}

check_docker() {
    check_in_path docker

    if [[ $? ]]; then
        echo "$PREAMBLE $INFO Running docker health check..."

        docker run hello-world
        if [[ $? ]]; then
            echo "$PREAMBLE $GOOD Docker correctly configured"
        else
            echo "$PREAMBLE $BAD Docker does not seem to be configured correctly"
            return 1
        fi

        if [[ $(docker images | grep $DOCKER_IMAGE) ]]; then
            echo "$PREAMBLE $GOOD Found '$DOCKER_IMAGE' docker image"
        else
            echo "$PREAMBLE $INFO Could not find image: '$DOCKER_IMAGE'."
            echo "$PREAMBLE $INFO Pulling from ghcr.io..."
          docker pull "$DOCKER_IMAGE"
            
        fi
    else
        echo "$PREAMBLE $INFO Not running docker health check since it cannot be found on path..."
        return 1
    fi

    return 0
}

dependencies=(
    pandoc  
    pandoc-crossref 
    python3
    pdflatex
)

dependencies_optional=(
    tectonic
)

if [[ $1 = "--docker" ]]; then
    check_docker
else
    for dependency in "${dependencies[@]}"; do
        check_in_path $dependency

        if ! [[ $? ]]; then
            HEALTH=1
        fi
    done

    echo "$PREAMBLE $INFO The following are optional dependencies."

    for dependency in "${dependencies_optional[@]}"; do
        check_in_path $dependency
    done
fi

if ! [[ HEALTH ]]; then
    exit 1
fi
