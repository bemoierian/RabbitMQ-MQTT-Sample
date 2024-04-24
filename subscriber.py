import paho.mqtt.client as mqtt

def on_subscribe(client, userdata, mid, reason_code_list, properties):
    if reason_code_list[0].is_failure:
        print(f"Consumer: Broker rejected your subscription: {reason_code_list[0]}")
    else:
        print(f"Consumer: Broker granted the following QoS: {reason_code_list[0].value}")

def on_unsubscribe(client, userdata, mid, reason_code_list, properties):
    if len(reason_code_list) == 0 or not reason_code_list[0].is_failure:
        print("Consumer: Unsubscribe succeeded (if SUBACK is received in MQTTv3 it success)")
    else:
        print(f"Consumer: Broker replied with failure: {reason_code_list[0]}")
    client.disconnect()

def on_message(client, userdata, message):
    # userdata is the structure we choose to provide, here it's a list()
    print(f"Consumer: Received message '{message.payload.decode()}' on topic '{message.topic}'")

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Consumer: Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        client.subscribe("amq.topic.mytopic")
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

mqttc.user_data_set([])
mqttc.connect("localhost", 1883, 60)
mqttc.loop_forever()
