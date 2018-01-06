import asyncio
import concurrent.futures
import requests
import os

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
while True:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
