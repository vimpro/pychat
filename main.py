import asyncio
import websockets
import json
import pathlib
import ssl
import datetime

CONNECTIONS = set()

def log(event, time):
    with open("log.txt", "+a") as myfile:
        myfile.write(f"{time}: {event}\n")

async def handler(websocket):
    CONNECTIONS.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            log(data, datetime.datetime.now())
            websockets.broadcast(CONNECTIONS, json.dumps(data))
        await websocket.wait_closed()
    finally:
        CONNECTIONS.remove(websocket)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(
    certfile='/etc/letsencrypt/live/compscichat.tk/fullchain.pem', 
    keyfile="/etc/letsencrypt/live/compscichat.tk/privkey.pem")

async def main():
    async with websockets.serve(handler, "", 8080, ssl=ssl_context):
        await asyncio.Future()

asyncio.run(main())