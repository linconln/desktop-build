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
    chave = transaction["conta"]
    print("Calculando a média: ", chave)
    media_lida = redis_conn.lindex(chave, 0)
    if(media_lida==None):
        media = transaction["value"]
        redis_conn.rpush(chave, media)
    else:
        print("Media lida: ", media_lida)
        media = (float(media_lida) + transaction["value"]) / 2
        print(" Media: ", media)
        redis_conn.lset(chave, 0, media)
    print("Criando Chave: ", chave, " Transacao: ", transaction)
    if(redis_conn.rpush(chave, json.dumps(transaction))==1):
        print("Transação criada: ", chave, transaction)
    else:
        print("*** Erro na criação ***", chave, transaction)

channel.basic_consume(queue=queue_name,
                      on_message_callback=chamado_quando_uma_transacao_eh_consumida, auto_ack=True)

print("Esperando por mensagens. Para sair pressione CTRL+C")
channel.start_consuming()