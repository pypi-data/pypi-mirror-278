import unittest
from xq.message import Message
from xq.queue import Queue
from datetime import timedelta, datetime

BODY = "body"

class FakeRedis:
    def __init__(self):
        self.q = {}

    def zadd(self, queue, payload):
        self.q.setdefault(queue, [])
        for k in payload:
            self.q[queue].append((k, payload[k]))

    def zrange(self, queue_name, start, poll_count, withscores=True):
        return self.q[queue_name] 

    def zrem(self, queue_name, data):
        self.q[queue_name].remove(data)


class TestQueue(unittest.TestCase):

    def test_enqueue_deque_no_time(self):
        redis = FakeRedis()
        q = Queue(redis)
        q.enqueue(BODY)
        out = q.poll()
        self.assertEqual(1, len(out))
        self.assertEqual(BODY, out[0].body)
        out = q.poll()
        self.assertEqual(0, len(out))
    
        

if __name__ == '__main__':
    unittest.main()
