import sqlite3

import json
import threading
import time




# Устанавливаем соединение с базой данных
#us = sqlite3.connect('users.db')
#cs = us.cursor()
#cs.execute('''
#CREATE TABLE IF NOT EXISTS Users (
#id INTEGER PRIMARY KEY,
#username TEXT NOT NULL,
#class INTEGER NOT NULL
#)
#''')

#cs.execute('''
#CREATE TABLE IF NOT EXISTS Teachers (
#id INTEGER PRIMARY KEY,
#username TEXT NOT NULL,
#name TEXT NOT NULL,
#class INTEGER NOT NULL,
#subject TEXT NOT NULL
#)
#''')

#cs.execute('''
#CREATE TABLE IF NOT EXISTS Subjects (
#id INTEGER PRIMARY KEY,
#math BOOL NOT NULL,
#eng BOOL NOT NULL
#)
#''')

#cs.execute('SELECT math FROM Subjects WHERE math = 1')
#results = cs.fetchall()
#print(results[0][0])
#cs.execute('INSERT INTO Subjects (id, math) VALUES (?, ?)', (1234, 0))

#names = ['jack','jill','bill']
#snames = json.dumps(names)
#c.execute("INSERT INTO Teachers " + snames + ";")
#print(snames)

#cs.execute('INSERT INTO Users (id, username, class) VALUES (?, ?, ?)', (145145145, '@testus', 10))
#cs.execute('INSERT INTO Users (id, username, class) VALUES (?, ?, ?)', (145145145, '@testus', 11))
#cs.execute('INSERT INTO Subjects (id, math, eng) VALUES (?, ?, ?)', (1236, False, True))
#cs.execute('SELECT math FROM Subjects WHERE id=1235')
#print(type(cs.fetchall()[0][0]))
#cs.execute('UPDATE Users SET class = ? WHERE username = ?', (9, '@testus'))

#cs.execute('SELECT Subjects.math, Teachers.name FROM Subjects JOIN Teachers ON Subjects.id = Teachers.id')
#res = cs.fetchall()
#print(res)

#cs.execute('SELECT username, class FROM Users WHERE class >= ?', (10, ))
#results = cs.fetchall()

#for row in results:
#  print(list(row))


#cs.execute('DELETE FROM Users WHERE username = ? AND NOT class = ?', ('@testus', 1))

#subj = {'Рус': True, 'Алг': False, 'Физ': False}
#strsubj = json.dumps(subj)

