import MySQLdb as mdb
import sys

class DatabaseCon(object):

    def __init__(self, localhost, user, pwd, db_name):
        try:
            self.con = mdb.connect(localhost, user, pwd, db_name)
            self.cur = self.con.cursor()
        except mdb.Error, e:
            print "Cannot initialize database"

    def add_user(self, n, u, i):
        d = "INSERT INTO users(name, username, info) VALUES('{}', '{}', '{}')".format(n, u, i)
        self.cur.execute(d)
        self.con.commit()
        
    def add_circuit(self, n, ds, df):
        d = "INSERT INTO circuits(name, description, difficulty) VALUES('{}', '{}', '{}')".format(n, ds, df)
        self.cur.execute(d)
        self.con.commit()
    
    def add_race(self, c, u1, u2, t1, t2):
        d = "INSERT INTO races(circuit, user1, user2, time1, time2) VALUES('{}', '{}', '{}', '{}', '{}')".format(c, u1, u2, t1, t2)
        print d
        self.cur.execute(d)
        self.con.commit()

    def add_lap(self, r, l, t1, t2):
        d = "INSERT INTO laps(race, lap_num, time1, time2) VALUES('{}', '{}', '{}', '{}')".format(r, l, t1, t2)
        self.cur.execute(d)
        self.con.commit()

    def get_users(self):
        self.cur.execute("SELECT * from users")
        return self.cur.fetchall()

    def get_circuits(self):
        self.cur.execute("SELECT * from circuits")
        return self.cur.fetchall()

    def get_races(self):
        self.cur.execute("SELECT * from races")
        return self.cur.fetchall()

    def get_laps(self):
        self.cur.execute("SELECT * from laps")
        return self.cur.fetchall()

    def get_last_race(self):
        self.cur.execute("SELECT * from races ORDER BY race_id desc LIMIT 1")
        return self.cur.fetchall()
        
    def get_race_laps(self, race_id):
        d = "SELECT * from laps WHERE race = '{}'".format(race_id)
        self.cur.execute(d)
        return self.cur.fetchall()

    def get_user_races(self, user_id):
        d = "SELECT * from races WHERE user1 = '{}' or user2 = '{}'".format(user_id, user_id)
        self.cur.execute(d)
        return self.cur.fetchall()
    
    def get_user_data(self, user_id):
        d = "SELECT * from users WHERE user_id = '{}'".format(user_id)
        self.cur.execute(d)
        return self.cur.fetchall()
    
    def get_user_from_name(self, name):
        d = "SELECT * from users WHERE name = '{}'".format(name)
        self.cur.execute(d)
        return self.cur.fetchall()
        
    def get_user_rank(self, user_id):
        self.cur.execute("SELECT * FROM users ORDER BY win_count")
        data = self.cur.fetchall()
        count = 0
        for user in data:
            if int(user[0]) == int(user_id):
                return (count, len(data)) 
            count += 1
        return (0,0)

    def get_circuit(self, name):
        d = "SELECT * from circuits WHERE name = '{}'".format(name)
        self.cur.execute(d)
        return self.cur.fetchall()
    
                
    def close_con(self):
        if self.con:    
            self.con.close()


    def delete_data_from_table(self, table):
        d = "DELETE FROM {}".format(table)
        self.cur.execute(d)
