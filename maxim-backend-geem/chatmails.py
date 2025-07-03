import asyncio

from geem.utils.emails import createMail

from geem import run
from geem.models import ModelChat, ModelRequest, ModelUser



def parsing_message(rows: list):
    message = ''
    for row in rows:
        message += f'<li>{row}</li>'
    return message


async def main():
    await run()
    senders = {}
    chats = await ModelChat.filter(is_send=False)
    for chat in chats:
        request: ModelRequest = await chat.request
        user: ModelUser = await request.user
        chat_user: ModelUser = await chat.user
        identifier = f'{request.id}{chat_user.id}'
        row = f'{request.id} - {request.title}'
        if not senders.get(identifier):
            if user.id != chat_user.id:
                senders[identifier] = {
                    'emails': [user.email],
                    'rows': [row]
                }
            else:
                users = await ModelUser.filter(company=1)
                emails = []
                for user in users:
                    emails.append(user.email)
                senders[identifier] = {
                    'emails': emails,
                    'rows': [row]
                }
        chat.is_send = True
        await chat.save()
    for key in senders.keys():
        message = f'Hola, <br><br>'
        message += f'Esta es una notificación de la plataforma de meneses, usted tiene nuevos mensajes de chat para las solicitudes:<br><br>'
        message += '<ul>'
        message += parsing_message(rows=senders[key]['rows'])
        message += '</ul>'
        emails = senders[key]['emails']
        for email in emails:
            send_email(email=email, message=message)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()