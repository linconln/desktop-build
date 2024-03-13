import pika
import json
import redis

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host = "localhost",
    port = 5672,
    virtual_host = "/"
))

channel = connection.channel()

queue_name = "fraud_validator_queue"

channel.queue_declare(queue="fraud_validator_queue")
channel.queue_bind(exchange="amq.fanout", queue="fraud_validator_queue")

redis_conn = redis.Redis(host='localhost', port=6379, db=0)

def chamado_quando_uma_transacao_eh_consumida(channel, method_frame, header_frame, body):
    transaction = json.loads(body.decode('utf-8'))
    print("Transação: ", transaction)

channel.basic_consume(queue=queue_name,
                      on_message_callback=chamado_quando_uma_transacao_eh_consumida, auto_ack=True)

print("Esperando por mensagens. Para sair pressione CTRL+C")
channel.start_consuming()