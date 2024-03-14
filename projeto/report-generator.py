from minio import Minio
import redis
import io

minio_conn = Minio(
    endpoint="localhost:9000", 
    access_key="minioadmin", 
    secret_key="minioadmin",
    secure=False)

bucket_name = "meu-bucket"
bucket_exists = minio_conn.bucket_exists(bucket_name)
if bucket_exists:
    print(f"Bucket {bucket_name} já existe!")
else:
    minio_conn.make_bucket(bucket_name)
    print("Bucket criado com sucesso!")

#nome_arquivo = "atividade_01_aula.py"

redis_conn = redis.Redis(host='localhost', port=6379, db=0)

chaves = redis_conn.keys("report*")

for chave in chaves:
    str_chave = chave.decode("utf-8")
    str_chave = str_chave+".txt"
    print("Chave: ", str_chave)
    reports = redis_conn.lrange(chave, 0, 999999)
    value=""
    size=0
    for report in reports:
        print(report)
        str_report=report.decode("utf-8")
        value=value+str_report+"\n"

    size=len(value)
    value_as_bytes=value.encode("utf-8")
    str_reports=io.BytesIO(value_as_bytes)

    result = minio_conn.put_object(
        bucket_name=bucket_name,
        object_name=str_chave,
        data=str_reports,
        length=size
    )

    print(f"Versão do arquivo {str_chave}: {result.version_id}")

    get_url = minio_conn.get_presigned_url(
        method='GET',
        bucket_name=bucket_name,
        object_name= str_chave, )

#    delete_url = minio_conn.get_presigned_url(
#        method='DELETE',
#        bucket_name=bucket_name,
#        object_name= str_chave)

    print(f"Download URL: [GET]{get_url}")
#print(f"Delete URL: [DELETE]{e_}")