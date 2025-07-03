from hawk import Publisher

from security.settings import NAME_ENV


async def send_message_alert(message: str):
    async with Publisher() as publisher:
        message += f' - SERVER: {NAME_ENV}'
        await publisher.send_message('send_message_alert', data={'message': message})
