from typing import Any, Callable, Optional

import json
import paho.mqtt.client as mqtt


class MqttClient:
    def __init__(self, host: str, port: int, use_tls: bool = False, ca_certs: Optional[str] = None):
        self.client = mqtt.Client()

        if use_tls:
            self.client.tls_set(ca_certs)

        self.client.connect(host, port)

    def publish(self, topic: str, data: Any, serialize: bool = True, qos: int = 0):
        if serialize:
            data = json.dumps(data, default=str)

        self.client.publish(topic, data, qos)


class MqttConsumer:
    def __init__(
        self, topic: str, qos: int, host: str, port: int, use_tls: bool = False, ca_certs: Optional[str] = None
    ):
        self.topic = topic
        self.qos = qos
        self.url_params: list[tuple[int, str]] = []
        self.host = host
        self.port = port
        self.use_tls = use_tls
        self.ca_certs = ca_certs

    def consume(self, cb: Callable[[dict, dict], None], serialize: bool = True):
        self.cb = cb

        for index, section in enumerate(self.topic.split("/")):
            if section.startswith(":"):
                self.topic = self.topic.replace(section, "+")
                self.url_params.append((index, section[1:]))

        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message_callback(serialize)

        if self.use_tls:
            client.tls_set(self.ca_certs)

        client.connect(self.host, self.port)
        client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(self.topic, self.qos)

    def on_message_callback(self, serialize: bool = True):
        def on_message(client, userdata, msg):
            msg.topic.split("/")

            payload = msg.payload
            if serialize:
                payload = json.loads(payload.decode("utf-8"))

            url_params = {}

            for index, param in self.url_params:
                url_params[param] = msg.topic.split("/")[index]

            if len(url_params.keys()) > 0:
                self.cb(payload, url_params)
            else:
                self.cb(payload)

        return on_message
