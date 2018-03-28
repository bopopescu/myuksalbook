import pymysql
import datetime
from model.pageVO import PageVO
from model.boardVO import BoardVO
import base64
import sys

class PageDao:

    def __init__(self):
        con = pymysql.connect(host='localhost', user='myuksal', password='myuksal',
                              db='account', charset="utf8")
        print('db연결 시작')
        self.con = con
        print('db연결')
        cus = con.cursor(pymysql.cursors.DictCursor)
        self.cus = cus

        self.sql_insert = "insert into members VALUES (%s,%s,password(%s),%s,%s,now())"
        self.sql_select_all = "select * from members"
        self.sql_select_id = "select * from members where id = %s"
        print('성공')


    def login(self,vo):
        print('로그인 시작')
        sql = "select no,id from members where id = %s and pwd = password(%s)"

        try:
            self.cus.execute(sql, (vo.user_id, vo.user_pw))
            ansor = self.cus.fetchall()
            print(ansor)

            return ansor
        except:
            return '테스트 : 로그인 실패'



    def new_account(self, vo):
        self.d_vo = vo

        print('입력 시작')
        print(self.sql_insert)

        user_no_b = "" + self.d_vo.user_email + "" + self.d_vo.user_id
        print(user_no_b)
        user_no_b = user_no_b.encode('utf-8')
        user_no = base64.b64encode(user_no_b)
        user_no = user_no.decode('utf-8')
        print(user_no)

        self.cus.execute(self.sql_insert, (user_no,self.d_vo.user_id, self.d_vo.user_pw, self.d_vo.user_email, self.d_vo.user_p_num))
        print('sql')
        self.con.commit()
        self.con.close()
        print('성공')




    def new_board(self, vo):
        print('글 등록 시작')
        sql = "insert into board values(NULL, %s, %s, %s, %s, %s, 0, now())"
        self.cus.execute(sql, (vo.no, vo.user, vo.title, vo.content, vo.file))
        self.con.commit()
        self.cus.close()
        self.con.close()


    def select_board(self, page):
        sql = "select * from board ORDER BY board_num DESC LIMIT " + page + ",1"
        self.cus.execute(sql)


        result = self.cus.fetchall()



        return result[0]



    def select_board2(self):
        sql = "select * from board order by board_num"
        self.cus.execute(sql)

        return  self.cus.fetchall()

    def count_board(self):
        sql = "select count(board_num) from board"
        self.cus.execute(sql)
        o = self.cus.fetchall()
        t = o[0]
        th = t['count(board_num)']
        return th


    def user_info(self, user, no):
        sql = "select id,email,p_num,join_date from members WHERE id = %s and no = %s"

        self.cus.execute(sql,(user,no))
        o = self.cus.fetchall()
        t = o[0]

        return t



    def user_alt(self, vo):
        sql = "update members set id = %s, email = %s, p_num = %s WHERE no = %s"

        self.cus.execute(sql,(vo.user_id, vo.user_email, vo.user_p_num, vo.user_no))

        self.cus.execute("commit")

        print('수정완료!')