#cs.execute('INSERT INTO Teachers (id, username, name, class, subject) VALUES (?, ?, ?, ?, ?)', (1235, '@testuser', 'testname', 11, 'abcd'))
#cs.execute('UPDATE Teachers SET class=?', (12, ))
#cs.execute('SELECT subject FROM Teachers')
#res = cs.fetchall()
#print(json.loads(res[0][0]))
class database:

    def __init__(self, db, debug=0):
        self.db = db
        self.debug = debug
        self.tabl = 'Users'
        #self.usr = sqlite3.connect(self.db, check_same_thread=False)
        self.lstorage = threading.local()

    def get_thread(self):
        if not(hasattr(self.lstorage, 'connection')):
            self.lstorage.connection = sqlite3.connect(self.db)
        return self.lstorage.connection

    def close_all(self):
        for attr in dir(self.lstorage):
            if isinstance(getattr(self.lstorage, attr), sqlite3.Connection):
                getattr(self.lstorage, attr).close()
    def init(self):
        us = self.get_thread()
        cs = us.cursor()
        cs.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY NOT NULL,
        username TEXT NOT NULL,
        name TEXT NOT NULL,
        class INTEGER NOT NULL,
        sch_id INTEGER NOT NULL,
        warn BOOL NOT NULL,
        havetheme BOOL NOT NULL
        )
        ''')

        cs.execute('''
        CREATE TABLE IF NOT EXISTS Teachers (
        id INTEGER PRIMARY KEY NOT NULL,
        username TEXT NOT NULL,
        name TEXT NOT NULL,
        class INTEGER NOT NULL,
        sch_id INTEGER NOT NULL,
        is_busy BOOL NOT NULL,
        is_confirmed BOOL NOT NULL,
        warn BOOL NOT NULL
        )
        ''')

        cs.execute('''
        CREATE TABLE IF NOT EXISTS Subjects (
        s_id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL UNIQUE
        )
        ''')

        cs.execute('''
        CREATE TABLE IF NOT EXISTS Themes (
        t_id INTEGER NOT NULL,
        u_id INTEGER NOT NULL,
        s_id INTEGER NOT NULL,
        theme TEXT,
        status BOOL NOT NULL,
        is_find BOOL NOT NULL
        )
        ''')
        
        cs.execute('''
        CREATE TABLE IF NOT EXISTS JoinedTS (
        t_id INTEGER NOT NULL,
        s_id INTEGER NOT NULL,
        UNIQUE(t_id, s_id)
        )
        ''')

        cs.execute('''
        CREATE TABLE IF NOT EXISTS Schools (
        sch_id INTEGER PRIMARY KEY AUTOINCREMENT,
        school TEXT NOT NULL UNIQUE
        )
        ''')

        cs.execute('''
        CREATE TABLE IF NOT EXISTS Admins (
        id INTEGER PRIMARY KEY NOT NULL
        )
        ''')

        us.commit()

    def insert(self, id, username, name, clas, school=1, warn=0, havetheme=0):
        us = self.get_thread()
        cs = us.cursor()
        if type(school) == str:
            cs.execute('SELECT sch_id FROM Schools WHERE school=?', (school, ))
            sch_id = cs.fetchall()[0][0]
        else:
            sch_id = school
        try:
            cs.execute(f'INSERT INTO {self.tabl} (id, username, name, class, sch_id, warn, havetheme) VALUES (?, ?, ?, ?, ?, ?, ?)',  (id, username, name, clas, sch_id, warn, havetheme))
            us.commit()
            return True
        except Exception as e:
            return e if self.debug else False

    def delete(self, id):
        try:
            us = self.get_thread()
            cs = us.cursor()
            cs.execute(f'DELETE FROM {self.tabl} WHERE {'id' if self.tabl=='Teachers' or self.tabl=='Users' or self.tabl=='Admins' else 's_id'}=?', (id, ))
            us.commit()
            return True
        except Exception as e:
            return e if self.debug else False
        
    def update(self, id, col, data):
        try:
            us = self.get_thread()
            cs = us.cursor()
            cs.execute(f'UPDATE {self.tabl} SET {col}=? WHERE id=?', (data, id, ))
            us.commit()
            return True
        except Exception as e:
            return e if self.debug else False
        
    def selectwhere(self, wherewhat, select='*', where='id'):
        try:
            us = self.get_thread()
            cs = us.cursor()
            cs.execute(f'SELECT {select} FROM {self.tabl} WHERE {where}=?', (wherewhat, ))
            result = cs.fetchall()
            us.commit()
            return result if len(result)>0 else None
        except Exception as e:
            return e if self.debug else False
    
    def selectall(self):
        try:
            us = self.get_thread()
            cs = us.cursor()
            cs.execute(f'SELECT * FROM {self.tabl}')
            result = cs.fetchall()
            #us.commit()
            return result if len(result)>0 else None
        except Exception as e:
            return e if self.debug else False


class user_database(database):
    def __init__(self, db, debug=0):
        self.db = db
        self.debug = debug
        self.tabl = 'Users'
        #self.usr = sqlite3.connect(self.db, check_same_thread=False)
        self.lstorage = threading.local()

class teachers_database(database):
    def __init__(self, db, debug=0):
        self.db = db
        self.debug = debug
        self.tabl = 'Teachers'
        #self.usr = sqlite3.connect(self.db, check_same_thread=False)
        self.lstorage = threading.local()

    def insert(self, id, username, name, clas, school=1, is_busy=1, is_confirmed=0, warn=0):
        us = self.get_thread()
        cs = us.cursor()
        if type(school) == str:
            cs.execute('SELECT sch_id FROM Schools WHERE school=?', (school, ))
            sch_id = cs.fetchall()[0][0]
            print('tch', sch_id)
        else:
            sch_id = school
        try:
            cs.execute(f'INSERT INTO {self.tabl} (id, username, name, class, sch_id, is_busy, is_confirmed, warn) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (id, username, name, clas, sch_id, is_busy, is_confirmed, warn))
            us.commit()
            return True
        except Exception as e:
            return e if self.debug else False
    
    
        
    def allteachers(self, is_confirmed):
        try:
            us = self.get_thread()
            cs = us.cursor()
            cs.execute('SELECT * FROM Teachers WHERE is_confirmed=?', (is_confirmed, ))
            result = cs.fetchall()
            us.commit()
            return result if len(result)>0 else None
        except Exception as e:
            return e if self.debug else False

class subjects_database(database):
    def __init__(self, db, debug=0):
        self.db = db
        self.debug = debug
        self.tabl = 'Subjects'
        #self.usr = sqlite3.connect(self.db, check_same_thread=False)
        self.lstorage = threading.local()

    def init(self):
        if self.debug:
            subj = ['Математика', 'Русский язык', 'Алгебра', 'Геометрия', 'Физика', 'Информатика', 'Химия', 'Биология', 'Английский язык', 'Обществознание']
            for item in subj:
                self.insert(item)
    
    def insert(self, subj):
        us = self.get_thread()
        cs = us.cursor()
        try:
            cs.execute(f'INSERT INTO {self.tabl} (s_id, subject) VALUES (NULL, ?)', (subj,))
            #cs.execute("INSERT INTO items (id, name) VALUES (NULL, ?)", (name,))
            us.commit()
            return True
        except Exception as e:
            return e if self.debug else False

class themes_database(database):
    def __init__(self, db, debug=0):
        self.db = db
        self.debug = debug
        self.tabl = 'Themes'
        #self.usr = sqlite3.connect(self.db, check_same_thread=False)
        self.lstorage = threading.local()
    
    def insert(self, t_id, u_id, s_id, theme='None', status=0, is_find=0):
        us = self.get_thread()
        cs = us.cursor()
        try:
            cs.execute(f'INSERT INTO {self.tabl} (t_id, u_id, s_id, theme, status, is_find) VALUES (?, ?, ?, ?, ?, ?)', (t_id, u_id, s_id, theme, status, is_find))
            us.commit()
            return True
        except Exception as e:
            return e if self.debug else False
        
    def update(self, id):
        us = self.get_thread()
        cs = us.cursor()
        try:
            cs.execute(f'UPDATE {self.tabl} SET status=0 WHERE (u_id=? OR t_id=?) AND status=1', (id, id))
            us.commit()
            return True
        except Exception as e:
            return e if self.debug else False
    
    def select_active(self, id):
        try:
            us = self.get_thread()
            cs = us.cursor()
            cs.execute(f'SELECT * FROM {self.tabl} WHERE status=1 AND is_find=1 AND (u_id=? OR t_id=?)', (id, id))
            result = cs.fetchall()
            us.commit()
            return result if len(result)>0 else None
        except Exception as e:
            return e if self.debug else False

class joinedts_database(database):
    def __init__(self, db, debug=0):
        self.db = db
        self.debug = debug
        self.tabl = 'JoinedTS'
        #self.usr = sqlite3.connect(self.db, check_same_thread=False)
        self.lstorage = threading.local()

    def insert(self, t_id, subject):
        us = self.get_thread()
        cs = us.cursor()
        if type(subject) == str:
            s_id = cs.execute(f'SELECT Subjects.s_id FROM Subjects WHERE Subjects.subject = ?', (subject, ))
            s_id = list(s_id)[0][0]
        else:
            s_id = subject
        try:
            cs.execute(f'INSERT INTO {self.tabl} (t_id, s_id) VALUES (?, ?)', (t_id, s_id))
            us.commit()
            return True
        except Exception as e:
            return e if self.debug else False
        
    def selectbytid(self, t_id):
        try:
            us = self.get_thread()
            cs = us.cursor()
            cs.execute(f'SELECT s.subject FROM Subjects s JOIN {self.tabl} ts ON s.s_id = ts.s_id WHERE ts.t_id=?', (t_id, ))
            result = cs.fetchall()
            us.commit()
            return result if len(result)>0 else None
        except Exception as e:
            return e if self.debug else False
        
    def delete(self, t_id, subject):
        us = self.get_thread()
        cs = us.cursor()
        if type(subject) == str:
            s_id = cs.execute(f'SELECT Subjects.s_id FROM Subjects WHERE Subjects.subject = ?', (subject, ))
            s_id = list(s_id)[0][0]
        else:
            s_id = subject
        try:
            cs.execute(f'DELETE FROM {self.tabl} WHERE t_id=? AND s_id=?', (t_id, s_id, ))
            us.commit()
            return True
        except Exception as e:
            return e if self.debug else False


class schools_database(database):
    def __init__(self, db, debug=0):
        self.db = db
        self.debug = debug
        self.tabl = 'Schools'
        #self.usr = sqlite3.connect(self.db, check_same_thread=False)
        self.lstorage = threading.local()

    def init(self):
        if self.debug:
            subj = ['МБОУ СОШ 6']
            for item in subj:
                self.insert(item)
    
    def insert(self, school):
        us = self.get_thread()
        cs = us.cursor()
        try:
            cs.execute(f'INSERT INTO {self.tabl} (sch_id, school) VALUES (NULL, ?)', (school,))
            #cs.execute("INSERT INTO items (id, name) VALUES (NULL, ?)", (name,))
            us.commit()
            return True
        except Exception as e:
            return e if self.debug else False

class admins_database(database):
    def __init__(self, db, debug=0):
        self.db = db
        self.debug = debug
        self.tabl = 'Admins'
        #self.usr = sqlite3.connect(self.db, check_same_thread=False)
        self.lstorage = threading.local()

    def init(self):
        if self.debug:
            subj = ['1634714523']
            for item in subj:
                self.insert(item)
    
    def insert(self, id):
        us = self.get_thread()
        cs = us.cursor()
        try:
            cs.execute(f'INSERT INTO {self.tabl} (id) VALUES (?)', (id,))
            #cs.execute("INSERT INTO items (id, name) VALUES (NULL, ?)", (name,))
            us.commit()
            return True
        except Exception as e:
            return e if self.debug else False
        
'''
udb = user_database('users.db', 1)
tdb = teachers_database('users.db', 1)
sdb = subjects_database('users.db', 1)
tmdb = themes_database('users.db', 1)
jdb = joinedts_database('users.db', 1)
sch = schools_database('users.db', 1)
adb = admins_database('users.db', 1)
''''''
udb.init()
tdb.init()
sdb.init()
tmdb.init()
jdb.init()
sch.init()
adb.init()
'''

#print(udb.insert(12345, '@testus', 'usname', 10, 'МБОУ СОШ 6'))
#print(tdb.insert(54321, '@testteach', 'teachname', 10, 1))
#jdb.insert(54321, 1)
#jdb.insert(54321, 9)
#tmdb.insert(54321, 12345, 9, 'Электростатика')


#'''
