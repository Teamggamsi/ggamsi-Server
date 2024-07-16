import pymysql

async def Connect():
    connection = pymysql.connect(host="43.201.116.75", port=3306, user="root", passwd="1234", db="ggamsi", charset="utf8")
    cursor = connection.cursor()
    return connection, cursor