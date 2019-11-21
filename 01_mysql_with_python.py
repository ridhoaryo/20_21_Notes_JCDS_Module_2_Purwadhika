import mysql.connector

db = mysql.connector.connect(
    host = 'localhost',
    port = 3306,
    user = 'ridhoaryo',
    passwd = 'do708091Mysql',
    database = 'ptabc'
)
c = db.cursor()
# c.execute('select * from karyawan')
# x = c.fetchall()
# for i in x:
# #     print(i)

# sql = 'insert into karyawan (nama, gaji) values (%s, %s)'
# val = ('Andi', 15000000)
# c.execute(sql, val)
# db.commit()
# print(c.rowcount, 'Data Tersimpan')

sql = 'insert into karyawan (nama, gaji) values (%s, %s)'
val = [('Budi', 15000000), ('Caca', 15000000)]
c.executemany(sql, val)
db.commit()
print(c.rowcount, 'Data Tersimpan')
