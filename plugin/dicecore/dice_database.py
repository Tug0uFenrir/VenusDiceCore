import psycopg2
def connect_db():
    '''
    进行数据库连接
    :return: conn
    '''
    a=[]
    # 打开配置文件并读取内容
    with open('plugin/dicecore/database_config.ini', 'r') as f:
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

def get_group_bot_status(conn, group_id):
    '''
    获取机器人状态
    :param conn:数据库连接
    :param group_id: q群id
    :return: 字符串
    '''
    cursor = conn.cursor()
    cursor.execute('''
        SELECT bot_status FROM group_status
        WHERE group_id = %s
    ''', (str(group_id),))
    result = cursor.fetchone()
    print(result)
    return result[0] if result[0] else "off"


def update_group_rule(conn, group_id, rule):
    '''
    更新群聊规则书状态
    :param conn:
    :param group_id:
    :param rule:
    :return:
    '''
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO group_status (group_id, status)
        VALUES (%s, %s)
        ON CONFLICT (group_id) DO UPDATE SET status = EXCLUDED.status
    ''', (group_id, rule))
    conn.commit()

def update_group_bot_status(conn, group_id, status):
    '''
    更新群聊中机器人的状态
    :param conn:
    :param group_id:
    :param status:
    :return:
    '''
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO group_status (group_id, bot_status)
        VALUES (%s, %s)
        ON CONFLICT (group_id) DO UPDATE SET bot_status = EXCLUDED.bot_status
    ''', (group_id, status))
    conn.commit()

def get_group_bot_rule(conn,group_id):
    '''
    获取群组内机器人的规则书
    :param conn:
    :param group_id:
    :return:
    '''
    cursor = conn.cursor()
    cursor.execute('''
    SELECT status FROM group_status
    WHERE group_id = %s''', (str(group_id),))
    result = cursor.fetchone()
    return result[0] if result else "coc"

def get_bind_character(conn,user_id,group_id):
    '''
    获得在群里绑定的角色信息
    :param conn:
    :param user_id:
    :param group_id:
    :return:
    '''
    cursor = conn.cursor()
    cursor.execute(f'''
    SELECT * FROM player_character WHERE player_qq_id={user_id} AND bind_qq_group={group_id}''')
    result = cursor.fetchone()
    return result if result else None