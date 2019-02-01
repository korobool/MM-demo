#!/usr/bin/env python
import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='input')
channel.queue_declare(queue='output')


def preprocess(data):
    data = json.loads(data.decode("utf-8"))
    data['text'].append(str(len(data['text'])))
    result = json.dumps(data)
    channel.basic_publish(exchange='', routing_key='output', body=result)


def callback(ch, method, properties, body):
    preprocess(body)

channel.basic_consume(callback, queue='input', no_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()