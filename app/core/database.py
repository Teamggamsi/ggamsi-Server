import pymysql

async def Connect():
    connection = pymysql.connect(host="localhost", user="root", passwd="", db="ggamsi", charset="utf8")
    cursor = connection.cursor()
    return connection, cursor