import json
import pika
import asyncio
import aiohttp

from aiohttp import web

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='input')
# channel.queue_declare(queue='output')

def output_message():
    method_frame, header_frame, body = channel.basic_get('output')
    if method_frame:
        channel.basic_ack(method_frame.delivery_tag)
        return body.decode("utf-8")
    else:
        return ''

async def text_handler(request):
    input = await request.json()
    response = web.Response(content_type='text/html')
    channel.basic_publish(exchange='', routing_key='input', body=json.dumps(input))
    response.text = "Message was successfully queued.\n"
    return response

async def get_graph(request):
    result_str = output_message()
    if result_str:
        response = web.Response(content_type='application/json')
        response.text = json.dumps(result_str)
    else:
        response = web.Response(content_type='text/html')
        response.text = 'The queue is empty!\n'
    return response

async def application(request):
    return web.FileResponse('../static/templates/index.html')

async def init(loop):
    handler = app.make_handler()
    srv = await loop.create_server(handler, '0.0.0.0', 8080)
    print('serving on', srv.sockets[0].getsockname())
    return srv


loop = asyncio.get_event_loop()
app = web.Application()
app.router.add_post('/text', text_handler)
app.router.add_get('/result', get_graph)
app.router.add_get('/app', application)
loop.run_until_complete(init(loop))

if __name__ == '__main__':
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass