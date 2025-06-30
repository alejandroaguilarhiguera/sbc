from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

mqtt_private_key = os.getenv("MQTT_PRIVATE_KEY")
mqtt_cert_key = os.getenv("MQTT_CERT_KEY")
mqtt_root_pem = os.getenv("MQTT_ROOT_PEM")


mqtt_client = os.getenv("MQTT_CLIENT")
mqtt_endpoint = os.getenv("MQTT_ENDPOINT")
mqtt_port = int(os.getenv("MQTT_PORT"))

# Configura tu cliente MQTT
client = AWSIoTMQTTClient(mqtt_client)
client.configureEndpoint(mqtt_endpoint, mqtt_port)


client.configureCredentials(mqtt_root_pem, mqtt_private_key, mqtt_cert_key)

# Opcional: configuración adicional
client.configureOfflinePublishQueueing(-1)  # Cola infinita
client.configureDrainingFrequency(2)  # Mensajes por segundo
client.configureConnectDisconnectTimeout(10)
client.configureMQTTOperationTimeout(5)

print("Conectado a AWS IoT Core")

# Publicar un mensaje JSON en un topic
topic = "action"
def custom_callback(client, userdata, message):
    print("\n--- Mensaje Recibido ---")
    print(f"Topic: {message.topic}")
    print(f"Payload: {message.payload.decode('utf-8')}") # Decodificar el payload de bytes a string
    print(f"QoS: {message.qos}")
    print("------------------------\n")

# Conectar
client.connect()

subscribe_topic = "sensor" # O, por ejemplo, "comandos/dispositivo1"
client.subscribe(subscribe_topic, 1, custom_callback)
topicToSend = "message"


message = {
    "key": "hello world"
}

client.publish(topicToSend, json.dumps(message), 1)



try:
    print("Manteniendo la conexión abierta. Presiona Ctrl+C para salir.")
    while True:
        time.sleep(1) # Espera 1 segundo para no consumir CPU innecesariamente
except KeyboardInterrupt:
    print("\nDesconexión iniciada por el usuario.")
    client.disconnect()
    print("Desconectado de AWS IoT Core.")



