# Raspberry Pi train departure web server

This is a flask web application for use with the model railway train departure board. It is designed to run on a Raspberry Pi, but could be on a different system with Python 3 and the Flask modules.

It runs on port 8080 and does not need any special permissions.

## Install

Save the departures.py file on your local system.

# Set destinations

If you would like to change the destinations update the variables
    platform0_dest
    platform1_dest

### Install Flask
sudo apt install python3-flask


## Run
    python3 departures.py

Alternatively give the python file executable permissions and then you can call it directly. 

For details of how to start programs automatically 
[Starting programs automatically on Linux](http://www.penguintutor.com/linux/startup)