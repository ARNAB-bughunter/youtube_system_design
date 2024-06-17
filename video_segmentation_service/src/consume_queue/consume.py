#!/usr/bin/env python
import pika
import json
from src.video_segmentation.video_segmentation import video_segmentation


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello',durable=True)

    def callback(ch, method, properties, body):
        body = json.loads(body)
        video_segmentation(body['video_path'], body['video_id'])
        ch.basic_ack(delivery_tag=method.delivery_tag)



    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=False)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
