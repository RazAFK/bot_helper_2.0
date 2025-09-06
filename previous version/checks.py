def is_in_users(message, db):
    user = db.selectwhere(message.chat.id, 'user')
    return 1 if user!=None else 0

def is_teacher(message, db):
    teacher = db.selectwhere(message.chat.id, 'teacher')
    return 1 if teacher!=None else 0 

def is_admin(message, db):
    admin = db.selectwhere(message.chat.id, 'admin')
    return 1 if admin!=None else 0

def is_in_diolog(message, db):
    theme = db.selectthemeactive(message.chat.id)
    return 1 if theme!=None else 0