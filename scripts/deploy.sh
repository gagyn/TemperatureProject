systemctl restart docker
docker build --platform=local -o . git://github.com/docker/buildx
mkdir -p ~/.docker/cli-plugins
mv buildx ~/.docker/cli-plugins/docker-buildx
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

echo $DOCKERHUB_PASS | docker login -u $DOCKERHUB_LOGIN --password-stdin
docker buildx build --platform linux/arm32/7 -t gagyn/temperature_project:scanner -f ./src/TemperatureScanner/Dockerfile.arm32 ./src --push
docker buildx build --platform linux/arm32/7 -t gagyn/temperature_project:nginx -f ./src/nginx/Dockerfile.arm32 ./src/nginx --push