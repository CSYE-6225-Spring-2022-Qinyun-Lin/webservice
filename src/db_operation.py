import mysql.connector as mc


def connect_mysql():
    config = {
        'user': 'root',
        'password': 'adminadmin!',
        'host': '127.0.0.1',
        'port': '3306',
        'database': 'csye6225'
    }
    con = mc.connect(**config)
    return con


def execute_and_get_result(sql):
    con = connect_mysql()
    cursor = con.cursor(buffered=True)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        con.close()
        return result
    except Exception:
        return None


def execute(sql):
    con = connect_mysql()
    cursor = con.cursor(buffered=True)
    try:
        cursor.execute(sql)
        con.commit()
        con.close()
        return True
    except Exception:
        return False
