import unittest
from xq.message import Message
from datetime import timedelta, datetime

BODY = "body"

class TestMessage(unittest.TestCase):

    def test_serialization(self):
        msg = Message(BODY, 12, timedelta(days=2), datetime.now())
        j = msg.to_json()
        new_msg = Message.from_json(j)
        self.assertEqual(msg.id, new_msg.id)
        self.assertEqual(msg.body, new_msg.body)
        self.assertEqual(msg.timestamp, new_msg.timestamp)
        self.assertEqual(msg.run_every, new_msg.run_every)
