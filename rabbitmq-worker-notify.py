import config as cf
import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host=cf.RMQ_HOST, 
                                                               port=cf.RMQ_PORT, 
                                                               credentials=pika.PlainCredentials(cf.RMQ_USER, cf.RMQ_PASSWORD)))
channel = connection.channel()

channel.queue_declare(cf.ORDERS_QUEUE_NOTIFY)

channel.queue_bind(
    exchange=cf.EXCHANGE_NAME,
    queue=cf.ORDERS_QUEUE_NOTIFY,
    routing_key='order.notify'  # binding key
)

def callback(ch, method, properties, body):
    payload = json.loads(body)
    print(' [x] Notifying {}'.format(payload['user_email']))
    print(' [x] Done')
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(
    queue=cf.ORDERS_QUEUE_NOTIFY,
    on_message_callback=callback
)

print(' [*] Waiting for notify messages. To exit press CTRL+C')
channel.start_consuming()