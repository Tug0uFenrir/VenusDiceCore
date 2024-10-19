skills_roll = on_command('ra', aliases={'rc'})
@skills_roll.handle()
async def handle_func(event: MessageEvent, args: Message = CommandArg()):
    # Regular expression patterns
    pattern = r"^\s*([\u4e00-\u9fa5]+)\s*(\d+)$"
    p2 = r"^\s*(极难|困难|)?\s*([\u4e00-\u9fa5]+)\s*(\d+)$"

    if location := args.extract_plain_text():
        user_name = event.sender.nickname
        # Use regex to parse command
        match = re.match(pattern, location.strip())
        match2 = re.match(p2, location.strip())

        if match2:
            level = match2.group(1)
            skill_name = match2.group(2)
            skill_value = int(match2.group(3))
            dice_value = int(roll_dice('1d100')[1])  # Simulate rolling a dice

            if level == "困难":
                message=''
                if int(skill_value) // 2 >= int(dice_value):
                    message = f"筱酱发现{user_name}进行了{skill_name}, 结果是.........{dice_value}/{skill_value//2}【困难成功！】\n{chat(f'''{event.user_id}:s{skill_name}={skill_value},t={dice_value}''')}"

                else:
                    message = f"筱酱发现{user_name}进行了【{skill_name}】鉴定, 结果是.........{dice_value}/{skill_value//2}【失败！！】\n{chat(f'''{event.user_id}:s{skill_name}={skill_value},t={dice_value}''')}"
                await skills_roll.send(message)
            elif level == "极难":
                message=''
                if int(skill_value) // 4 >= int(dice_value):
                    message = f"筱酱发现{user_name}进行了{skill_name}, 结果是.........{dice_value//4}/{skill_value}【极难成功！】\n{chat(f'''{event.user_id}:s{skill_name}={skill_value},t={dice_value}''')}"
                else:
                    message = f"筱酱发现{user_name}进行了【{skill_name}】鉴定, 结果是.........{dice_value//4}/{skill_value}【失败！！】\n{chat(f'''{event.user_id}:s{skill_name}={skill_value},t={dice_value}''')}"
                await skills_roll.send(message)

        if match:
            skill_name = match.group(1)
            skill_value = match.group(2)
            dice_value = roll_dice('1d100')[1]

            if int(skill_value) >= int(dice_value):
                success = f"筱酱发现{user_name}进行了{skill_name}, 结果是.........{dice_value}/{skill_value}【成功！】\n{chat(f'''{event.user_id}:s{skill_name}={skill_value},t={dice_value}''')}"
                if int(skill_value) // 2 >= int(dice_value):
                    success = f"筱酱发现{user_name}进行了{skill_name}, 结果是.........{dice_value}/{skill_value}【困难成功！】\n{chat(f'''{event.user_id}:s{skill_name}={skill_value},t={dice_value}''')}"
                if int(skill_value) // 4 >= int(dice_value):
                    success = f"筱酱发现{user_name}进行了{skill_name}, 结果是.........{dice_value}/{skill_value}【极难成功！】\n{chat(f'''{event.user_id}:s{skill_name}={skill_value},t={dice_value}''')}"
                if int(dice_value) == 1:
                    success = f"筱酱发现{user_name}进行了{skill_name}, 结果是.........{dice_value}/{skill_value}【大成功！！！！！】\n{chat(f'''{event.user_id}:s{skill_name}={skill_value},t={dice_value}''')}"
                await skills_roll.send(success)
            else:
                fail = f"筱酱发现{user_name}进行了【{skill_name}】鉴定, 结果是.........{dice_value}/{skill_value}【失败！！】\n{chat(f'''{event.user_id}:s{skill_name}={skill_value},t={dice_value}''')}"
                await skills_roll.send(fail)







@st.handle()

