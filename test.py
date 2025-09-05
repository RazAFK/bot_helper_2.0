from db import *
from log import log_info, log_error
from errors import *

#create_db_and_tables()

#add_subject('geometry')
#update(Subject, Subject.id==1, {'id': 'MATH'}, 1)

rows_update(
    model = User,
    conditions= (User.id == 1),
    updates={'username': 'idiot'},
    max_rows=1
)
