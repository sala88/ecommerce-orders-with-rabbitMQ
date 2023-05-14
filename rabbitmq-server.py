from flask import Flask, request
import config as cf
import pika
import json
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    return 'OK'

@app.route('/order/', methods = ['POST'])
def order():
    request_data = request.get_json()

    
    order = {
        'id': str(uuid.uuid4()),
        'user_email': request_data['user_email'],
        'product': request_data['product'],
        'quantity': request_data['quantity']
    }
    print(order)


    connection = pika.BlockingConnection(pika.ConnectionParameters(host=cf.RMQ_HOST, 
                                                                   port=cf.RMQ_PORT, 
                                                                   credentials=pika.PlainCredentials(cf.RMQ_USER, cf.RMQ_PASSWORD)))
    channel = connection.channel()

    channel.exchange_declare(
        exchange=cf.EXCHANGE_NAME, 
        exchange_type=cf.EXCHANGE_TYPE
    )
    
    channel.queue_declare(
        cf.ORDERS_QUEUE_NOTIFY
    )
    
    channel.queue_declare(
        cf.ORDERS_QUEUE_REPORT
    )

    channel.queue_bind(
        exchange=cf.EXCHANGE_NAME,
        queue=cf.ORDERS_QUEUE_NOTIFY,
        routing_key='order.notify'  # binding key
    )
    
    channel.queue_bind(
        exchange=cf.EXCHANGE_NAME,
        queue=cf.ORDERS_QUEUE_REPORT,
        routing_key='order.report'  # binding key
    )

    channel.basic_publish(
        exchange=cf.EXCHANGE_NAME,
        routing_key='order.notify',
        body=json.dumps({'user_email': order['user_email']})
    )

    print(' [x] Sent notify message')
    channel.basic_publish(
        exchange=cf.EXCHANGE_NAME,
        routing_key='order.report',
        body=json.dumps(order)
    )
    print(' [x] Sent report message')

 


    connection.close()
    return " [x] Sent: %" 


if __name__ == '__main__':
    app.run(debug=cf.DEBUG, host=cf.HOST, port=cf.PORT)