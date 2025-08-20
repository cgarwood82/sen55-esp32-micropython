# Micro Python esp32-c3 Environment Sensor

This project supports getting a sen55 sensor working with a esp32-c3 leveraging MicroPython. This repo makes use of the
[sen5x](https://pypi.org/project/sensirion-i2c-sen5x/) module. The general implementation here was to develope an i2c 
connection to the sensor from the esp32-c3, spin up a webserver, and present the metrics in a format that is consumable
by Prometheus which can be presented in Grafana.

## Esp32-c3 Super Mini
If you leverage an esp32-c3 super mini, it has a 5v that you can use to power the sensor. Otherwise, you will have to us
a convert 3.3v to 5v. For the i2c connection, you simply need to pick two gpio pins to update on in main.py. The 
default pins are 21 and 22. See the pinout for the sen55 sensor to determine which is tx and which is rx and update
the main.py file accordingly.

## Networking
Leveraging the wifi interface on the c3, the wifi ssid and password hard coded in main.py can be used to connect to the
network. It doesn't need egress to the internet, as it's only used to publish metrics for prometheus to consume.

## Webserver
The webserver is a single page that has text that is updated every 10 seconds. The text is the current temperature,
humidity, and VOCs, particulate matter, and n0x. The text is updated every 10 seconds. Further, it's displayed over
standard port 80.

## Development
If you are using a brand new esp32 module, you'll need to flash the esp32-c3 firmware. The firmware can be found
[here](https://micropython.org/download/esp32-c3/). Once this flashed, you are  then start working from your preferred
development environment. I personally used JetBrains PyCharm and made use of the excellent [MicroPython plugin](https://plugins.jetbrains.com/plugin/16233-micropython).

Be sure to install the requirements.txt file before you start as that isn't included in this repo. You'll need this to 
actually have the firmware flash as it'll be deployed. 

## Validation
After you flash the firmware, the esp32 will reboot. Looking through the REPL terminal, you should see the following:

```
Connecting to WiFi...
Connected, IP address: 10.66.1.100
MicroPython v1.24.1 on 2024-11-29; ESP32C3 module with ESP32C3
Type "help()" for more information.
>>> HTTP server listening on ('0.0.0.0', 80)
Sensor data updated: {'ppm2_5': 0, 'temperature': 25.5, 'voc': 100, 'ppm4_0': 0, 'humidity': 50, 'nox': 1, 'ppm1_0': 0, 'ppm10_0': 0}
```

This will show you that you have successfully flashed the esp32, the IP address of the esp32, that the webserver is 
running, and the sensor is reporting data. Open your web browser and navigate to the IP address of the esp32. You should
see the following:

```
# HELP sen5x_ppm1_0 Particulate Matter 1.0 measurement
# TYPE sen5x_ppm1_0 gauge
sen5x_ppm1_0 0
# HELP sen5x_ppm2_5 Particulate Matter 2.5 measurement
# TYPE sen5x_ppm2_5 gauge
sen5x_ppm2_5 0
# HELP sen5x_ppm4_0 Particulate Matter 4.0 measurement
# TYPE sen5x_ppm4_0 gauge
sen5x_ppm4_0 0
# HELP sen5x_ppm10_0 Particulate Matter 10.0 measurement
# TYPE sen5x_ppm10_0 gauge
sen5x_ppm10_0 0
# HELP sen5x_humidity Humidity measurement
# TYPE sen5x_humidity gauge
sen5x_humidity 50
# HELP sen5x_temperature Temperature measurement
# TYPE sen5x_temperature gauge
sen5x_temperature 25.5
# HELP sen5x_voc VOC measurement
# TYPE sen5x_voc gauge
sen5x_voc 100
# HELP sen5x_nox NOx measurement
# TYPE sen5x_nox gauge
sen5x_nox 1
```

This is the data that is being published in a formate for prometheus.

## Next Steps...
Outside of the scope of this repo, next up would be to configure prometheus and grafana to present the data. 
