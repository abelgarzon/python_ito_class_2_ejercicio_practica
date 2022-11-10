import time
import json
import paho.mqtt.client as paho

# instalar paho con:
# $ python3 -m pip install paho-mqtt

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Mqtt Publicador conectado")
    else:
        print(f"Mqtt Publicador connection faild, error code={rc}")

def controlador(client, actuador, valor):
    if actuador == "luces":
        topico = "actuadores/luces/1"
    elif actuador == "volar":
        topico = "actuadores/volar"
    elif actuador[0:5] == "motor":
        topico = "actuadores/motores/" + actuador[-1]
    elif actuador == "joystick":
        topico = "actuadores/joystick"
    client.publish(topico, valor)

if __name__ == "__main__":
    client = paho.Client("controlador")
    client.on_connect = on_connect
    client.username_pw_set("senaIoT", "pic16f877a")
    client.connect("localhost", 1883, 10)
    client.loop_start()

    print("Drone Mock: Sistema controlador de actuadores")

    time.sleep(0.1)

    while True:
        actuador = input("Ingrese que actuador desea controlar, o escriba FIN para salir: ").lower()
        if actuador == "fin":
            break
        if actuador == "joystick":
            x = float(input("Ingrese el valor que desea enviar en x: "))
            y = float(input("Ingrese el valor que desea enviar en y: "))
            valor = []
            coordenadas = ["x", "y"]
            valor.append(x)
            valor.append(y)
            valor = dict(zip(coordenadas, valor))
            valor = json.dumps(valor)
        else:
            valor = int(input("Ingrese el valor que desea enviar: "))
        controlador(client, actuador, valor)

    client.disconnect()
    client.loop_stop()