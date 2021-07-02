from confluent_kafka import KafkaError
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError

consumber = AvroConsumer({
    'sasl.mechanism': 'PLAIN',
    'sasl.username': 'cq_user10',
    'sasl.password': 'cq_user!',
    'security.protocol': 'SASL_PLAINTEXT',
    'bootstrap.servers': ['77.1.22.70:9094', '77.1.22.71:9094', '77.1.22.72:9094', '77.1.22.73:9094',
                          '77.1.22.74:9094', '77.1.22.75:9094', '77.1.22.76:9094', '77.1.22.77:9094',
                          '77.1.22.78:9094', '77.1.22.79:9094', '77.1.22.80:9094', '77.1.22.81:9094'],
    'schema.registry.url': 'http://77.1.22.70:8081,http://77.1.22.71:8081,http://77.1.22.72:8081,'
                           'http://77.1.22.73:8081,http://77.1.22.74:8081,http://77.1.22.75:8081,'
                           'http://77.1.22.76:8081,http://77.1.22.77:8081,http://77.1.22.78:8081,'
                           'http://77.1.22.79:8081,http://77.1.22.80:8081,http://77.1.22.81:8081',
    'group.id': 'group_id'})

consumber.subscribe(['CQDSJB_GXPT_DB.GX_SH_LWZX_SMGPXX'])

while True:
    try:
        message = consumber.poll(100)
    except SerializerError as e:
        print("Message deserialization failed for {}: {}".format(message, e))
        break
    if message is None:
        continue
    if message.error():
        print("AvroConsumer error: {}".format(message.error()))
        continue
    print(message.value())

consumber.close()
