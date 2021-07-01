from kafka import KafkaConsumer

consumer = kafka_avro_binary_consumer("CQDSJB_GXPT_DB.GX_SH_LWZX_SMGPXX",
                         sasl_mechanism="PLAIN",
                         sasl_plain_username="admin",
                         sasl_plain_password="admin-secret",
                         security_protocol="SASL_PLAINTEXT",
                         bootstrap_servers=['77.1.22.70:9094', '77.1.22.71:9094', '77.1.22.72:9094', '77.1.22.73:9094',
                                            '77.1.22.74:9094', '77.1.22.75:9094', '77.1.22.76:9094', '77.1.22.77:9094',
                                            '77.1.22.78:9094', '77.1.22.79:9094', '77.1.22.80:9094', '77.1.22.81:9094'],
                         group_id="group_id")

for message in consumer:
    print(message.topic, message.partition, message.offset, message.key, message.value.decode('utf-8','ignore'))
