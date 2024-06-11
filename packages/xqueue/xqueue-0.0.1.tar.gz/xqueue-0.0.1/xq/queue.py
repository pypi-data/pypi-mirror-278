import logging
from datetime import datetime
from xq.message import Message

XQ_STORAGE_PREFIX = "xq_prefix_"
BATCH_POLL_COUNT = 5

logger = logging.getLogger(__name__)

class Queue:
    def __init__(self, redis, queue_name="default"):
        self.redis = redis
        self.queue_name = XQ_STORAGE_PREFIX + queue_name
        self.next_run_timestamp = None

    def enqueue(self, body, run_at=None, run_every=None, run_whenever_at=None):
        if not isinstance(body, str) and not isinstance(body, bytes):
            raise TypeError("invalid body type, please use str type")
        now_timestamp = datetime.now().timestamp()
        timestamp = 0
        if run_every:
            pass
        elif run_at:
            timestamp = run_at.timestamp()
            if timestamp < now_timestamp:
                logger.error("cannot schedule task happened at past")
                return
        elif run_whenever_at:
            pass
        else: # run immediately and only once
            pass

        msg = Message(body, timestamp, run_every, run_whenever_at)
        self.redis.zadd(self.queue_name, {msg.to_json(): timestamp})

    def poll(self):
        now_timestamp = datetime.now().timestamp()
        keep_poll = True
        messages_to_process = []
        while keep_poll:
            messages = self.redis.zrange(self.queue_name, 0, BATCH_POLL_COUNT, withscores=True)
            logger.debug(f"polled {len(messages)} messages")
            if len(messages) == 0:
                break
            for message in messages:
                msg_str, timestamp = message
                msg = Message.from_json(msg_str)
                if msg.timestamp > now_timestamp: # not ready to process
                    keep_poll = False
                else:
                    self.redis.zrem(self.queue_name, msg_str)
                    messages_to_process.append(msg)

        self._re_enqueue(messages_to_process)
        return messages_to_process

    def _re_enqueue(self, msgs):
        msgs_to_enqueue = []
        for msg in msgs:
            if msg.run_every:
                msg.timestamp = datetime.fromtimestamp(msg.timestamp) + msg.run_every
                msgs_to_enqueue.append(msg)
            elif msg.run_whenever_at:
                pass
            else:
                pass
        for msg in msgs_to_enqueue:
            self.redis.zadd(self.queue_name, {msg.to_json(): msg.timestamp})

    def _next_timestamp(self, msg):
        pass