async def handle_func(event: MessageEvent, args: Message = CommandArg()):
    if location := args.extract_plain_text():
        user_name = event.sender.nickname
        user_id = event.sender.user_id
        conn = connect_db()

        if isinstance(event, GroupMessageEvent):
            group_id = event.group_id

            # 检查玩家是否有绑定的角色卡
            bound_char = get_bound_character(conn, user_id, group_id)

            if not bound_char:
                await st.send(f"{user_name}阁下，您尚未新建角色卡，无法使用 st 功能哦～")
                return
            character_id = bound_char[0]

        elif isinstance(event, PrivateMessageEvent):
            group_id = None

            # 获取最近创建的私聊角色卡
            character_id = get_recent_private_character(conn, user_id)

            if not character_id:
                await st.send(f"{user_name}阁下，您尚未新建角色卡，无法使用 st 功能哦～")
                return

        else:
            await st.send(f"{user_name}阁下，暂时只支持群聊和私聊中的 st 功能哦～")
            return

        # 从数据库中获取现有技能数据
        existing_skills_str = get_character_skills(conn, user_id, character_id)
        existing_skills = eval(existing_skills_str) if existing_skills_str else {}

        # 从输入文本解析技能数据
        skills_regex = re.findall(r'([一-龥a-zA-Z]+)(\d+)', location)
        new_skills = {skill[0]: int(skill[1]) for skill in skills_regex}

        # 将新的技能数据加到现有技能数据上
        for skill, value in new_skills.items():
            if skill in existing_skills:
                existing_skills[skill] += value
            else:
                existing_skills[skill] = value

        # 将合并后的技能数据更新到数据库
        update_character_skills(conn, user_id, character_id, str(existing_skills))

        await st.send(f"{user_name}阁下，技能已经导入并更新成功咯～")






pc=on_command("pc")
@pc.handle()

async def handle_func(event: MessageEvent, args: Message = CommandArg()):
    if location := args.extract_plain_text():
        user_name = event.sender.nickname
        user_id = event.sender.user_id
        conn = connect_db()
        char_list = location.split(' ')

        if char_list[0] in ['new', 'tag', 'show', 'nn', 'del', 'list', 'stat']:
            if char_list[0] == 'new':
                character_name = char_list[1]
                insert_player(conn, user_id, user_name, character_name)
                await pc.send(f"{user_name}的数据已经保存咯！")

            elif char_list[0] == 'list':
                group_id = None
                if isinstance(event, GroupMessageEvent):
                    group_id = event.group_id
                characters = select_group_players(conn, group_id, user_id)
                structure = f"{user_name}的角色列表：\n"
                for item in characters:
                    bind_status = "-"
                    if item[3] == "*":
                        if item[2] == str(group_id):
                            bind_status = "*"
                        elif item[2] is None:
                            bind_status = "P"
                        else:
                            bind_status = "O"
                    structure += f"[{item[0]}]<COC7>{item[1]}    {bind_status}\n"
                await pc.send(structure)

            elif char_list[0] == 'show':
                if len(char_list) < 2:
                    # 返回当前绑定角色卡的详细信息
                    group_id = event.group_id if isinstance(event, GroupMessageEvent) else None
                    if not group_id:
                        await pc.send("无法确定当前群聊绑定哦～")
                        return
                    bound_char = get_bound_character(conn, user_id, group_id)

                    if not bound_char:
                        await pc.send(f"{user_name}阁下，您尚未绑定角色卡哦～")
                        return
                    character = get_player_details(conn, bound_char[0])
                else:
                    # 返回指定角色卡的详细信息
                    character_name = char_list[1]

                    character = get_player_details(conn, character_name)

                if character:
                    skills = eval(character[2]) if character[2] else '无'
                    details = f"角色ID: {character[0]}\n角色名: {character[1]}\n技能: {skills}\n绑定群: {character[3] if character[3] else '无'}\n绑定状态: {character[4]}"
                    await pc.send(details)
                else:
                    await pc.send(f"未找到角色 {char_list[1]} 的角色卡哦～")

            elif char_list[0] == 'tag':
                if len(char_list) < 2:
                    await pc.send("请提供要标记的角色卡名哦～")
                    return

                character_name = char_list[1]
                group_id = event.group_id if isinstance(event, GroupMessageEvent) else None

                if not group_id:
                    await pc.send("只能在群聊中使用 tag 功能哦～")
                    return

                existing_chars = select_group_players(conn, group_id, user_id)
                for char in existing_chars:
                    if char[1] == character_name:
                        # 找到了角色，进行绑定
                        update_bind_status(conn, user_id, group_id, char[0], '*')
                        await pc.send(f"角色卡 {character_name} 已标记为当前群绑定卡啦～")
                        return

                await pc.send(f"未找到名为 {character_name} 的角色卡哦～")

            elif char_list[0] == 'del':
                if len(char_list) < 2:
                    await pc.send("请提供要删除的角色卡名哦～")
                    return

                character_name = char_list[1]
                delete_player_character(conn, user_id, character_name)
                await pc.send(f"角色卡 {character_name} 已删除哦～")
            elif char_list[0] == 'nn':
                if len(char_list) < 2:
                    await pc.send("请提供新的角色卡名哦～")
                    return
                new_name = char_list[1]
                group_id = event.group_id if isinstance(event, GroupMessageEvent) else None
                if not group_id:
                    await pc.send("无法确定当前群聊绑定哦～")
                    return
                bound_char = get_bound_character(conn, user_id, group_id)
                if not bound_char:
                    await pc.send(f"{user_name}阁下，您尚未绑定角色卡哦～")
                    return
                character_id = bound_char[0]
                update_character_name(conn, user_id, character_id, new_name)
                await pc.send(f"{user_name}阁下，角色卡名字已成功修改为 {new_name} 啦～")














































