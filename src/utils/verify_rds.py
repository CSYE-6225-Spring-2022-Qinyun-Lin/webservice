import mysql.connector as mc

host = open("/home/ec2-user/webConfig/mysql_host.txt").readline().strip()
user, password = open("/home/ec2-user/webConfig/mysql_key.txt").readline().strip().split(", ")


def get_all():
    sql = "select * from health"
    config = {
        'user': user,
        'password': password,
        'host': host,
        'port': '3306',
        'database': 'csye6225'
    }
    con = mc.connect(**config)

    cursor = con.cursor(buffered=True)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        for each in result:
            print(each)
        con.close()

    except Exception:
        return None


if __name__ == '__main__':
    get_all()
