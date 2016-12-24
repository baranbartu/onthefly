import json
from onthefly.backend import BaseBackend
from redis import Redis


class RedisBackend(BaseBackend):
    def __init__(self, options, **kwargs):
        self.client = Redis.from_url(options['URL'])
        super(RedisBackend, self).__init__(options, **kwargs)

    def get_all_fields(self):
        fields_dumped = self.client.hget(self.bucket_prefix, 'fields')
        return json.loads(fields_dumped) if fields_dumped else []

    def set_fields(self):
        self.client.hset(
            self.bucket_prefix, 'fields', json.dumps(self._all_fields))

    def set_value(self, name, value):
        self.client.hset(
            self.bucket_prefix, name, json.dumps(value))

    def get_value(self, name):
        dumped = self.client.hget(self.bucket_prefix, name)
        return json.loads(dumped)

    def get_all_values(self):
        if not self.all_fields:
            return {}
        values = self.client.hmget(
            self.bucket_prefix, self.all_fields)
        all_values = {}
        for i, field in enumerate(self.all_fields):
            all_values[field] = json.loads(values[i])
        return all_values

    def delete_value(self, name):
        self.client.hdel(self.bucket_prefix, name)
