import asyncio
import concurrent.futures
import requests
import os
from pyformance import counter, count_calls
from pyformance.registry import MetricsRegistry
import signalfx.pyformance

registry = MetricsRegistry()
counter = registry.counter("http_requests_sent")

token = ''

if 'SF_TOKEN' not in os.environ:
    token = os.environ['SF_TOKEN']

sfx = signalfx.pyformance.SignalFxReporter(token=os.environ['SF_TOKEN'],reporting_interval=1,registry=registry)

sfx.start()

async def main():

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        target = 'http://localhost:8901'
        if 'TARGET_ADDRESS' in os.environ:
            target = os.environ['TARGET_ADDRESS']

        print ('Sending data to ..',target)
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(
                executor,
                requests.get,
                target
            )
            for i in range(20)
        ]
        for response in await asyncio.gather(*futures):
            print (response.text)
            counter.inc()
while True:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
