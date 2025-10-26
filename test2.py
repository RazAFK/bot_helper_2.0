from temp_db import select_message, Message, add_message
from datetime import datetime, timedelta

#add_message(4, 0, 2, {'text': 'wep'}, 1, 0)
#print(datetime.now())
print(select_message((Message.receiver==2) & (Message.send_time>=('2025-10-26 16:32:53.412133'))))