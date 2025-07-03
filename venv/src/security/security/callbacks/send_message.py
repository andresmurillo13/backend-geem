from rocketchat.main import RocketChatBot

from security.settings import ROCKET_CHAT_CHANNEL_BLOCK_IP


async def callback_send_message_rocket_chat(data):
    message = data.get('message')
    if message:
        with RocketChatBot() as rocket_chat:
            rocket_chat.chat_post_message(text=message, channel=ROCKET_CHAT_CHANNEL_BLOCK_IP)
