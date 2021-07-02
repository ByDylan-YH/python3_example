import io
import avro.schema
from example.kafka import KafkaConsumer

consumer = KafkaConsumer("CQDSJB_GXPT_DB.GX_SH_LWZX_SMGPXX",
                                      sasl_mechanism="PLAIN",
                                      sasl_plain_username="admin",
                                      sasl_plain_password="admin-secret",
                                      security_protocol="SASL_PLAINTEXT",
                                      bootstrap_servers=['77.1.22.70:9094', '77.1.22.71:9094', '77.1.22.72:9094', '77.1.22.73:9094',
                                                         '77.1.22.74:9094', '77.1.22.75:9094', '77.1.22.76:9094', '77.1.22.77:9094',
                                                         '77.1.22.78:9094', '77.1.22.79:9094', '77.1.22.80:9094', '77.1.22.81:9094'],
                                      group_id="group_id")

schema_path= "user.avsc"
schema = avro.schema.parse(open(schema_path).read())

for msg in consumer:
    bytes_reader = io.BytesIO(msg.value)
    decoder = avro.io.BinaryDecoder(bytes_reader)
    reader = avro.io.DatumReader(schema)
    user1 = reader.read(decoder)
    print(user1)