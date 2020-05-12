# TemperatureProject
Scanning and saving temperature using Raspberry PI and Arduino

## Run the app using Docker:

`git clone https://github.com/gagyn/TemperatureProject.git`

### Now edit file ***config.txt*** with your Arduino port!

For me the USB port where Arduino is plugged in, was /dev/ttyACM0. You may have it somewhere else, so check it before.

`docker build -t temperature .`

`docker run -d --device=/dev/ttyACM0 --name temperature temperature`

Here 

## After a few minutes, if you want to get all the temperatures data, use command:

`docker logs temperature`

alternatively:

`docker exec -it temperature cat temperatures.txt`
