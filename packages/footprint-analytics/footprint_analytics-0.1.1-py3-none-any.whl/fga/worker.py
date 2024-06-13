import json
from concurrent.futures import ThreadPoolExecutor
from threading import Thread, RLock

from fga.exception import InvalidAPIKeyError
from fga.http_client import HttpClient
from fga.processor import ResponseProcessor
from fga.constants import DEFAULT_HEADER


class Workers:

    def __init__(self):
        self.threads_pool = ThreadPoolExecutor(max_workers=16)
        self.is_active = True
        self.consumer_lock = RLock()
        self.is_started = False
        self.configuration = None
        self.storage = None
        self.response_processor = ResponseProcessor()

    def setup(self, configuration, storage):
        self.configuration = configuration
        self.storage = storage
        self.response_processor.setup(configuration, storage)

    def start(self):
        with self.consumer_lock:
            if not self.is_started:
                self.is_started = True
                consumer = Thread(target=self.buffer_consumer)
                consumer.start()

    def stop(self):
        self.flush()
        self.is_active = False
        self.is_started = True
        self.threads_pool.shutdown()

    def flush(self):
        events = self.storage.pull_all()
        if events:
            return self.threads_pool.submit(self.send, events)

    def send(self, events):
        url = self.configuration.server_url
        print('url', url)
        payload = self.get_payload(events)
        print('payload', payload)
        DEFAULT_HEADER["token"] = self.configuration.api_key
        DEFAULT_HEADER["project-id"] = self.configuration.project_id
        res = HttpClient.post(url, payload, header=DEFAULT_HEADER)
        print('Send Res', res.body)

        try:
            self.response_processor.process_response(res, events)
        except InvalidAPIKeyError as  e:
            print('InvalidAPIKeyError', e)
            self.configuration.logger.error("Invalid API Key")

    def get_payload(self, events) -> bytes:
        payload_body = []
        for event in events:
            event_body = event.get_event_body()
            if event_body:
                payload_body.append(event_body)
        # if self.configuration.options:
        #     payload_body["options"] = self.configuration.options
        return json.dumps(payload_body, sort_keys=True).encode('utf8')

    def buffer_consumer(self):
        try:
            if self.is_active:
                with self.storage.lock:
                    self.storage.lock.wait(self.configuration.flush_interval_millis / 1000)
                    while True:
                        if not self.storage.total_events:
                            break
                        events = self.storage.pull(self.configuration.flush_queue_size)
                        if events:
                            self.threads_pool.submit(self.send, events)
                        else:
                            wait_time = self.storage.wait_time / 1000
                            if wait_time > 0:
                                self.storage.lock.wait(wait_time)
        except Exception:
            self.configuration.logger.exception("Consumer thread error")
        finally:
            with self.consumer_lock:
                self.is_started = False
