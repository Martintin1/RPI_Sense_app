# -*- coding: utf-8 -*-
from __future__ import print_function # In python 2.7
from flask import (Flask, request, jsonify)
import sys
from sense_hat import SenseHat
from decimal import Decimal

app = Flask(__name__)

sense = SenseHat()
sense.set_rotation(180)

counter = 0

html_page = """<!DOCTYPE HTML>
<html>
<head>
<title>Sensormtning</title>
<script>

    var XMLHttp = new XMLHttpRequest();
    
    function startMeasure()
    {
        if(XMLHttp.readyState == 0 || XMLHttp.readyState == 4)
        {
           XMLHttp.open("GET", "/ajax", true);
           XMLHttp.onreadystatechange = handleServerResponse; // anropas da man far ett svar
           XMLHttp.send(null);
           setTimeout('startMeasure()',1000);
        }
        else
        {
           //alert("korvTimeout")
           setTimeout('startMeasure()',1000); //vanta en sekund, sedan prova igen
        }
    }

    function handleServerResponse()
    {
       if(XMLHttp.readyState == 4)
       {
          if(XMLHttp.status == 200) //om verforingen funkade
          {
            json = JSON.parse(XMLHttp.responseText);
            document.getElementById("tempDiv").innerHTML = 'Temp: ' + json.Temp;
            document.getElementById("pressureDiv").innerHTML = 'Tryck: ' + json.Pressure;
          }
          else
          {
             //alert("korv5")
          }
       }
    }

    function displayText()
    {
       if(XMLHttp.readyState == 0 || XMLHttp.readyState == 4)
       {
          XMLHttp.open("GET", "/displaytext", true);
          XMLHttp.send(null);
       }
    
    }
</script>
</head>
<body>
<h1>SensormÃ¤tning</h1>
<form action="" method="GET">
<input type="button" value="Starta mÃ¤tning" onclick="startMeasure()">
</form>
<form action="" method="GET">
<input type="button" value="Visa text" onclick="displayText()"
</form>
<div id="tempDiv"></div>
<div id="pressureDiv"></div>
</body>
</html>"""

@app.route('/api', methods=['POST'])
def get_sensor_value(): 
    usernam = request.form['usernam']
    return jsonify(usernam='hej')


@app.route('/')
def index():
    return html_page
        
        
@app.route('/ajax', methods = ['GET'])
def ajax_request():
    valueTemp = str(round(sense.get_temperature() - 16.3, 1))
    valuePressure = str(round(sense.get_pressure(), 1))

    global counter
    counter += 1
    if(counter == 10):
        sense.show_message("Temp: " + valueTemp)
    elif(counter == 20):
        sense.show_message("Tryck: " + valuePressure)
        counter = 0
    
    return jsonify({'Temp': valueTemp, 'Pressure': valuePressure})
    
@app.route('/displaytext', methods=['GET'])
def displayText():
    sense.show_message("Snyggt jobbat!")
    return jsonify({'MessageDisplayed': True})
    
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug = True)
    
