#!/usr/bin/env python
import pika
import json
import sys

sys.path.append('../')

from analyzer.weights import NodesBertScoring
from analyzer.weights import EntityNodesFinder
from analyzer.graph import MMGraphAnalyzer

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='input')
channel.queue_declare(queue='output')
nodes_finder = EntityNodesFinder()
weights_analyzer = NodesBertScoring()
graph_analyzer = MMGraphAnalyzer()


def preprocess(data):
    data = json.loads(data.decode("utf-8"))
    # data['text'].append(str(len(data['text'])))
    nodes_finder.preprocess(data['text'])
    weights_analyzer.analyze(nodes_finder.all_tokens, nodes_finder.all_nps, nodes_finder.all_ners)
    """
    print(nodes_finder.all_nps,
          nodes_finder.all_ners,
          nodes_finder.all_tokens)
    """
    result = '{}'
    # result = json.dumps(weights_analyzer.analyze(data['text']))
    # result = json.dumps(graph_analyzer.analyze(data['text'], result))
    channel.basic_publish(exchange='', routing_key='output', body=result)


def callback(ch, method, properties, body):
    preprocess(body)

channel.basic_consume(callback, queue='input', no_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()