import pymysql

async def Connect():
    connection = pymysql.connect(host="172.26.15.219", user="root", passwd="", db="ggamsi", charset="utf8")
    cursor = connection.cursor()
    return connection, cursor