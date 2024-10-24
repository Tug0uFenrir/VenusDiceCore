import psycopg2


'''
group_status
group_id（主键，索引，唯一键）varchar
status 本群使用的规则 varchar
bot_status 机器人本群是否开启 varchar

player_character
player_qq_id（主键，索引） 玩家的qq号 bigint
player_character_id (主键，索引)玩家角色的id big int
player_character_name 玩家角色的名字 varchar
player_character_skills 玩家的技能 varchar
bind_qq_group 该角色卡绑定的群聊号 bigint
bind_type 绑定的状态 varchar
player_character_rule_type 这张角色卡所属什么规则
'''

def connect_db():
    with open('database_config.ini','r') as f:
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


def update_character_sanity(conn, qq_id, character_id, new_sanity):
    cursor = conn.cursor()
    skills = get_character_skills(conn, qq_id, character_id)

    if skills:
        skills = eval(skills)
        skills['san'] = new_sanity
        cursor.execute('''
            UPDATE player_character
            SET player_character_skills = %s
            WHERE player_qq_id = %s AND player_character_id = %s
        ''', (str(skills), str(qq_id), character_id))
        conn.commit()


def insert_player(conn, qq_id, player_name, charter_name, rule_type):
    cursor = conn.cursor()
    cursor.execute('SELECT qq_id FROM players WHERE qq_id = %s', (str(qq_id),))
    if cursor.fetchone() is None:
        cursor.execute('''
            INSERT INTO players (qq_id, name)
            VALUES (%s, %s) ON CONFLICT (qq_id) DO NOTHING
        ''', (qq_id, player_name))
        conn.commit()
    cursor.execute('SELECT MAX(player_character_id) FROM player_character WHERE player_qq_id = %s', (qq_id,))
    max_id = cursor.fetchone()[0]
    if max_id is None:
        max_id = 0
    player_character_id = max_id + 1
    cursor.execute('''
        INSERT INTO player_character (player_qq_id, player_character_id, player_character_name, player_character_rule_type)
        VALUES (%s, %s, %s, %s) ON CONFLICT (player_qq_id, player_character_id) DO NOTHING
    ''', (qq_id, player_character_id, charter_name, rule_type))
    conn.commit()


def select_player(conn, qq_id,):
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

def update_bind_status(conn, qq_id, group_id, character_id, bind_type, rule_type):
    cursor = conn.cursor()
    unbind_type = '-'
    cursor.execute('''
        UPDATE player_character
        SET bind_type = %s
        WHERE player_qq_id = %s AND bind_qq_group = %s
    ''', (unbind_type, str(qq_id), str(group_id)))
    conn.commit()

    cursor.execute('''
        UPDATE player_character
        SET bind_qq_group = %s, bind_type = %s, player_character_rule_type = %s
        WHERE player_qq_id = %s AND player_character_id = %s
    ''', (str(group_id), bind_type, rule_type, str(qq_id), character_id))
    conn.commit()


def delete_player_character(conn, qq_id, character_name):
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM player_character
        WHERE player_qq_id = %s AND player_character_id = %s 
    ''', (str(qq_id), str(character_name)))
    conn.commit()

def update_character_name(conn, qq_id, character_id, new_name, rule_type):
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE player_character
        SET player_character_name = %s, player_character_rule_type = %s
        WHERE player_qq_id = %s AND player_character_id = %s
    ''', (new_name, rule_type, str(qq_id), str(character_id)))
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


def get_player_details(conn, character_id):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT player_character_id, player_character_name, player_character_skills, bind_qq_group, bind_type, player_character_rule_type
        FROM player_character
        WHERE player_character_id = %s
    ''', (character_id,))
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



def update_group_rule(conn, group_id, rule):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO group_status (group_id, status)
        VALUES (%s, %s)
        ON CONFLICT (group_id) DO UPDATE SET status = EXCLUDED.status
    ''', (group_id, rule))
    conn.commit()

def get_group_bot_status(conn, group_id):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT bot_status FROM group_status
        WHERE group_id = %s
    ''', (str(group_id),))
    result = cursor.fetchone()
    return result[0] if result else "off"

def get_group_bot_rule(conn,group_id):
    cursor = conn.cursor()
    cursor.execute('''
    SELECT status FROM group_status
    WHERE group_id = %s''', (str(group_id),))
    result = cursor.fetchone()
    return result[0] if result else "coc"

def update_group_bot_status(conn, group_id, status):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO group_status (group_id, bot_status)
        VALUES (%s, %s)
        ON CONFLICT (group_id) DO UPDATE SET bot_status = EXCLUDED.bot_status
    ''', (group_id, status))
    conn.commit()



def get_group_rule(conn, group_id):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT status FROM group_status
        WHERE group_id = %s
    ''', (str(group_id),))
    result = cursor.fetchone()
    return result[0] if result else "coc"


def get_character_rule(conn, qq_id, character_id):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT player_character_rule_type FROM player_character
        WHERE player_qq_id = %s AND player_character_id = %s
    ''', (str(qq_id), character_id))
    result = cursor.fetchone()
    return result[0] if result else None

