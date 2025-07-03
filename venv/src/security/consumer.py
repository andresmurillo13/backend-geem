import asyncio
from hawk import Consumer

from security.callbacks import callback_send_message_rocket_chat

loop = asyncio.get_event_loop()


async def main():
    await Consumer.consume('send_message_alert', callback=callback_send_message_rocket_chat)

if __name__ == "__main__":
    loop.run_until_complete(main())
    loop.close()
