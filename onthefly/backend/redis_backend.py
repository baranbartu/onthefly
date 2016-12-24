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

    def add_field(self, name):
        fields_dumped = self.client.hget(self.bucket_prefix, 'fields')
        fields = json.loads(fields_dumped) if fields_dumped else []
        fields.append(name)
        self.client.hset(
            self.bucket_prefix, 'fields', json.dumps(list(set(fields))))

        original_value = self.get_value_from_original_settings(name)
        self.set_value(name, original_value)

    def set_value(self, name, value):
        self.client.hset(
            self.bucket_prefix, name, json.dumps(value))

    def get_value(self, name):
        dumped = self.client.hget(self.bucket_prefix, name)
        return json.loads(dumped)

    def get_all_values(self):
        fields = self.get_all_fields()
        values = self.client.hmget(
            self.bucket_prefix, fields)
        all_values = {}
        for i, field in enumerate(fields):
            all_values[field] = json.loads(values[i])
        return all_values

    def delete(self, name):
        fields = self.get_all_fields()
        fields.pop(name)
        self.client.hset(
            self.bucket_prefix, 'fields', json.dumps(list(set(fields))))
        self.client.hdel(self.bucket_prefix, name)
