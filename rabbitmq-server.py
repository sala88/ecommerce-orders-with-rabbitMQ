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

    channel.basic_publish(
        exchange=cf.EXCHANGE_NAME,
        routing_key=cf.BINDING_KEY_NOTIFY,
        body=json.dumps({'user_email': order['user_email']})
    )
    print(' [x] Sent notify message')
    
    channel.basic_publish(
        exchange=cf.EXCHANGE_NAME,
        routing_key=cf.BINDING_KEY_REPORT,
        body=json.dumps(order)
    )
    print(' [x] Sent report message')

    connection.close()
    return " [x] Sent: %", order


if __name__ == '__main__':
    app.run(debug=cf.DEBUG, host=cf.HOST, port=cf.PORT)