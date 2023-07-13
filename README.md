# ecommerce-orders-with-rabbitMQ


Creare i docker
Docker per le code RabbitMQ (in locale)

docker pull bitnami/rabbitmq

docker run --name  rabbitmq -p 4369:4369 -p 5551:5551 -p 5552:5552 -p 5672:5672 -p 15672:15672 -p 25672:25672 bitnami/rabbitmq:latest
