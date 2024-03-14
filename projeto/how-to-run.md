# Como rodar o projeto
senhas padrões nos containers
dados de entrada em transaction.json
executar fraud-validator-consumer.py para aguardar os eventos
executar transaction-producer.py para gerar os eventos
executar report-generator.py para gerar e obter os endereços de acesso dos relatórios

# Python dependências
pip install pika
pip install redis
pip install minio

# Docker containers
docker run --rm -it -p '15672:15672 -p 5672:5672 rabbitmq:3-management
docker run -it --rm --name redis -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
docker run -p 9000:9000 -p 9001:9001 quay.io/minio/minio server /data --console-address ":9001"