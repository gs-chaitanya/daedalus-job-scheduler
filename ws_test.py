import asyncio
import websockets
import json

async def listen_to_websocket():
    uri = "ws://localhost:8888/ws/jobs"

    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to WebSocket server!")

                while True:
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=10)  # wait for new messages, max 10s
                        job_update = json.loads(message)
                        print("Received job update:", json.dumps(job_update, indent=2))
                    except asyncio.TimeoutError:
                        print("No job update received in the last 10 seconds.")
        except Exception as e:
            print(f"Connection error: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(listen_to_websocket())
