import config as cf
import pika, json, smtplib
from email.mime.text import MIMEText


def send_email(to_mail):
    print("Sending email.")
    subject = "Order placed"
    body = "Thank you for placing your order"
    sender = "companiesdb@gmail.com"
    password = "eeemuaxidsohyhwn"
    recipients = [to_mail]

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print('Email send')

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
    send_email(json.loads(body)['user_email'])
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(
    queue=cf.ORDERS_QUEUE_NOTIFY,
    on_message_callback=callback
)

print('Waiting message to send email..')
channel.start_consuming()