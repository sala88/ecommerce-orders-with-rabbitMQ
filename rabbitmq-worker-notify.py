import config as cf
import pika, json

connection = pika.BlockingConnection(pika.ConnectionParameters(host=cf.RMQ_HOST, 
                                                               port=cf.RMQ_PORT, 
                                                               credentials=pika.PlainCredentials(cf.RMQ_USER, cf.RMQ_PASSWORD)))
channel = connection.channel()

channel.queue_declare(cf.ORDERS_QUEUE_NOTIFY)

channel.exchange_declare(
    exchange=cf.EXCHANGE_NAME, 
    exchange_type=cf.EXCHANGE_TYPE
)

channel.queue_bind(
    exchange=cf.EXCHANGE_NAME,
    queue=cf.ORDERS_QUEUE_NOTIFY,
    routing_key=cf.BINDING_KEY_NOTIFY
)

def callback(ch, method, properties, body):
    payload = json.loads(body)
    print('Notify the user: {}'.format(payload['user_email']))
    print('Notification done')
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(
    queue=cf.ORDERS_QUEUE_NOTIFY,
    on_message_callback=callback
)

print('Waiting for notification messages..')
channel.start_consuming()