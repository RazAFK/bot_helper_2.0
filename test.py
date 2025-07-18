from db import *
from log import log_info, log_error

create_db_and_tables()

log_info('sucks')

try:
    add_subject('math')
except Exception as ex:
    log_error(ex)