@pc.handle()
async def handle_func(event: MessageEvent, args: Message = CommandArg()):
    user_name = event.sender.nickname
    user_id = event.sender.user_id
    conn = connect_db()

    args_text = args.extract_plain_text().split()
    if not args_text:
        await pc.send(f"{user_name}阁下，请提供参数哦～")
        return

    cmd = args_text[0]
    rest_args = ' '.join(args_text[1:])

    if cmd == 'tag':
        character_name = rest_args.strip()
        group_id = event.group_id if isinstance(event, GroupMessageEvent) else None

        if not group_id:
            await pc.send("只能在群聊中使用 tag 功能哦～")
            return

        existing_chars = select_group_players(conn, group_id, user_id)
        for char in existing_chars:
            if char[1] == character_name:
                # 找到了角色，进行绑定
                update_bind_status(conn, user_id, group_id, char[0], '*')
                await pc.send(f"角色卡 {character_name} 已标记为当前群绑定卡啦～")
                return

        await pc.send(f"未找到名为 {character_name} 的角色卡哦～")

    elif cmd == 'show':
        if len(args_text) < 2:
            group_id = event.group_id if isinstance(event, GroupMessageEvent) else None
            if not group_id:
                await pc.send("无法确定当前群聊绑定哦～")
                return
            bound_char = get_bound_character(conn, user_id, group_id)
            if not bound_char:
                await pc.send(f"{user_name}阁下，您尚未绑定角色卡哦～")
                return
            character = get_player_details(conn, bound_char[0])
        else:
            character_name = args_text[1]
            character = get_player_details(conn, character_name)

        if character:
            skills = eval(character[2]) if character[2] else '无'
            details = f"角色ID: {character[0]}\n角色名: {character[1]}\n技能: {skills}\n绑定群: {character[3] if character[3] else '无'}\n绑定状态: {character[4]}"
            await pc.send(details)
        else:
            await pc.send(f"未找到角色 {args_text[1]} 的角色卡哦～")

    elif cmd == 'list':
        group_id = None
        if isinstance(event, GroupMessageEvent):
            group_id = event.group_id
        characters = select_group_players(conn, group_id, user_id)
        structure = f"{user_name}的角色列表：\n"
        for item in characters:
            bind_status = "-"
            if item[3] == "*":
                if item[2] == str(group_id):
                    bind_status = "*"
                elif item[2] is None:
                    bind_status = "P"
                else:
                    bind_status = "O"
            structure += f"[{item[0]}]<COC7>{item[1]}    {bind_status}\n"
        await pc.send(structure)

    elif cmd == 'del':
        character_name = rest_args.strip()
        delete_player_character(conn, user_id, character_name)
        await pc.send(f"角色卡 {character_name} 已删除哦～")

    elif cmd == 'nn':
        new_name = rest_args.strip()
        group_id = event.group_id if isinstance(event, GroupMessageEvent) else None
        if not group_id:
            await pc.send("无法确定当前群聊绑定哦～")
            return
        bound_char = get_bound_character(conn, user_id, group_id)
        if not bound_char:
            await pc.send(f"{user_name}阁下，您尚未绑定角色卡哦～")
            return
        character_id = bound_char[0]
        update_character_name(conn, user_id, character_id, new_name)
        await pc.send(f"{user_name}阁下，角色卡名字已成功修改为 {new_name} 啦～")

    elif cmd == 'stat':
        await pc.send(f"{user_name}阁下，当前指令还未实现～")

    else:
        await pc.send(f"{user_name}阁下，不支持的指令哦～")











