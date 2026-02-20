import asyncio
import websockets
import json

async def test():
    uri = "ws://localhost:8001/ws/stats"
    try:
        async with websockets.connect(uri) as websocket:
            print("[*] Connected to WebSocket.")
            while True:
                msg = await websocket.recv()
                data = json.loads(msg)
                print(f"[*] Received stats: is_active={data.get('is_active')}, total_packets={data.get('total_packets')}")
                if data.get('is_active'):
                    print("[+] System IS ACTIVE!")
                    break
    except Exception as e:
        print(f"[!] WebSocket Error: {e}")

if __name__ == "__main__":
    asyncio.run(test())
