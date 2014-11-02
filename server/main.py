# -*- coding: utf-8 -*-
"""
YoMicro
Micropython board Yo service.
When receiving a Yo, the service will flash the LEDs on the board
When getting a 'shake' event from the board's accelerometer, the 
service will send a Yo out to subscribers.

"""
import sys
import serial
import requests
import oauth2
from time import sleep
from flask import request, Flask
from multiprocessing import Process

# Yo API Token: http://dev.justyo.co
token = 'd067c302-0414-4ad8-8f7c-d38fddff876b'
board = serial.Serial('/dev/tty.usbmodem1422', 9600, timeout=0)
app = Flask(__name__)

def listen():
    print "Listening for shakes..."
    # Listen for the board to emit a 'shake'
    while True:
        event = board.read(999)
        if '∆' in event:
            # Respond to shake by sending a yo to subscribers
            response = requests.post("http://api.justyo.co/yoall/", data={'api_token': token, 'link': 'https://github.com/rrotaru/YoMicro'})
            if response.status_code == 201:
                print "Board shaken! Yo successfully sent to all subscribers."
            elif response.status_code == 400:
                print "Slow down, Yo! Only one 'Yo all' per minute."
        # Take a short break so we don't send so many Yos.
        sleep(1)


@app.route("/yo/")
def yo():
    # Show who sent us a yo!
    username = request.args.get('username')
    print "We got a Yo from " + username + ', it\'s disco time!'
    # Respond by flashing the board (int represents for how many seconds)
    board.write('3')
    # OK!
    return 'OK'

if __name__ == "__main__":
    app.debug = True
    process = Process(target=listen)
    process.start()
    app.run(host="127.0.0.1", port=5000)
