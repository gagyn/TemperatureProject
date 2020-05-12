# TemperatureProject
Scanning and saving temperature using Raspberry PI and Arduino

### Run the app using Docker:

```git clone https://github.com/gagyn/TemperatureProject.git```

```docker build -t temperature .```

```docker run -d --device=/dev/ttyACM0 --name temperature temperature```

For me the USB port where the Arduino is plugged in, was /dev/ttyACM0. You may have it somewhere else, so check it before.

```docker logs temperature```
