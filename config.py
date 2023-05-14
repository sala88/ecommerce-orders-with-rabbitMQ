

# Flask
DEBUG = True
HOST = 'localhost'
PORT = 8080

# RabbitMQ
RMQ_USER = 'user'
RMQ_PASSWORD = 'bitnami'
RMQ_HOST = 'localhost'
RMQ_PORT = 5672
ORDERS_QUEUE_NOTIFY = 'order_notify'
ORDERS_QUEUE_REPORT = 'order_report'
EXCHANGE_NAME = 'order'
EXCHANGE_TYPE = 'direct'