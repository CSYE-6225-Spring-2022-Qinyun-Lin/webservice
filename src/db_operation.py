import mysql.connector as mc


class DBExecutor:
    def __init__(self):
        # self.host = "127.0.0.1"
        # self.user = "root"
        # self.password = "adminadmin!"
        self.host = open("/home/ec2-user/webConfig/mysql_host.txt").readline().strip()
        self.user, self.password = open("/home/ec2-user/webConfig/mysql_key.txt").readline().strip().split(", ")

    def connect_mysql(self):
        config = {
            'user': self.user,
            'password': self.password,
            'host': self.host,
            'port': '3306',
            'database': 'csye6225'
        }
        con = mc.connect(**config)
        return con

    def setup_db(self):
        con = self.connect_mysql()
        cursor = con.cursor(buffered=True)
        try:
            sql = """create table health
                    (
                        id varchar(50) not null,
                        user_name varchar(50) not null,
                        password varchar(100) not null,
                        first_name varchar(30) not null,
                        last_name varchar(30) not null,
                        account_created datetime not null,
                        account_updated datetime not null,
                        image_id varchar(50) default null null,
                        image_filename varchar(50) default null null,
                        image_url varchar(200) default null null,
                        image_upload date default null null,
                        constraint heath_id_uindex
                            unique (id),
                        constraint heath_user_name_uindex
                            unique (user_name)
                    );"""
            cursor.execute(sql)
            con.commit()
            con.close()
            return True
        except Exception:
            return False

    def execute_and_get_result(self, sql):
        con = self.connect_mysql()
        cursor = con.cursor(buffered=True)
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            con.close()
            return result
        except Exception:
            return None

    def execute(self, sql):
        con = self.connect_mysql()
        cursor = con.cursor(buffered=True)
        try:
            cursor.execute(sql)
            con.commit()
            con.close()
            return True
        except Exception:
            return False


if __name__ == '__main__':
    db_executor = DBExecutor()
    if db_executor.setup_db():
        print("Set up MySQL successfully!")
    else:
        print("Set up MySQL failed!")
