"""
MIT License

Copyright (c) 2023 Bean-jun

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import pickle
import time
import uuid

from bframe import current_app, request
from bframe.logger import init_logger
from bframe.wrappers import Response

logger = init_logger()


class SessionMix:

    def __init__(self, key=None):
        self.session_id = key

    @property
    def get_session_key_name(self):
        return self.session_id or current_app.Config.get("SESSION_ID")

    def parse_session_id(self):
        if self.get_session_key_name not in request.Cookies.keys():
            return None
        return request.Cookies[self.get_session_key_name].value

    def create_session_key(self):
        session_key = str(uuid.uuid4()) + str(time.time())
        return session_key

    def open_session(self):
        session_key = self.parse_session_id()
        logger.info(f"open session, parse session key {session_key}")
        if not session_key or not self.has_storage(session_key):
            logger.info(
                f"open session, not has_storage session key {session_key}")
            session_key = self.create_session_key()
        request.session = session_key
        logger.info(f"open session, session key {session_key}")

    def save_session(self, resp: Response):
        resp.set_cookies(self.get_session_key_name,
                         request.session,
                         max_age=current_app.Config.get("SESSION_MAX_AGE"),
                         expires=current_app.Config.get("SESSION_EXPIRES"),
                         path=current_app.Config.get("SESSION_PATH"),
                         domain=current_app.Config.get("SESSION_DOMAIN"),
                         secure=current_app.Config.get("SESSION_SECURE"),
                         httponly=current_app.Config.get("SESSION_HTTPONLY"),
                         samesite=current_app.Config.get("SESSION_SAMESITE"),
                         )
        logger.info("save session")

    def has_storage(self, session_key):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def __setitem__(self, key, value):
        raise NotImplementedError

    def __getitem__(self, key):
        raise NotImplementedError


class MemorySession(SessionMix):

    def __init__(self, key=None):
        super().__init__(key)
        self._storage = {}

    def has_storage(self, session_key):
        return self._storage.get(session_key)

    def clear(self):
        if request.session in self._storage:
            del self._storage[request.session]

    def __setitem__(self, key, value):
        if request.session not in self._storage:
            self._storage[request.session] = dict()
        self._storage[request.session].update({key: value})

    def __getitem__(self, key):
        if request.session not in self._storage:
            return None
        return self._storage[request.session].get(key)


class SimpleRedisSession(SessionMix):

    def __init__(self,
                 key=None,
                 redis_host="localhost",
                 redis_port=6379,
                 redis_password=None,
                 redis_decode_responses=True):
        super().__init__(key)
        import redis
        self.redis = redis.Redis(host=redis_host,
                                 port=redis_port,
                                 password=redis_password,
                                 decode_responses=redis_decode_responses)

    def _get_key_by_request(self):
        return "%s_%s" % (self.get_session_key_name, request.session)

    def _get_key(self, key):
        return "%s_%s" % (self.get_session_key_name, key)

    # def _dump_object(self, k):
    #     return pickle.dumps(k) if k is not None else k

    # def _load_object(self, k):
    #     return pickle.loads(k) if k is not None else k

    def has_storage(self, session_key):
        return self.redis.exists(self._get_key(session_key))

    def clear(self):
        return super().clear()

    def __setitem__(self, key, value):
        self.redis.hset(self._get_key_by_request(),
                        key,
                        value)

    def __getitem__(self, key):
        value = self.redis.hget(self._get_key_by_request(),
                                key)
        return value
