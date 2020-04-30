from apis import local as api
from exceptions import LocalApi

longpoll_waiters = set()


class Waiter:
    def __init__(self, user_id):
        self.user_id = user_id
        self.updates = []


def notify_longpoll_requests(event):
    for waiter in longpoll_waiters:
        try:
            api.chats.check_user_in_chat(event['chat_id'], waiter.user_id)
        except (LocalApi.ForbiddenError, LocalApi.NotFoundError):
            pass
        else:
            waiter.updates.append(event)
