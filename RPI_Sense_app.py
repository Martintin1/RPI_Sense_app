# -*- coding: utf-8 -*-
from __future__ import print_function # In python 2.7
from flask import (Flask, request, jsonify, render_template)
import sys
from sense_hat import SenseHat
from decimal import Decimal

app = Flask(__name__)

sense = SenseHat()
sense.set_rotation(180)

counter = 0
displayGreen = True


@app.route('/api', methods=['POST'])
def get_sensor_value(): 
    usernam = request.form['usernam']
    return jsonify(usernam='hej')


@app.route('/')
def index():
    return render_template('RPI_Sense_app.html')
        
        
@app.route('/ajax', methods = ['GET'])
def ajax_request():
    valueTemp = str(round(sense.get_temperature() - 16.3, 1))
    valuePressure = str(round(sense.get_pressure(), 1))

    global counter
    global displayGreen
    
    if(displayGreen):
        sense.set_pixel(0, 0, [0, 255, 0])
        sense.set_pixel(1, 0, [0, 255, 0])
        sense.set_pixel(2, 0, [0, 255, 0])
        sense.set_pixel(3, 0, [0, 255, 0])

        sense.set_pixel(4, 0, [0, 0, 0])
        sense.set_pixel(5, 0, [0, 0, 0])
        sense.set_pixel(6, 0, [0, 0, 0])
        sense.set_pixel(7, 0, [0, 0, 0])
        displayGreen = False
    else:
        sense.set_pixel(4, 0, [0, 0, 255])
        sense.set_pixel(5, 0, [0, 0, 255])
        sense.set_pixel(6, 0, [0, 0, 255])
        sense.set_pixel(7, 0, [0, 0, 255])

        sense.set_pixel(0, 0, [0, 0, 0])
        sense.set_pixel(1, 0, [0, 0, 0])
        sense.set_pixel(2, 0, [0, 0, 0])
        sense.set_pixel(3, 0, [0, 0, 0])
        displayGreen = True

    counter += 1
    if(counter == 10):
        sense.show_message("Temp: " + valueTemp)
    elif(counter == 20):
        sense.show_message("Tryck: " + valuePressure)
        counter = 0
    
    return jsonify({'Temp': valueTemp, 'Pressure': valuePressure})
    
@app.route('/displaytext', methods=['GET'])
def displayText():
    sense.show_message("Perfekt!")
    return jsonify({'MessageDisplayed': True})
    
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug = True)
    
