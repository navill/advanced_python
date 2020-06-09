import json
from pymemcache.client.base import Client


def json_serializer(key, value):
    if isinstance(value, str):
        return value, 1
    return json.dumps(str(value)), 2


def json_deserializer(key, value, flags):
    if flags == 1:
        return value
    if flags == 2:
        return json.loads(value)
    raise Exception("Unknown serialization format")


# pymemcache initailize: $memcached -l 127.0.0.1:11211
client = Client(('127.0.0.1', 11211), serializer=json_serializer,
                deserializer=json_deserializer)
client.set('key', {'a': 'b', 'c': 'd'})
result = client.get('key')
print(result)

# binary는 json encode에서 지원하지 않는 타입이므로 str(지원 가능)로 변환 후 dumps해야한다.
bit_data = b'asdlkfajsenr'
client.set('key1', bit_data)
print(client.get('key1'))
