import pymysql

class DBConnect:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='root', db='moon', charset='utf8mb4')
        self.curs = self.conn.cursor(pymysql.cursors.DictCursor)

    def select_list(self):
        ret = []
        try:
            sql = """select texts from text_youtube"""
            self.curs.execute(sql)
            youtube = self.curs.fetchall()
            for idx in youtube:
                ret.append(idx["texts"])
            return ret
        except Exception as e:
            print(e)
            pass

    def insert_ndsl(self, ndsl_list):
        try:
            sql = """insert into ndsl (title, link, abstract) 
                     values (%s, %s, %s)"""
            for v in ndsl_list:
                self.curs.execute(sql, v[0], v[1], v[2])
            self.conn.commit()    
        except Exception as e:
            print(e)
            pass
    
    def insert_detail(self, detail_list):
        try:
            sql = """insert into ndsl (author, content) 
                     values (%s, %s)"""
            for v in detail_list:
                self.curs.execute(sql, v[0], v[1])
            self.conn.commit()    
        except Exception as e:
            print(e)
            pass

    def db_close(self):
        self.conn.close()