from unconscious import _unconscious
import asyncio
import threading
import asyncio


async def async_rust_server():
    await _unconscious.rust_server()


def rust_server_cli():
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_rust_server())


class Client:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.run_server)
        self.thread.start()

    def run_server(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.main())

    async def main(self):
        await _unconscious.rust_server()

    def stop(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()
