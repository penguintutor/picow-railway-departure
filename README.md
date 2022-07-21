# Pico W model railway train departure sign

This provides a railway train departure board running on a Raspberry Pi Pico W.
It can handle two SD1306 I2C display modules.

## Install

First setup the Raspberry Pi Pico W with the MicroPython interpretter. Use Thonny to connect to the Raspberry Pi and transfer files.

The following files need to be uploaded to the Raspberry Pi Pico W.

* main.py (main program file - save as main.py to run automatically)
* ssd1306.py (SSD1306 library)
* secrets.json (WiFi SSID and password - see below)

## Configure

You wil need to configure a secrets.json file with your WiFi details:

### secrets.json
Create a file called secrets.json with your network configuration information.

    {
    "SSID":"MYSSID",
    "WPASS":"WirelessPassword"
    }

### main.py

You may need to change the IP address in the url variable.

