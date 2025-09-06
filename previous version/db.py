import sqlite3
import threading
import datetime

class data_base:
    def __init__(self, db, debug=0):
        self.db = db
        self.debug = debug
        self.lstorage = threading.local()
        self.tabl = {'user': 'Users', 'teacher': 'Teachers', 'subject': 'Subjects', 'theme': 'Themes', 'joinTS': 'JoinedTS', 'school': 'Schools', 'admin': 'Admins', 'time': 'EnterTime'}
        self.userstatus = {}
        self.is_writing = {}
        self.subjecttheme = {}

    def get_connection(self):
        if not hasattr(self.lstorage, 'conn'):
            self.lstorage.conn = sqlite3.connect('users.db')
        return self.lstorage.conn
    
    def close_connections(self):
        if hasattr(self.lstorage, 'conn'):
            self.lstorage.conn.close()
    
    def init(self):
        us = self.get_connection()
        cs = us.cursor()
        #Users
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
        #Teachers
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
        #Subjects
        cs.execute('''
        CREATE TABLE IF NOT EXISTS Subjects (
        s_id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL UNIQUE
        )
        ''')
        #Themes
        cs.execute('''
        CREATE TABLE IF NOT EXISTS Themes (
        t_id INTEGER NOT NULL,
        u_id INTEGER NOT NULL,
        s_id INTEGER NOT NULL,
        theme TEXT,
        is_active BOOL NOT NULL,
        datetimestart TEXT NOT NULL,
        datetimeanswer TEXT NOT NULL,
        datetimeend TEXT NOT NULL
        )
        ''')#
        #JoinedTS
        cs.execute('''
        CREATE TABLE IF NOT EXISTS JoinedTS (
        t_id INTEGER NOT NULL,
        s_id INTEGER NOT NULL,
        UNIQUE(t_id, s_id)
        )
        ''')
        #Schools
        cs.execute('''
        CREATE TABLE IF NOT EXISTS Schools (
        sch_id INTEGER PRIMARY KEY AUTOINCREMENT,
        school TEXT NOT NULL UNIQUE
        )
        ''')
        #Admins
        cs.execute('''
        CREATE TABLE IF NOT EXISTS Admins (
        id INTEGER PRIMARY KEY NOT NULL
        )
        ''')
        #EnterTime
        cs.execute('''
        CREATE TABLE IF NOT EXISTS EnterTime (
        id INTEGER PRIMARY KEY NOT NULL,
        datetime INTEGER NOT NULL
        )
        ''')

        if self.debug:
            subjects = ['Математика', 'Русский язык', 'Алгебра', 'Геометрия', 'Физика', 'Информатика', 'Химия', 'Биология', 'Английский язык', 'Обществознание']
            for item in subjects:
                self.insertSubject(item)
            schools = ['МБОУ СОШ 6']
            for item in schools:
                self.insertSchool(item)
            admins = ['1634714523', '994452801']
            for item in admins:
                self.insertAdmin(item)

        us.commit()
