# TemperatureProject
Scanning and saving temperature using Raspberry PI and Arduino

## Download config and docker-compose file:

##### Linux:
`curl -o docker-compose.yml https://raw.githubusercontent.com/gagyn/TemperatureProject/master/docker-compose.yml && curl -o config.json https://raw.githubusercontent.com/gagyn/TemperatureProject/master/config.json`

##### Powershell:
`curl -o docker-compose.yml https://raw.githubusercontent.com/gagyn/TemperatureProject/add-api/docker-compose.yml; curl -o config.json https://raw.githubusercontent.com/gagyn/TemperatureProject/add-api/config.json`

### Now edit file ***config.json*** and ***docker-compose.yml*** with your Arduino port!

For me the USB port where Arduino is plugged in, is /dev/ttyACM0. You may have it somewhere else, so check it before.

### Mongo database

You can use mongo database on localhost or put your link to external database in ***config.json*** file.

### Run temperature scanner and API using docker-compose

`docker-compose up`

### Scanning started...

Now your scanner has started and it's saving temperatures records in mongo database.
