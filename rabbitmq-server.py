from flask import Flask, request, render_template
import config as cf
import pika, json, uuid

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def about():
    return render_template('about.html')

def publish_message(channel, exchange, routing_key, body):
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=body)
    print(' [x] Sent notify message')

@app.route('/order/', methods = ['GET', 'POST'])
def order():
    if request.method == 'POST':

        order = {
            'id': str(uuid.uuid4()),
            'user_email': request.form['user_email'],
            'product': request.form['product'],
            'quantity': request.form['quantity']
        }




        connection = pika.BlockingConnection(pika.ConnectionParameters(host=cf.RMQ_HOST, 
                                                                    port=cf.RMQ_PORT, 
                                                                    credentials=pika.PlainCredentials(cf.RMQ_USER, cf.RMQ_PASSWORD)))
        channel = connection.channel()

        channel.exchange_declare(
            exchange=cf.EXCHANGE_NAME, 
            exchange_type=cf.EXCHANGE_TYPE
        )
        
        publish_message(channel, cf.EXCHANGE_NAME, cf.BINDING_KEY_NOTIFY, json.dumps({'user_email': order['user_email']}))

        publish_message(channel, cf.EXCHANGE_NAME, cf.BINDING_KEY_REPORT, json.dumps(order))

        connection.close()

    return render_template('order.html')




if __name__ == '__main__':
    app.run(debug=cf.DEBUG, host=cf.HOST, port=cf.PORT)



