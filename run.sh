#!/bin/bash
echo ${{secrets.AWS_ECR_LOGIN_URI}}/${{ secrets.ECR_REPOSITORY_NAME }}

# Pull the latest Docker image
docker pull $AWS_ECR_LOGIN_URI/$ECR_REPOSITORY_NAME:latest

# Check if container "mltest1" is running and stop/remove it
if docker ps -q --filter "name=mltest1" | grep -q .; then
    docker stop mltest1
    docker rm -fv mltest1
fi

# Run Docker image to serve users
docker run -d -p 8080:8080 --ipc="host" --name=mltest1 \
    -e "AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID" \
    -e "AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY" \
    -e "AWS_REGION=$AWS_REGION" \
    $AWS_ECR_LOGIN_URI/$ECR_REPOSITORY_NAME:latest

# Clean previous images and containers
docker system prune -f
