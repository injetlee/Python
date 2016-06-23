from openpyxl import load_workbook
import pymysql
config = {
	'host': '127.0.0.1',
	'port':3306,
	'user': 'root',
	'password': 'root',
	'charset': 'utf8mb4',
	#'cursorclass': pymysql.cursors.DictCursor

}
conn = pymysql.connect(**config)
conn.autocommit(1)
cursor = conn.cursor()
name = 'lyexcel'
cursor.execute('create database if not exists %s' %name)
conn.select_db(name)
table_name = 'info'
cursor.execute('create table if not exists %s(id MEDIUMINT NOT NULL AUTO_INCREMENT,name varchar(30),tel varchar(30),primary key (id))'%table_name)

wb2 = load_workbook('hpu.xlsx')
ws=wb2.get_sheet_names()
for row in wb2:
	print("1")
	for cell in row:
		value1=(cell[0].value,cell[4].value)
		cursor.execute('insert into info (name,tel) values(%s,%s)',value1)

print("overing...")
# for row in A:
# 	print(row)
#print (wb2.get_sheet_names())
