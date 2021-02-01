import json
import pickle
from telethon import TelegramClient, sync
import asyncio
import csv

from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.channels import GetAdminLogRequest
from telethon.tl.functions.messages import GetHistoryRequest

from telethon.tl.types import InputChannel
from telethon.tl.types import ChannelAdminLogEventsFilter
from telethon.tl.types import InputUserSelf
from telethon.tl.types import InputUser

from credentials import *

client = TelegramClient(phone_number, api_id, api_hash).start()
# me = client.get_me()
# print(me.stringify())

telegramchanname = open('telegramchanname.txt').read().split()

telechanposts = []

for tn in telegramchanname:
    channel_username = tn
    try:
        channel_entity = client.get_entity(channel_username)
        posts = client(GetHistoryRequest(
            peer=channel_entity, limit=999,
            offset_date=None, offset_id=0, max_id=0,
            min_id=0, add_offset=0, hash=0))
        maxid = min(o.id for o in posts.messages)
        while maxid > 1:
            posts2 = client(GetHistoryRequest(
                peer=channel_entity, limit=999,
                max_id=maxid, offset_date=None, offset_id=maxid,
                min_id=0, add_offset=0, hash=0))
            posts.messages.extend(posts2.messages)
            maxid = min(o.id for o in posts.messages)
            print(tn + maxid.__str__())
        telechanposts.append(posts)
    except:
        continue

    print(tn)


with open('telechanposts.pickle', 'wb') as f:
    pickle.dump(telechanposts, f)

# with open('telechanposts.pickle', 'rb') as f:
#     telechanposts = pickle.load(f)


outposts = []
for p in telechanposts:
    for q in p.messages:
        outposts.append(
            [p.chats[0].id, p.chats[0].username, q.date.timestamp(), q.sender_id, q.post_author, q.message,
             q.views]
        )

with open('outposts.csv', 'w', encoding='utf8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['channel_id', 'channel_username', 'timestamp', 'sender_id', 'post_author', 'message',
                     'views'])
    writer.writerows(outposts)
