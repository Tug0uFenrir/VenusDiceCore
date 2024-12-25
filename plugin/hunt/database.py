import psycopg2

def connect_db():
    a=[]
    # 打开配置文件并读取内容
    with open('database_hunt_config.ini', 'r') as f:
            data_string = f.read().strip()

        # 找到'DATABASE='后面的部分并解析成列表
            if "DATABASE=" in data_string:
                    data_list_str = data_string.split('=')[1].strip('[]')
                    data_list = data_list_str.split(',')
                    a=data_list
                    print(a)
    f.close()

    conn=psycopg2.connect(
                dbname=a[0],
                user=a[1],
                password=a[2],
                host=a[3],
                port=a[4],
            )
    print("连接成功")
    return conn


def select_all_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM status")
    rows = cursor.fetchall()
    return rows

def update_status(conn,group_id:str,status:bool):
    cursor = conn.cursor()
    cursor.execute("UPDATE status SET bot_staus=%s WHERE group_id=%s", (status,group_id))
    conn.commit()
    return cursor