@st.handle()
async def handle_st(event: MessageEvent, args: Message = CommandArg()):
    user_name = event.sender.nickname
    user_id = event.sender.user_id
    SYNONYMS=coc_skills_SYMONYS()
    conn = connect_db()

    if isinstance(event, GroupMessageEvent):
        group_id = event.group_id
        bound_char = get_bound_character(conn, user_id, group_id)

        if not bound_char:
            await st.send(f"{user_name}阁下，您尚未新建角色卡，无法使用 st 功能哦～")
            return
        character_id = bound_char[0]

    elif isinstance(event, PrivateMessageEvent):
        group_id = None
        character_id = get_recent_private_character(conn, user_id)

        if not character_id:
            await st.send(f"{user_name}阁下，您尚未新建角色卡，无法使用 st 功能哦～")
            return

    else:
        await st.send(f"{user_name}阁下，暂时只支持群聊和私聊中的 st 功能哦～")
        return

    args_text = args.extract_plain_text().split()
    if not args_text:
        await st.send(f"{user_name}阁下，参数不能为空哦～")
        return

    cmd = args_text[0]  # 获取命令
    rest_args = ' '.join(args_text[1:])  # 其余参数

    properties = get_character_properties(conn, user_id, character_id) or {}

    if cmd in ('del', 'clr', 'show'):
        if cmd == 'del':
            prop_name = rest_args.strip()  # 属性名
            if prop_name in properties:
                del properties[prop_name]
                await st.send(f"{user_name}阁下，已删除属性{prop_name}～")
            else:
                await st.send(f"{user_name}阁下，没有找到属性{prop_name}哦～")
        elif cmd == 'clr':
            properties = {}
            await st.send(f"{user_name}阁下，所有属性已清空～")
        elif cmd == 'show':
            prop_name = rest_args.strip() if rest_args.strip() else None  # 属性名
            if not prop_name:
                filtered_props = {}
                for key, value in properties.items():
                    if value > 1:
                        key = SYNONYMS.get(key, key)  # 使用同义词
                        if key not in filtered_props or value > filtered_props[key]:  # 保留最高值
                            filtered_props[key] = value

                props = '\n'.join([f'{k}：{v}' for k, v in filtered_props.items()])
                await st.send(f"{user_name}阁下的所有属性如下：\n{props}")
            else:
                if prop_name in SYNONYMS:
                    prop_name = SYNONYMS[prop_name]
                if prop_name in properties:
                    await st.send(f"{user_name}阁下，属性{prop_name}的值是：{properties[prop_name]}")
                else:
                    await st.send(f"{user_name}阁下，没有找到属性{prop_name}哦～")
    else:
        if ':' in rest_args:
            parts = rest_args.split(':')
            prop_name = parts[0].strip()
            value_expr = parts[1].strip()

            match = re.match(r'([+-]?\d+d\d+)|([+-]?\d+)', value_expr)
            if match:
                if 'd' in value_expr:
                    dice_result = roll_dice(value_expr)[1]
                    new_value = properties.get(prop_name, 0) + dice_result if value_expr.startswith(
                        '+') else properties.get(prop_name, 0) - dice_result
                else:
                    new_value = properties.get(prop_name, 0) + int(value_expr) if value_expr.startswith(
                        '+') else properties.get(prop_name, 0) - int(value_expr)
                properties[prop_name] = new_value
            else:
                properties[prop_name] = int(value_expr.replace('+', ''))

            await st.send(f"{user_name}阁下，属性{prop_name}更新成功～")
        else:
            await st.send(f"{user_name}阁下，参数格式有误哦～")

    # 更新属性
    update_character_properties(conn, user_id, character_id, str(properties))


















