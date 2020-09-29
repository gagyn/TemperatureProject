sudo systemctl restart docker

echo $DOCKERHUB_PASS | docker login -u $DOCKERHUB_LOGIN --password-stdin
docker buildx build --platform linux/arm32/7 -t gagyn/temperature_project:scanner -f ./src/TemperatureScanner/Dockerfile.arm32 ./src --push
docker buildx build --platform linux/arm32/7 -t gagyn/temperature_project:nginx -f ./src/nginx/Dockerfile.arm32 ./src/nginx --push