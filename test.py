from db import *
from temp_db import *
import db, temp_db
from log import log_info, log_error, log_temp, log_temp_error
from errors import *

#create_db_and_tables()

#add_subject('geometry')
#update(Subject, Subject.id==1, {'id': 'MATH'}, 1)
#temp_db.create_db_and_tables()
#print(add_message(1, 0, 1, {"text":{"text": "abcd","message_id": 123}, "photo":{"id": "123asd"}}))
print(select_message(Message.id==1)[0].content.text)