#inserts
    def insertUser(self, id, username, name, clas, school=1, warn=0, havetheme=0):
        tabl = self.tabl['user']
        us = self.get_connection()
        cs = us.cursor()
        if type(school) == str:
            cs.execute('SELECT sch_id FROM Schools WHERE school=?', (school, ))
            sch_id = cs.fetchall()[0][0]
        else:
            sch_id = school
        try:
            cs.execute(f'INSERT INTO {tabl} (id, username, name, class, sch_id, warn, havetheme) VALUES (?, ?, ?, ?, ?, ?, ?)',  (id, username, name, clas, sch_id, warn, havetheme))
            us.commit()
            return True
        except Exception as e:
            return e if self.debug else False

    def insertTeacher(self, id, username, name, clas, school=1, is_busy=1, is_confirmed=0, warn=0):
        tabl = self.tabl['teacher']
        us = self.get_connection()
        cs = us.cursor()
        if type(school) == str:
            cs.execute('SELECT sch_id FROM Schools WHERE school=?', (school, ))
            sch_id = cs.fetchall()[0][0]
            print('tch', sch_id)
        else:
            sch_id = school
        try:
            cs.execute(f'INSERT INTO {tabl} (id, username, name, class, sch_id, is_busy, is_confirmed, warn) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (id, username, name, clas, sch_id, is_busy, is_confirmed, warn))
            us.commit()
            return True
        except Exception as e:
            return e if self.debug else False
        
    def insertSubject(self, subj):
        tabl = self.tabl['subject']
        us = self.get_connection()
        cs = us.cursor()
        try:
            cs.execute(f'INSERT INTO {tabl} (s_id, subject) VALUES (NULL, ?)', (subj,))
            #cs.execute("INSERT INTO items (id, name) VALUES (NULL, ?)", (name,))
            us.commit()
            return True
        except Exception as e:
            return e if self.debug else False
        
    def insertTheme(self, u_id, s_id, t_id=0, theme='None', is_active=0, datetime='0-0-0 0:0:0.0'):
        tabl = self.tabl['theme']
        us = self.get_connection()
        cs = us.cursor()
        try:
            cs.execute(f'INSERT INTO {tabl} (t_id, u_id, s_id, theme, is_active, datetimestart, datetimeanswer, datetimeend) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (t_id, u_id, s_id, theme, is_active, datetime, datetime, datetime))
            us.commit()
            return True
        except Exception as e:
            return e if self.debug else False
        
    def insertJoinTS(self, t_id, subject):
        tabl = self.tabl['joinTS']
        us = self.get_connection()
        cs = us.cursor()
        if type(subject) == str:
            s_id = cs.execute(f'SELECT Subjects.s_id FROM Subjects WHERE Subjects.subject = ?', (subject, ))
            s_id = list(s_id)[0][0]
        else:
            s_id = subject
        try:
            cs.execute(f'INSERT INTO {tabl} (t_id, s_id) VALUES (?, ?)', (t_id, s_id))
            us.commit()
            return True
        except Exception as e:
            return e if self.debug else False
        
    def insertSchool(self, school):
        tabl = self.tabl['school']
        us = self.get_connection()
        cs = us.cursor()
        try:
            cs.execute(f'INSERT INTO {tabl} (sch_id, school) VALUES (NULL, ?)', (school,))
            #cs.execute("INSERT INTO items (id, name) VALUES (NULL, ?)", (name,))
            us.commit()
            return True
        except Exception as e:
            return e if self.debug else False

    def insertAdmin(self, id):
        tabl = self.tabl['admin']
        us = self.get_connection()
        cs = us.cursor()
        try:
            cs.execute(f'INSERT INTO {tabl} (id) VALUES (?)', (id,))
            #cs.execute("INSERT INTO items (id, name) VALUES (NULL, ?)", (name,))
            us.commit()
            return True
        except Exception as e:
            return e if self.debug else False

    def insertEnterTime(self, id):
        tabl = self.tabl['time']
        us = self.get_connection()
        cs = us.cursor()
        dt = str(datetime.datetime.now())
        try:
            cs.execute(f'INSERT INTO {tabl} (id, datetime) VALUES (?, ?)', (id, dt))
            #cs.execute("INSERT INTO items (id, name) VALUES (NULL, ?)", (name,))
            us.commit()
            return True
        except Exception as e:
            return e if self.debug else False
#deletes
    def delete(self, id, tab=['user', 'teacher', 'subject', 'theme', 'joinTS', 'school', 'admin']):
        tabl = self.tabl[tab]
        us = self.get_connection()
        cs = us.cursor()
        if tabl=='Teachers' or tabl=='Users' or tabl=='Admins':
            sid = 'id'
        elif tabl=='JoinedTS':
            sid = 't_id'
        else:
            sid = 's_id'
        try:
            cs.execute(f'DELETE FROM {tabl} WHERE {sid}=?', (id, ))
            us.commit()
            return True
        except Exception as e:
            return e if self.debug else False
    
    def deleteJoinTS(self, t_id, subject):
        tabl = self.tabl['joinTS']
        us = self.get_connection()
        cs = us.cursor()
        if type(subject) == str:
            s_id = cs.execute(f'SELECT Subjects.s_id FROM Subjects WHERE Subjects.subject = ?', (subject, ))
            s_id = list(s_id)[0][0]
        else:
            s_id = subject
        try:
            cs.execute(f'DELETE FROM {tabl} WHERE t_id=? AND s_id=?', (t_id, s_id, ))
            us.commit()
            return True
        except Exception as e:
            return e if self.debug else False

    def deletethemefind(self, id):
        tabl = self.tabl['theme']
        us = self.get_connection()
        cs = us.cursor()
        try:
            cs.execute(f'DELETE FROM {tabl} WHERE t_id=0 AND u_id=?', (id, ))
            us.commit()
            return True
        except Exception as e:
            return e if self.debug else False
#updates
    def update(self, id, col, data, tab=['user', 'teacher', 'subject', 'theme', 'joinTS', 'school', 'admin']):
        tabl = self.tabl[tab]
        us = self.get_connection()
        cs = us.cursor()
        try:
            cs.execute(f'UPDATE {tabl} SET {col}=? WHERE id=?', (data, id, ))
            us.commit()
            return True
        except Exception as e:
            return e if self.debug else False

    def updateThemesDT(self, u_id, action=['start', 'answer', 'end'], t_id=0):
        tabl = self.tabl['theme']
        us = self.get_connection()
        cs = us.cursor()
        dt = str(datetime.datetime.now())
        try:
            if action=='start':
                cs.execute(f'UPDATE {tabl} SET datetime{action}=? WHERE (u_id=?) AND t_id=0', (dt, u_id))
                us.commit()
                return True
            elif action=='answer':
                cs.execute(f'UPDATE {tabl} SET datetime{action}=? WHERE (u_id=? AND t_id=?) AND is_active=1 AND datetimeanswer=?', (dt, u_id, t_id, '0-0-0 0:0:0.0', ))
                us.commit()
                return True
            else:
                cs.execute(f'UPDATE {tabl} SET datetime{action}=? WHERE (u_id=? OR t_id=?) AND NOT(t_id=0) AND is_active=0 AND datetimeend=?', (dt, u_id, u_id, '0-0-0 0:0:0.0'))
                us.commit()
                return True
        except Exception as e:
            return e if self.debug else False

    def updatefindingTheme(self, u_id, t_id):
        tabl = self.tabl['theme']
        us = self.get_connection()
        cs = us.cursor()
        try:
            cs.execute(f'UPDATE {tabl} SET is_active=1 WHERE t_id=0 AND u_id=?', (u_id, ))
            cs.execute(f'UPDATE {tabl} SET t_id=? WHERE t_id=0 AND u_id=?', (t_id, u_id, ))
            us.commit()
            return True
        except Exception as e:
            return e if self.debug else False

    def updatethemeend(self, u_id):
        tabl = self.tabl['theme']
        us = self.get_connection()
        cs = us.cursor()
        try:
            cs.execute(f'UPDATE {tabl} SET is_active=0 WHERE (t_id=? OR u_id=?) and NOT(t_id=0)', (u_id, u_id, ))
            us.commit()
            return True
        except Exception as e:
            return e if self.debug else False
#selects        
    def selectall(self, tab=['user', 'teacher', 'subject', 'theme', 'joinTS', 'school', 'admin']):
        tabl = self.tabl[tab]
        us = self.get_connection()
        cs = us.cursor()
        try:
            cs.execute(f'SELECT * FROM {tabl}')
            result = cs.fetchall()
            #us.commit()
            return result if len(result)>0 else None
        except Exception as e:
            return e if self.debug else False
        
    def selectwhere(self, wherewhat, tab=['user', 'teacher', 'subject', 'theme', 'joinTS', 'school', 'admin'], select='*', where='id'):
        tabl = self.tabl[tab]
        us = self.get_connection()
        cs = us.cursor()
        if tab=='teacher' and select=='name' and wherewhat==0:
            return ['Не найден']
        try:
            cs.execute(f'SELECT {select} FROM {tabl} WHERE {where}=?', (wherewhat, ))
            result = cs.fetchall()
            us.commit()
            return result if len(result)>0 else None
        except Exception as e:
            return e if self.debug else False
        
    def selectteachersconfirmed(self, is_confirmed):
        tabl = self.tabl['teacher']
        us = self.get_connection()
        cs = us.cursor()
        try:
            cs.execute(f'SELECT * FROM {tabl} WHERE is_confirmed=?', (is_confirmed, ))
            result = cs.fetchall()
            us.commit()
            return result if len(result)>0 else None
        except Exception as e:
            return e if self.debug else False
    
    def selectteacheractive(self):
        tabl = self.tabl['teacher']
        us = self.get_connection()
        cs = us.cursor()
        try:
            cs.execute(f'SELECT * FROM {tabl} WHERE is_busy=0', ())
            result = cs.fetchall()
            us.commit()
            return result if len(result)>0 else None
        except Exception as e:
            return e if self.debug else False
        
    def selectthemeactive(self, id):
        tabl = self.tabl['theme']
        us = self.get_connection()
        cs = us.cursor()
        try:
            cs.execute(f'SELECT * FROM {tabl} WHERE is_active=1 AND (u_id=? OR t_id=?)', (id, id))
            result = cs.fetchall()
            us.commit()
            return result if len(result)>0 else None
        except Exception as e:
            return e if self.debug else False
    
    def selectthemeall(self, activity):
        tabl = self.tabl['theme']
        us = self.get_connection()
        cs = us.cursor()
        try:
            if activity==1 or activity==0:
                cs.execute(f'SELECT * FROM {tabl} WHERE is_active=? AND NOT(t_id=0)', (activity, ))
            else:
                cs.execute(f'SELECT * FROM {tabl} WHERE t_id=0', ())
            result = cs.fetchall()
            return result if len(result)>0 else None
        except Exception as e:
            return e if self.debug else False

    def selectthemefind(self):
        tabl = self.tabl['theme']
        us = self.get_connection()
        cs = us.cursor()
        try:
            cs.execute(f'SELECT * FROM {tabl} WHERE t_id=0', ())
            result = cs.fetchall()
            return result if len(result)>0 else None
        except Exception as e:
            return e if self.debug else False
    
    def selectthemefindbyid(self, id):
        tabl = self.tabl['theme']
        us = self.get_connection()
        cs = us.cursor()
        try:
            cs.execute(f'SELECT * FROM {tabl} WHERE t_id=0 AND u_id=?', (id, ))
            result = cs.fetchall()
            return result if len(result)>0 else None
        except Exception as e:
            return e if self.debug else False
        
    def selectteacherssubjects(self, t_id):
        tabl = self.tabl['joinTS']
        us = self.get_connection()
        cs = us.cursor()
        try:
            cs.execute(f'SELECT s.subject FROM Subjects s JOIN {tabl} ts ON s.s_id = ts.s_id WHERE ts.t_id=?', (t_id, ))
            result = cs.fetchall()
            return result if len(result)>0 else None
        except Exception as e:
            return e if self.debug else False
    
    def selectactivethemebyid(self, id):
        tabl = self.tabl['theme']
        us = self.get_connection()
        cs = us.cursor()
        try:
            cs.execute(f'SELECT * FROM {tabl} WHERE (t_id=? OR u_id=?) AND is_active=1', (id, id, ))
            result = cs.fetchall()
            return result if len(result)>0 else None
        except Exception as e:
            return e if self.debug else False