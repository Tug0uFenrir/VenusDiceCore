import psycopg2

def connect_db():
    with open('plugin/database_config.ini','r') as f:
        a=f.readlines()[-1].replace('DATABASE=[','').replace(']','').split(',')
        conn=psycopg2.connect(
            dbname=a[0],
            user=a[1],
            password=a[2],
            host=a[3],
            port=a[4],
        )
        f.close()
        return conn


def insert_player(conn, qq_id, player_name, charter_name):
    cursor = conn.cursor()
    # 检查玩家是否存在
    cursor.execute('SELECT qq_id FROM players WHERE qq_id = %s', (str(qq_id),))
    if cursor.fetchone() is None:
        # 玩家不存在，先创建玩家
        cursor.execute('''
            INSERT INTO players (qq_id, name)
            VALUES (%s, %s) ON CONFLICT (qq_id) DO NOTHING
        ''', (qq_id, player_name))
        conn.commit()

    # 查询现有角色 ID
    cursor.execute('SELECT MAX(player_character_id) FROM player_character WHERE player_qq_id = %s', (qq_id,))
    max_id = cursor.fetchone()[0]
    if max_id is None:
        max_id = 0
    player_character_id = max_id + 1

    # 插入角色信息，如果主键存在则跳过插入
    cursor.execute('''
        INSERT INTO player_character (player_qq_id, player_character_id, player_character_name)
        VALUES (%s, %s, %s) ON CONFLICT (player_qq_id, player_character_id) DO NOTHING
    ''', (qq_id, player_character_id, charter_name))
    conn.commit()


def select_player(conn, qq_id, player_name):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT player_character_id, player_character_name 
        FROM player_character
        WHERE player_qq_id = %s
    ''', (str(qq_id),))

    results = cursor.fetchall()
    return results

def select_group_players(conn, group_id, qq_id):
    cursor = conn.cursor()
    if group_id:  # 如果提供了群号
        cursor.execute('''
            SELECT player_character_id, player_character_name, bind_qq_group, bind_type
            FROM player_character
            WHERE bind_qq_group = %s OR bind_qq_group IS NULL OR bind_qq_group != %s
        ''', (str(group_id), str(group_id)))
    else:
        cursor.execute('''
            SELECT player_character_id, player_character_name, bind_qq_group, bind_type
            FROM player_character
            WHERE player_qq_id = %s
        ''', (str(qq_id),))
    results = cursor.fetchall()
    return results

def update_bind_status(conn, qq_id, group_id, character_id, bind_type):
    cursor = conn.cursor()

    # 确保bind_type是字符串类型
    unbind_type = '-'

    # 更新其他同一用户在群组内的所有绑定为未绑定
    cursor.execute('''
        UPDATE player_character
        SET bind_type = %s
        WHERE player_qq_id = %s AND bind_qq_group = %s
    ''', (unbind_type, str(qq_id), str(group_id)))
    conn.commit()

    # 更新指定角色的绑定类型
    cursor.execute('''
        UPDATE player_character
        SET bind_qq_group = %s, bind_type = %s
        WHERE player_qq_id = %s AND player_character_id = %s
    ''', (str(group_id), bind_type, str(qq_id), character_id))
    conn.commit()


def delete_player_character(conn, qq_id, character_name):
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM player_character
        WHERE player_qq_id = %s AND player_character_id = %s 
    ''', (str(qq_id), str(character_name)))
    conn.commit()

def update_character_name(conn, qq_id, character_id, new_name):
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE player_character
        SET player_character_name = %s
        WHERE player_qq_id = %s AND player_character_id = %s
    ''', (new_name, str(qq_id), str(character_id)))
    conn.commit()



def get_bound_character(conn, qq_id, group_id):
    cursor = conn.cursor()
    if group_id is None:
        cursor.execute('''
            SELECT player_character_id FROM player_character
            WHERE player_qq_id = %s AND bind_qq_group IS NULL AND bind_type = %s
        ''', (str(qq_id), '*'))
    else:
        cursor.execute('''
            SELECT player_character_id FROM player_character
            WHERE player_qq_id = %s AND bind_qq_group = %s AND bind_type = %s
        ''', (str(qq_id), str(group_id), '*'))

    result = cursor.fetchone()
    return result


def get_character_skills(conn, qq_id, character_id):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT player_character_skills FROM player_character
        WHERE player_qq_id = %s AND player_character_id = %s
    ''', (str(qq_id), character_id))

    result = cursor.fetchone()
    return result[0] if result else None

def update_character_skills(conn, qq_id, character_id, skills):
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE player_character
        SET player_character_skills = %s
        WHERE player_qq_id = %s AND player_character_id = %s
    ''', (skills, str(qq_id), character_id))
    conn.commit()


def get_recent_private_character(conn, qq_id):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT player_character_id FROM player_character
        WHERE player_qq_id = %s AND bind_qq_group IS NULL
        ORDER BY player_character_id DESC LIMIT 1
    ''', (str(qq_id),))

    result = cursor.fetchone()
    return result[0] if result else None


def get_player_details(conn, player_character_id):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT player_character_id, player_character_name, player_character_skills, bind_qq_group, bind_type 
        FROM player_character
        WHERE player_character_id = %s
    ''', (player_character_id,))
    return cursor.fetchone()


def get_character_properties(conn, qq_id, character_id):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT player_character_skills 
        FROM player_character
        WHERE player_qq_id = %s AND player_character_id = %s
    ''', (str(qq_id), character_id))

    result = cursor.fetchone()
    return eval(result[0]) if result and result[0] else {}


