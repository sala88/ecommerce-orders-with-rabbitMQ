import config as cf
import pika, json, os
from fpdf import FPDF

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def generate_report(payload):
    print('Generate report')
    create_folder("report")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 14)  
    pdf.multi_cell(0, 10, f"ID: " + payload.get('id'))
    pdf.multi_cell(0, 10, f"User Email: " + payload.get('user_email'))
    pdf.multi_cell(0, 10, f"Product: " + payload.get('product'))
    pdf.multi_cell(0, 10, f"Quantity: " + payload.get('quantity'))
    pdf.output('report/' + payload.get('id') + '.pdf')
    print('Report done')

def callback(ch, method, properties, body):
    generate_report(json.loads(body))
    ch.basic_ack(delivery_tag=method.delivery_tag)

def consumer_report():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=cf.RMQ_HOST, 
                                                                   port=cf.RMQ_PORT, 
                                                                   credentials=pika.PlainCredentials(cf.RMQ_USER, cf.RMQ_PASSWORD)))
    channel = connection.channel()

    queue = channel.queue_declare(cf.ORDERS_QUEUE_REPORT)

    channel.queue_bind(
        exchange=cf.EXCHANGE_NAME,
        queue=queue.method.queue,
        routing_key=cf.BINDING_KEY_REPORT
    )

    channel.basic_consume(
        queue=cf.ORDERS_QUEUE_REPORT,
        on_message_callback=callback
    )

    print('Waiting message to generate report..')
    channel.start_consuming()

if __name__ == "__main__":
    consumer_report()