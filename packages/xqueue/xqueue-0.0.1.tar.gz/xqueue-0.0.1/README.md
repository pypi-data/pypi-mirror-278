# xq
A distributed queue system built on top of Redis

# install
```bash
pip3 install -r requirements.txt
```

# Use
## Producer
```python
import redis
from xq.queue import Queue

# connect to Redis
r = redis.Redis(host='localhost', port=6379)
# create queue
q = Queue(r, "test_queue")
# enqueue
q.enqueue("this is a message")
```

## Consumer
```python
import redis
from xq.queue import Queue

# connect to Redis
r = redis.Redis(host='localhost', port=6379)
# create queue
q = Queue(r, "test_queue")
# poll
messages = q.poll()
for message in messages:
    print(message.body)
```

## Use Worker
```python
import redis
from xq.queue import Queue
from xq.worker import Worker

# connect to Redis
r = redis.Redis(host='localhost', port=6379)
# create queue
q = Queue(r, "test_queue")
worker = Worker(q, process_message)
worker.run()

def process_message(message):
    print(message)
```