st = on_command("st")
@st.handle()
async def handle_st(event: MessageEvent, args: Message = CommandArg()):
    user_name = event.sender.nickname
    user_id = event.sender.user_id
    SYNONYMS = coc_skills_SYMONYS()
    conn = connect_db()

    if isinstance(event, GroupMessageEvent):
        group_id = event.group_id
        bound_char = get_bound_character(conn, user_id, group_id)

        if not bound_char:
            await st.send(f"{user_name}阁下，您尚未新建角色卡，无法使用 st 功能哦～")
            return
        character_id = bound_char[0]

    elif isinstance(event, PrivateMessageEvent):
        group_id = None
        character_id = get_recent_private_character(conn, user_id)

        if not character_id:
            await st.send(f"{user_name}阁下，您尚未新建角色卡，无法使用 st 功能哦～")
            return

    else:
        await st.send(f"{user_name}阁下，暂时只支持群聊和私聊中的 st 功能哦～")
        return

    # 从数据库中获取现有技能数据
    existing_skills_str = get_character_skills(conn, user_id, character_id)
    existing_skills = eval(existing_skills_str) if existing_skills_str else {}

    # 从输入文本解析技能数据
    location = args.extract_plain_text()
    skills_regex = re.findall(r'([一-龥a-zA-Z]+)(\d+)', location)
    new_skills = {skill[0]: int(skill[1]) for skill in skills_regex}

    # 将新的技能数据加到现有技能数据上
    for skill, value in new_skills.items():
        if skill in existing_skills:
            existing_skills[skill] += value
        else:
            existing_skills[skill] = value

    args_text = args.extract_plain_text().split()
    if not args_text:
        await st.send(f"{user_name}阁下，参数不能为空哦～")
        return

    cmd = args_text[0]
    rest_args = ' '.join(args_text[1:])

    properties = get_character_properties(conn, user_id, character_id) or {}

    if cmd in ('del', 'clr', 'show'):
        if cmd == 'del':
            prop_name = rest_args.strip()
            if prop_name in properties:
                del properties[prop_name]
                await st.send(f"{user_name}阁下，已删除属性{prop_name}～")
            else:
                await st.send(f"{user_name}阁下，没有找到属性{prop_name}哦～")
        elif cmd == 'clr':
            properties = {}
            await st.send(f"{user_name}阁下，所有属性已清空～")
        elif cmd == 'show':
            prop_name = rest_args.strip() if rest_args.strip() else None
            if not prop_name:
                filtered_props = {}
                for key, value in properties.items():
                    if value >= 20:
                        comp_key = SYNONYMS.get(key, key)
                        if comp_key not in filtered_props or value > filtered_props[comp_key]:
                            filtered_props[comp_key] = value

                props = '\n'.join([f'{k}：{v}' for k, v in filtered_props.items()])
                await st.send(f"{user_name}阁下的所有属性如下：\n{props}")
            else:
                if prop_name in SYNONYMS:
                    prop_name = SYNONYMS[prop_name]
                if prop_name in properties and properties[prop_name] >= 20:
                    await st.send(f"{user_name}阁下，属性{prop_name}的值是：{properties[prop_name]}")
                else:
                    await st.send(f"{user_name}阁下，没有找到属性{prop_name}或者该属性值过低哦～")
    else:
        properties = get_character_properties(conn, user_id, character_id) or {}

        # 检查是否有运算符号
        await st.send(rest_args)
        print(rest_args)
        if '' in rest_args:
            parts = rest_args.split(':')
            prop_name = parts[0].strip()
            value_expr = parts[1].strip()

            if prop_name in SYNONYMS:
                prop_name = SYNONYMS[prop_name]

            current_value = properties.get(prop_name, 0)

            match = re.match(r'^([+-]?\d+|[+-]?\d+d\d+|[*/]\d+)$', value_expr)

            if match:
                new_value = 0
                if 'd' in value_expr:
                    dice_roll, dice_result = roll_dice(value_expr)
                    if dice_result is not None:
                        if value_expr.startswith('+') or not value_expr.startswith('-'):
                            new_value = current_value + dice_result
                        else:
                            new_value = current_value - dice_result
                if value_expr.startswith('+'):
                    new_value = current_value + int(value_expr[1:])
                if value_expr.startswith('-'):
                    new_value = current_value - int(value_expr[1:])
                if value_expr.startswith('*'):
                    new_value = current_value * int(value_expr[1:])
                if value_expr.startswith('/'):
                    new_value = current_value // int(value_expr[1:])  # 整除
                else:
                    new_value = current_value + int(value_expr)

                # 确保新值不会溢出
                #new_value = max(min(new_value, 2 ** 31 - 1), -(2 ** 31))

                properties[prop_name] = new_value
                await st.send(f"{user_name}阁下，属性{prop_name}更新成功～ 当前值为：{properties[prop_name]}")
            # 更新属性
            update_character_properties(conn, user_id, character_id, str(properties))
        else:
            # 更新数据库中的角色技能数据
            update_character_skills(conn, user_id, character_id, str(existing_skills))
            await st.send(f"{user_name}阁下，技能导入完成啦～")




