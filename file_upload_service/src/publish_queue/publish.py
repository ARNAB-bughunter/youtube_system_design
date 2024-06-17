#!/usr/bin/env python
import pika
import json


def create_queue_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    return connection

def publish_message(connection, body):
    channel = connection.channel()
    channel.queue_declare(queue='hello',  durable=True)
    channel.basic_publish(exchange='', routing_key='hello', body=json.dumps(body))
