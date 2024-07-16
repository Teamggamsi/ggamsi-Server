import pymysql

async def Connect():
    connection = pymysql.connect(host="43.201.116.75", user="root", passwd="", db="ggamsi", charset="utf8")
    cursor = connection.cursor()
    return connection, cursor