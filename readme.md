This repository is pulled from ELA-Innovation's Bluetooth-Python-sample, and then modified to support other types of sensors and sending data to influxdb.

It uses ELA-Innovations code (in the ela folder) and `bluepy` to interface with bluetooth IoT sensors. It uses the PyP100 library to interface with a Tapo P110 energy monitoring plug. The data from all these sensors is requested every 10 seconds, and then uploaded to an influxdb server.

## Installation

Setup uv for managing python env

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install required packages for bluetooth:

```
sudo apt install -y \
    libglib2.0-dev \
    libbluetooth-dev \
    bluez \
    pkg-config \
    build-essential
```

Install docker and docker compose by following the instructions on [their website](https://docs.docker.com/engine/install/debian/)

Make sure to add your user to the docker group:

```
sudo groupadd docker 
sudo usermod -aG docker $USER
newgrp docker # so you don't have to log out and back in
``

Start influxdb up and setup your docker compose stuff.  

```
docker compose up
```

Under load data in the UI (localhost:8086) you can create an api token.

Copy the .env template file and enter in the api token.

Setup your tapo account information to access the power meter.

## Usage

Requirments: Python (3.11 or later?) and InfluxDB. 

Install and start influxdb. 

Use the `.env-template` file to create a `.env` file with all the required properties.

`
pip install -r requirements.txt
`

`
uv run main.py
`

## Folder Structure

`/ela/` hosts the library files for interfacing with ELA sensors.

`main.py` is the actual script for gathering data.

all the other python files are just testing/example files.

