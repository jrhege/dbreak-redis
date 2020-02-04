""" Tests for dbreak_redis.py module """

import fakeredis
import pytest

import dbreak_redis


class TestRedisWrapper:
    """ Tests for the RedisWrapper class """

    @pytest.fixture()
    def connection(self):
        """ A mocked connection to Redis """

        connection = fakeredis.FakeRedis()

        connection.set("sample-string", "sample")
        connection.lpush("sample-list", 1, 2, 3)
        connection.hset("sample-hash", "a", 1)
        connection.sadd("sample-set", "a", "b", "c")

        return connection

    @pytest.fixture()
    def wrapped_connection(self, connection):
        """ A mocked connection to Redis wrapped in a RedisWrapper """

        return dbreak_redis.RedisWrapper(connection)

    def test_set(self, wrapped_connection):
        """ Test using the set command """

        wrapped_connection.execute_statement(
            "set foo 1"
        )

        found = wrapped_connection.raw_connection.get("foo")

        assert found == b"1", "Unexpected stored string value"

    def test_set_quoted(self, wrapped_connection):
        """ Test using set with a quoted string """

        wrapped_connection.execute_statement(
            "set foo 'this is the string to use'"
        )

        found = wrapped_connection.raw_connection.get("foo")

        assert found == b"this is the string to use", "Unexpected stored string value"

    def test_get(self, wrapped_connection):
        """ Test using get """

        outputs = wrapped_connection.execute_statement(
            "get sample-string"
        )

        assert outputs[0] == b"sample", "Unexpected retrieved string value"

    def test_lpush(self, wrapped_connection):
        """ Test using lpush """

        wrapped_connection.execute_statement(
            "lpush foo 'a test' 'this is'"
        )

        found = wrapped_connection.raw_connection.lrange("foo", 0, -1)

        assert found == [b"this is", b"a test"], "Unexpected list items stored"

    def test_lrange(self, wrapped_connection):
        """ Test using lrange """

        outputs = wrapped_connection.execute_statement(
            "lrange sample-list 0 -1"
        )

        assert outputs[0] == [b"3", b"2", b"1"], "Unexpected retrieved list items"

    def test_hset(self, wrapped_connection):
        """ Test using hset """

        wrapped_connection.execute_statement(
            "hset foo a 1 b 2 c 3"
        )

        found = wrapped_connection.raw_connection.hgetall("foo")

        assert found == {b"a": b"1", b"b": b"2", b"c": b"3"}, "Unexpected stored hash items"

    def test_hgetall(self, wrapped_connection):
        """ Test using hgetall """

        outputs = wrapped_connection.execute_statement(
            "hgetall sample-hash"
        )

        assert outputs[0] == {b"a": b"1"}, "Unexpected retrieved hash items"

    def test_sadd(self, wrapped_connection):
        """ Test using sadd """

        wrapped_connection.execute_statement(
            "sadd foo a 'this is b' c"
        )

        found = wrapped_connection.raw_connection.smembers("foo")

        assert found == {b"a", b"this is b", b"c"}, "Unexpected stored hash items"

    def test_smembers(self, wrapped_connection):
        """ Test using smembers """

        outputs = wrapped_connection.execute_statement(
            "smembers sample-set"
        )

        assert outputs[0] == {b"a", b"b", b"c"}, "Unexpected retrieved hash items"
