'''
Inove Drone Mock Python IoT
---------------------------
Autor: Inove Coding School
Version: 1.0

Descripcion:
Se utiliza Flask para crear un emulador de vuelo
de un drone

Ejecución: Lanzar el programa y abrir en un navegador la siguiente dirección URL
http://IP:5009/
'''

__author__ = "Inove Coding School"
__email__ = "alumnos@inove.com.ar"
__version__ = "1.0"

import traceback
import json

from flask import Flask, request, jsonify, render_template, redirect
from flask_socketio import SocketIO
from flask_socketio import send, emit


app = Flask(__name__)
app.secret_key = 'ptSecret'
app.config['SECRET_KEY'] = 'ptSecret'
socketio = SocketIO(app)

# ---- MQTT ----
import paho.mqtt.client as mqtt
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("MQTT Conectado")
    client.subscribe("actuadores/volar")
    client.subscribe("actuadores/luces/#")
    client.subscribe("actuadores/motores/#")
    client.subscribe("actuadores/joystick")
    client.subscribe("sensores/inerciales")

def mqtt_connect():
    if client.is_connected() is False:
        try:
            client.username_pw_set("senaIoT", "pic16f877a")
            client.connect("192.168.68.200", 1883, 10)
            print("Conectado al servidor MQTT")
            client.loop_start()
        except:
            print("No pudo conectarse")


def on_message(client, userdata, msg):
    topic = str(msg.topic)
    value = str(msg.payload.decode("utf-8"))
    if topic == "actuadores/volar":
        socketio.emit('volar', int(value))

    # ---- Web sockets contra el frontend ----

    # NOTA: Podría mejorarse el manejo del ID
    # utilizando regular expression (re)
    # Se deja de esta manera para que se vea
    # facil para el alumno
    if topic == "actuadores/luces/1":
        socketio.emit('luz_1', int(value))
    if topic == "actuadores/motores/1":
        socketio.emit('motor_1', int(value))
    if topic == "actuadores/motores/2":
        socketio.emit('motor_2', int(value))
    if topic == "actuadores/motores/3":
        socketio.emit('motor_3', int(value))
    if topic == "actuadores/motores/4":
        socketio.emit('motor_4', int(value))

    if topic == "actuadores/joystick":
        socketio.emit('joystick', value)

    if topic == "sensores/inerciales":
        inerciales = json.loads(value)
        socketio.emit('heading', int(inerciales["heading"]))


# ---- Endpoints ----
@app.route('/')
def home():
    mqtt_connect()
    return render_template('index.html')


if __name__ == "__main__":
    client.on_connect = on_connect
    client.on_message = on_message

    app.run(debug=True, host="0.0.0.0", port=5009)
