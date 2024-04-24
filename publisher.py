import time
import paho.mqtt.client as mqtt

def on_publish(client, userdata, mid, reason_code, properties):
    try:
        userdata.remove(mid)
        print("Producer: published message with mid: {}".format(mid))

    except KeyError:
        print("Producer: on_publish() is called with a mid not present in unacked_publish")

unacked_publish = set()
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_publish = on_publish

mqttc.user_data_set(unacked_publish)
mqttc.connect("localhost", 1883, 60)
mqttc.loop_start()

# Our application produce some messages
msg_info = mqttc.publish("amq.topic.mytopic", "my message")
unacked_publish.add(msg_info.mid)

# Wait for publish
msg_info.wait_for_publish()

mqttc.disconnect()
mqttc.loop_stop()
