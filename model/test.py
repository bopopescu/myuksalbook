import pymysql

con = pymysql.connect(host='localhost', user='myuksal', password='myuksal',
                               db='account', charset='utf8')
cus = con.cursor()
sql = "select * from board ORDER BY board_num DESC LIMIT " + 0 + ",1"
cus.execute(sql)

result = cus.fetchall()

print (result)

con.close()
