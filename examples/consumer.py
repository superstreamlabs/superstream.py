import asyncio
import sys

from confluent_kafka import Consumer, KafkaException


async def main():
    token = "<superstream-token>"
    superstream_host = "<superstream-host>"
    group = "<kafka-consumer-group>"
    topics = ["<kafka-topic>"]
    brokers = "<kafka-broker>"
    config = {
        "bootstrap.servers": brokers,
        "security.protocol": "SASL_SSL",
        "sasl.mechanism": "PLAIN",
        "sasl.username": "",
        "sasl.password": "",
        "group.id": group,
        "session.timeout.ms": 6000,
        "enable.auto.offset.store": False,
        "statistics.interval.ms": 1000,
        "auto.offset.reset": "latest",
        "max.poll.interval.ms": 600000,
    }

    consumer = Consumer(config)
    consumer.subscribe(topics)

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            message = msg.value()
            if msg.error():
                raise KafkaException(msg.error())
            else:
                sys.stderr.write("[%s: %d] %s %s\n" % (msg.topic(), msg.partition(), message, msg.headers()))
    except KeyboardInterrupt:
        sys.stderr.write("%% Consumer stopped\n")

    finally:
        consumer.close()


if __name__ == "__main__":
    asyncio.run(main())
