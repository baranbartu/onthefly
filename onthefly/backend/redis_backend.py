import json
from onthefly.backend import AbstractBackend
from redis import Redis


class RedisBackend(AbstractBackend):
    def __init__(self, options, **kwargs):
        self.client = Redis.from_url(options['URL'])
        super(RedisBackend, self).__init__(options, **kwargs)

    def set(self, name, value):
        self.client.hset(
            self.bucket_prefix, name, json.dumps(value))

    def get(self, name):
        dumped = self.client.hget(self.bucket_prefix, name)
        return json.loads(dumped)

    def delete(self, name):
        self.client.hdel(self.bucket_prefix, name)

    def set_fields(self):
        self.client.hset(
            self.bucket_prefix, 'fields', json.dumps(self.field_registry))

    def fields(self):
        fields_dumped = self.client.hget(self.bucket_prefix, 'fields')
        return json.loads(fields_dumped) if fields_dumped else []

    def values(self):
        if not self.get_fields():
            return {}
        values = self.client.hmget(
            self.bucket_prefix, self.get_fields())
        all_values = {}
        for i, field in enumerate(self.get_fields()):
            all_values[field] = json.loads(values[i])
        return all_values
