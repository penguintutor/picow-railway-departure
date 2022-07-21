#!/usr/bin/env python3
from flask import Flask, request
from datetime import datetime, timedelta
import json

app = Flask(__name__)

platform0_dest = ["Camp Hill", "Watertown", "Blueditch"]
platform1_dest = ["Hill Valley", "Svalbard", "Gill Wood"]

platform0_train = 0
platform1_train = 1

platform0_time = datetime.now() + timedelta(minutes=2)
platform1_time = datetime.now() + timedelta(minutes=4)


@app.route('/departures.py')
def departures():
    global platform0_train, platform1_train, platform0_time, platform1_time
    platform = request.args.get('platform', default=0, type=int)
    current_time = datetime.now()     
    all_departures = {}
    # if train1 departed then reset time and set next train
    if (platform0_time <= datetime.now()):
        platform0_time = platform0_time + timedelta(minutes=10)
        platform0_train += 1
        if platform0_train >= len(platform0_dest):
            platform0_train = 0
    if (platform1_time <= datetime.now()):
        platform1_time = platform1_time + timedelta(minutes=10)
        platform1_train += 1
        if platform1_train >= len(platform1_dest):
            platform1_train = 0
        
    if platform == 1:
        train1_time_string = platform1_time.strftime('%H:%M')
        train1_dest_string = platform1_dest[platform1_train]
        train2_time = platform1_time+timedelta(minutes=10)
        train2_time_string = train2_time.strftime('%H:%M')
        train2 = platform1_train +1 
        if train2 >= len(platform1_dest):
            train2 = 0
        train2_dest_string = platform1_dest[train2]
    else:
        train1_time_string = platform0_time.strftime('%H:%M')
        train1_dest_string = platform0_dest[platform0_train]
        train2_time = platform0_time+timedelta(minutes=10)
        train2_time_string = train2_time.strftime('%H:%M')
        train2 = platform0_train +1 
        if train2 >= len(platform0_dest):
            train2 = 0
        train2_dest_string = platform0_dest[train2]
        
    all_departures['train1'] = [train1_time_string, train1_dest_string, train1_time_string]
    
    all_departures['train2'] = [train2_time_string, train2_dest_string, train2_time_string]
    
    all_departures["time"] = current_time.strftime('%H:%M')
    
    return (json.dumps(all_departures))
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)