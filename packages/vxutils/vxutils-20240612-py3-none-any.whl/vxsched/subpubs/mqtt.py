"""mqtt订阅发布模块"""

import logging
import random
import time
from typing import Optional, Any
from paho.mqtt import client as mqtt_client
from paho.mqtt.enums import CallbackAPIVersion
from vxsched import VXSubscriber, VXPublisher, VXScheduler
from vxsched.event import VXEvent, VXTrigger

broker = "broker.emqx.io"
port = 1883
topic = "python/mqtt"
# generate client ID with pub prefix randomly
client_id = f"python-mqtt-{random.randint(0, 1000)}"
username = "emqx"
password = "**********"


class VXMQTTPublisher(VXPublisher):
    def __init__(
        self,
        broker: str,
        port: str,
        topic: str,
        username: str,
        password: str,
        ca_certs: str = "",
        *,
        target_scheduler: Optional[VXScheduler] = None,
    ) -> None:
        self._broker = broker
        self._port = port
        self._topic = topic
        self._ca_certs = ca_certs
        self._username = username
        self._password = password
        self.connect()
        super().__init__(target_scheduler=target_scheduler)

    def connect(self) -> None:
        self._client = mqtt_client.Client(
            callback_api_version=CallbackAPIVersion.VERSION2,
            client_id=f"vxsched-mqtt-{random.randint(0, 100000)}",
            protocol=mqtt_client.MQTTv5,
        )

        if self._ca_certs:
            self._client.tls_set(ca_certs=self._ca_certs)

        self._client.username_pw_set(self._username, self._password)

        def on_connect(
            client: mqtt_client.Client,
            userdata: Any,
            flags: Any,
            rc: int,
            *args: Any,
            **kwargs: Any,
        ) -> None:
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        self._client.on_connect = on_connect
        self._client.connect(broker, port)
        self._client.loop_start()
        time.sleep(1)
        print("Connected to MQTT Broker!")

    def __call__(
        self,
        event: str | VXEvent,
        *,
        trigger: VXTrigger | None = None,
        data: mqtt_client.Dict[str, Any] | None = None,
        channel: str = "default",
        priority: int = 10,
        reply_to: str = "",
    ) -> None:
        if isinstance(event, str):
            event = VXEvent(
                type=event,
                data=data or {},
                priority=priority,
                channel=channel,
                reply_to=reply_to,
            )

        # self._client.publish(self._topic, event.model_dump_json(indent=4))
        self._client.publish("testtopic/1", "333")
        print("Published")


if __name__ == "__main__":
    publisher = VXMQTTPublisher(
        "rd621101.ala.cn-hangzhou.emqxsl.cn",
        8883,
        topic="testtopic/1",
        username="hq",
        password="miniqmt",
        ca_certs="E:\\quant\\src\\vxutils\\log\\emqxsl-ca.crt",
    )
    while True:
        publisher("test", data={"test": "test"})
        time.sleep(1)
