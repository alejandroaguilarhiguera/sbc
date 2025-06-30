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

# Conectar
client.connect()
print("Conectado a AWS IoT Core")

# Publicar un mensaje JSON en un topic
topic = "sensor"
mensaje = {
    "temperatura": 23.4,
    "unidad": "C",
    "timestamp": int(time.time())
}

client.publish(topic, json.dumps(mensaje), 1)
print("Mensaje publicado")

# Esperar antes de desconectar
time.sleep(2)
client.disconnect()