st = on_command("st")
@st.handle()
async def handle_st(event: MessageEvent, args: Message = CommandArg()):
    user_name = event.sender.nickname
    user_id = event.sender.user_id
    SYNONYMS = coc_skills_SYMONYS()
    conn = connect_db()

    if isinstance(event, GroupMessageEvent):
        group_id = event.group_id
        bound_char = get_bound_character(conn, user_id, group_id)

        if not bound_char:
            await st.send(f"{user_name}阁下，您尚未新建角色卡，无法使用 st 功能哦～")
            return
        character_id = bound_char[0]

    elif isinstance(event, PrivateMessageEvent):
        group_id = None
        character_id = get_recent_private_character(conn, user_id)

        if not character_id:
            await st.send(f"{user_name}阁下，您尚未新建角色卡，无法使用 st 功能哦～")
            return

    else:
        await st.send(f"{user_name}阁下，暂时只支持群聊和私聊中的 st 功能哦～")
        return

    # 从数据库中获取现有技能数据
    existing_skills_str = get_character_skills(conn, user_id, character_id)
    existing_skills = eval(existing_skills_str) if existing_skills_str else {}

    # 从输入文本解析技能数据
    location = args.extract_plain_text()
    skills_regex = re.findall(r'([\u4e00-\u9fa5a-zA-Z]+)(-?\d+)', location)
    new_skills = {skill[0]: int(skill[1]) for skill in skills_regex}

    # 将新的技能数据加到现有技能数据上
    for skill, value in new_skills.items():
        if skill in existing_skills:
            existing_skills[skill] += value
        else:
            existing_skills[skill] = value

    args_text = args.extract_plain_text().split()
    if not args_text:
        await st.send(f"{user_name}阁下，参数不能为空哦～")
        return

    cmd = args_text[0]
    rest_args = ' '.join(args_text[1:])

    properties = get_character_properties(conn, user_id, character_id) or {}

    if cmd in ('del', 'clr', 'show'):
        if cmd == 'del':
            prop_name = rest_args.strip()
            if prop_name in properties:
                del properties[prop_name]
                await st.send(f"{user_name}阁下，已删除属性{prop_name}～")
            else:
                await st.send(f"{user_name}阁下，没有找到属性{prop_name}哦～")
        elif cmd == 'clr':
            properties = {}
            await st.send(f"{user_name}阁下，所有属性已清空～")
        elif cmd == 'show':
            prop_name = rest_args.strip() if rest_args.strip() else None
            if not prop_name:
                filtered_props = {}
                for key, value in properties.items():
                    if value >= 20:
                        comp_key = SYNONYMS.get(key, key)
                        if comp_key not in filtered_props or value > filtered_props[comp_key]:
                            filtered_props[comp_key] = value

                props = '\n'.join([f'{k}：{v}' for k, v in filtered_props.items()])
                await st.send(f"{user_name}阁下的所有属性如下：\n{props}")
            else:
                if prop_name in SYNONYMS:
                    prop_name = SYNONYMS[prop_name]
                if prop_name in properties and properties[prop_name] >= 20:
                    await st.send(f"{user_name}阁下，属性{prop_name}的值是：{properties[prop_name]}")
                else:
                    await st.send(f"{user_name}阁下，没有找到属性{prop_name}或者该属性值过低哦～")
    else:
        properties = get_character_properties(conn, user_id, character_id) or {}
        values=get_character_skills(conn, user_id, character_id) or {}
        #await st.send(values)

        # 检查是否有运算符号
        cmd = args_text[0]
        await st.send(cmd)
        if cmd:
            match = re.match(r'([^\d+-/*]+)([+-/*])(\d+)', rest_args)
            if not match:
                await st.send(f"{user_name}阁下，参数格式错误，请使用 '属性名+10' 的格式～")
                return

            prop_name = match.group(1).strip()  # 去除空格
            operator = match.group(2)
            value = int(match.group(3))

            if prop_name in SYNONYMS:
                prop_name = SYNONYMS[prop_name]
                current_value = properties.get(prop_name, 0)

                match = re.match(r'^([+-]?\d+|[+-]?\d+d\d+|[*\/]\d+)$', value_expr)
                if match:
                    new_value = current_value
                    if 'd' in value_expr:
                        dice_roll, dice_result = roll_dice(value_expr)
                        if dice_result is not None:
                            if value_expr.startswith('+') or not value_expr.startswith('-'):
                                new_value = current_value + dice_result
                            else:
                                new_value = current_value - dice_result
                    elif value_expr.startswith('+'):
                        new_value = current_value + int(value_expr[1:])
                    elif value_expr.startswith('-'):
                        new_value = current_value - int(value_expr[1:])
                    elif value_expr.startswith('*'):
                        new_value = current_value * int(value_expr[1:])
                    elif value_expr.startswith('/'):
                        new_value = current_value // int(value_expr[1:])
                    else:
                        new_value = current_value + int(value_expr)

                    # 确保新值不会溢出
                    new_value = max(min(new_value, 2 ** 31 - 1), -(2 ** 31))

                    properties[prop_name] = new_value
                    await st.send(f"{user_name}阁下，属性{prop_name}更新成功～ 当前值为：{properties[prop_name]}")

                # 更新属性
                update_character_properties(conn, user_id, character_id, str(properties))
            else:
                await st.send(f"{user_name}阁下，参数格式错误，请使用 '属性名:值' 的格式～")
        else:
            await st.send(f"{user_name}阁下，请提供要修改的属性和值，例如 '力量:10'～")

    # 更新数据库中的角色技能数据
    update_character_skills(conn, user_id, character_id, str(existing_skills))
    await st.send(f"{user_name}阁下，技能导入完成啦～")
