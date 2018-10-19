#!/usr/bin/python3
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import time
from hermes_python.hermes import Hermes

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    mqtt_client.subscribe('hermes/nlu/intentParsed')
    mqtt_client.subscribe('hermes/asr/textCaptured')
    mqtt_client.subscribe('hermes/asr/startListening')
    mqtt_client.subscribe('hermes/nlu/query')
    mqtt_client.publish('hermes/dialogueManager/startSession',json.dumps({
            'siteId': 'default',
            'init': {
                'type': 'action',
                'canBeEnqueued':False
            }
        }))
    
def on_message(client, userdata, msg):
   
    payload = json.loads(msg.payload.decode('utf-8'))

    # if msg.topic == 'hermes/asr/textCaptured':
    #     print payload['text']

    # if msg.topic == 'hermes/nlu/intentParsed':
    #     print payload['intent']['intentName']

    if msg.topic == 'hermes/nlu/query':
        print payload
      

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_IP_ADDR, MQTT_PORT)
mqtt_client.loop_forever()