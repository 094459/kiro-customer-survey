#!/bin/bash

# Copyright (2026) Beachgeek.co.uk
# Author: Ricardo Sueiras
# Apache 2.0 license

set -e

CONTAINER_RUNTIME=${CONTAINER_RUNTIME:-docker}
IMAGE_NAME="customer-survey-app"
REGISTRY=${REGISTRY:-""}

validate_semver() {
    if [[ ! $1 =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo "Error: Invalid SEMVER format. Use x.y.z (e.g., 1.0.0)"
        exit 1
    fi
}

build_image() {
    local version=$1
    local push=$2
    
    validate_semver "$version"
    
    local full_name="${REGISTRY:+$REGISTRY/}$IMAGE_NAME:$version"
    
    echo "Building multi-arch image: $full_name"
    
    $CONTAINER_RUNTIME build \
        --platform linux/amd64,linux/arm64 \
        -t "$full_name" \
        .
    
    if [[ "$push" == "true" ]]; then
        echo "Pushing image: $full_name"
        $CONTAINER_RUNTIME push "$full_name"
    fi
}

list_images() {
    echo "Local images for $IMAGE_NAME:"
    $CONTAINER_RUNTIME images | grep "$IMAGE_NAME" || echo "No images found"
}

list_all_images() {
    echo "All local container images:"
    $CONTAINER_RUNTIME images
}

delete_image() {
    local version=$1
    
    validate_semver "$version"
    
    local full_name="${REGISTRY:+$REGISTRY/}$IMAGE_NAME:$version"
    
    echo "Deleting image: $full_name"
    $CONTAINER_RUNTIME rmi "$full_name"
}

run_image() {
    local version=$1
    
    validate_semver "$version"
    
    local full_name="${REGISTRY:+$REGISTRY/}$IMAGE_NAME:$version"
    
    echo "Running image: $full_name"
    $CONTAINER_RUNTIME run --rm -p 5000:5000 "$full_name"
}

shell_image() {
    local version=$1
    
    validate_semver "$version"
    
    local full_name="${REGISTRY:+$REGISTRY/}$IMAGE_NAME:$version"
    
    echo "Starting shell in image: $full_name"
    $CONTAINER_RUNTIME run --rm -it "$full_name" /bin/bash
}

show_help() {
    cat << EOF
Usage: $0 [OPTIONS] VERSION

Build and tag container images with SEMVER versioning.

ARGUMENTS:
  VERSION           SEMVER version (e.g., 1.0.0, 1.2.3)

OPTIONS:
  -p, --push        Push image to registry after build
  -l, --list        List existing local images for this app
  --list-all        List all local container images
  -d, --delete      Delete image by version
  -r, --run         Run image by version (port 5000:5000)
  -s, --shell       Run image and start interactive shell
  -h, --help        Show this help message

ENVIRONMENT VARIABLES:
  CONTAINER_RUNTIME Container runtime (default: docker)
  REGISTRY         Container registry URL (optional)

EXAMPLES:
  $0 1.0.0                    # Build version 1.0.0
  $0 --push 1.0.1            # Build and push version 1.0.1
  $0 --delete 1.0.0          # Delete version 1.0.0
  $0 --run 1.0.0             # Run version 1.0.0
  $0 --shell 1.0.0           # Shell into version 1.0.0
  $0 --list                  # List existing images
  REGISTRY=myregistry.com $0 --push 1.2.0
EOF
}

main() {
    local push=false
    local delete=false
    local run=false
    local shell=false
    local version=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -p|--push)
                push=true
                shift
                ;;
            -d|--delete)
                delete=true
                shift
                ;;
            -r|--run)
                run=true
                shift
                ;;
            -s|--shell)
                shell=true
                shift
                ;;
            -l|--list)
                list_images
                exit 0
                ;;
            --list-all)
                list_all_images
                exit 0
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            -*)
                echo "Unknown option: $1"
                show_help
                exit 1
                ;;
            *)
                if [[ -z "$version" ]]; then
                    version=$1
                else
                    echo "Error: Multiple versions specified"
                    exit 1
                fi
                shift
                ;;
        esac
    done
    
    if [[ -z "$version" ]]; then
        echo "Error: VERSION required"
        show_help
        exit 1
    fi
    
    if [[ "$delete" == "true" ]]; then
        delete_image "$version"
    elif [[ "$run" == "true" ]]; then
        run_image "$version"
    elif [[ "$shell" == "true" ]]; then
        shell_image "$version"
    else
        build_image "$version" "$push"
    fi
}

main "$@"
