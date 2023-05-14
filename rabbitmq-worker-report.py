import config as cf
import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host=cf.RMQ_HOST, 
                                                               port=cf.RMQ_PORT, 
                                                               credentials=pika.PlainCredentials(cf.RMQ_USER, cf.RMQ_PASSWORD)))
channel = connection.channel()

channel.queue_declare(cf.ORDERS_QUEUE_REPORT)

channel.queue_bind(
    exchange=cf.EXCHANGE_NAME,
    queue=cf.ORDERS_QUEUE_REPORT,
    routing_key='order.report'  # binding key
)

def callback(ch, method, properties, body):
    payload = json.loads(body)
    print(' [x] Generating report')
    print(f"""
    ID: {payload.get('id')}
    User Email: {payload.get('user_email')}
    Product: {payload.get('product')}
    Quantity: {payload.get('quantity')}
    """)
    print(' [x] Done')
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(
    queue=cf.ORDERS_QUEUE_REPORT,
    on_message_callback=callback
)

print(' [*] Waiting for notify messages. To exit press CTRL+C')
channel.start_consuming()