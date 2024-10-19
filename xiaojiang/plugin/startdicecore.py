from nonebot import on_command
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, PrivateMessageEvent
from nonebot.params import CommandArg
import re


from .dicecore import roll_dice, generate_multiple_characters, bot_info, coc_skills_SYMONYS, generate_coc_character
from .gpt import *
from .database import *

bot_cmd = on_command("bot")
@bot_cmd.handle()
async def handle_func(event: MessageEvent, args: Message = CommandArg()):
    await bot_cmd.send(bot_info())


roll_cmd = on_command("r", aliases={'r'})
@roll_cmd.handle()
async def handle_func(event: MessageEvent, args: Message = CommandArg()):
    if location := args.extract_plain_text():
        try:
            if location[0] == 'd':
                user_name = event.sender.nickname
                dice_response = roll_dice(f'1d{location[1:]}')
                talk_message = f'''{event.user_id}-{user_name}:t={dice_response}'''
                gpt_talk = chat(talk_message)
                await roll_cmd.send(
                    f"{user_name}阁下，筱酱给出答案了哦～答案是.....：\n【{location}={dice_response[0]}】\n{gpt_talk}")
            else:
                dice_response = str(roll_dice(location)[1])
                user_name = event.sender.nickname
                talk_message = f'''{event.user_id}-{user_name}:t={dice_response}'''
                gpt_talk = chat(talk_message)
                await roll_cmd.send(
                    f"{user_name}阁下，筱酱给出答案了哦～答案是.....：\n【{location}={dice_response}】\n{gpt_talk}")
        except Exception as e:
            pass
    else:
        user_name = event.sender.nickname
        print(user_name)
        dice_response = str(roll_dice('1d100')[1])
        talk_message = f'''{event.user_id}:t={dice_response}'''
        gpt_talk = chat(talk_message)
        await roll_cmd.send(f"{user_name}阁下，筱酱给出答案了哦～答案是.....：\n【1d100={dice_response}】\n{gpt_talk}")


coc_cmd = on_command("coc")
@coc_cmd.handle()
async def handle_func(event: MessageEvent, args: Message = CommandArg()):
    user_id = event.user_id
    if location := args.extract_plain_text():
        if str(user_id) in ["815290790", "1803514767", "1904454183", "2019934270", "1945063708"]:
            total_count = int(location)
            results_character = []
            coc_response = ''
            for _ in range(total_count):
                while True:
                    character_data = generate_coc_character()
                    total_points = character_data['total_point']
                    print(total_points)
                    if 500 <= total_points < 700:
                        results_character.append(character_data)
                        break
            for idx, character in enumerate(results_character):
                coc_response += f"COC7th人物制成第{idx + 1}个：\n"
                coc_response += f"力量:{character['STR']}敏捷:{character['DEX']}意志:{character['POW']}\n"
                coc_response += f"体质:{character['CON']}外貌:{character['APP']}教育:{character['EDU']}\n"
                coc_response += f"体型:{character['SIZ']}智力:{character['INT']}幸运:{character['LUCK']}\n"
                coc_response += f"HP:{character['HP']}MP:{character['MP']}SAN:{character['SAN']}\n"
                coc_response += f"体格:{character['Build']}DB:{character['DB']}  点数:[{character['noluck_point_total']}/{character['total_point']}]\n"
            await coc_cmd.send(
                f"{event.sender.nickname}阁下，筱酱为你的扮演生成了这几组数据～请查收！～:\n{coc_response}")
        else:
            coc_response = generate_multiple_characters(int(location))
            await coc_cmd.send(f"{event.sender.nickname}阁下，筱酱为你的扮演生成了这几组数据～请查收！～:\n{coc_response}")
    else:
        await coc_cmd.send(
            f"{event.sender.nickname}阁下，筱酱为你的扮演生成了这几组数据～请查收！～:\n{generate_multiple_characters(1)}")


gpt_chat = on_command("gpt")
@gpt_chat.handle()
async def handle_func(event: MessageEvent, args: Message = CommandArg()):
    if location := args.extract_plain_text():
        user_name = event.sender.nickname
        gpt_response = chat(location)
        await gpt_chat.send(f"{gpt_response}")


jrrp = on_command("jrrp")
@jrrp.handle()
async def handle_func(event: MessageEvent, args: Message = CommandArg()):
    dice_response = str(roll_dice('1d100')[1])
    gpt_response = chat(f"{event.sender.nickname}阁下的当前运势是{dice_response}")
    await jrrp.send(f"{event.sender.nickname}阁下的当前运势是{dice_response}\n{gpt_response}")


skills_roll = on_command('ra', aliases={'rc'})
@skills_roll.handle()
async def handle_func(event: MessageEvent, args: Message = CommandArg()):
    # Regular expression patterns
    pattern = r"^\s*([困难|极难]*?)\s*([\u4e00-\u9fa5]+)\s*(\d+)?\s*$"

    if location := args.extract_plain_text():
        user_name = event.sender.nickname
        user_id = event.user_id

        # 从数据库获取绑定角色的技能
        conn = connect_db()
        group_id = event.group_id if isinstance(event, GroupMessageEvent) else None
        bound_char = get_bound_character(conn, user_id, group_id)

        character_id = None
        if bound_char:
            character_id = bound_char[0]

        existing_skills = {}
        if character_id:
            existing_skills_str = get_character_skills(conn, user_id, character_id)
            existing_skills = eval(existing_skills_str) if existing_skills_str else {}

        # Use regex to parse the command
        match = re.match(pattern, location.strip())

        if match:
            difficulty = match.group(1)
            skill_name = match.group(2)
            input_skill_value = match.group(3)

            # 使用数据库中的技能值（如果有），否则使用用户输入的技能值
            if character_id and skill_name in existing_skills:
                skill_value = existing_skills[skill_name]
            elif input_skill_value:
                skill_value = int(input_skill_value)
            else:
                await skills_roll.send(f"{user_name}阁下，命令格式不正确哦～请提供{skill_name}的数值哦～")
                return

            # 投掷 1d100 骰子
            dice_value = int(roll_dice('1d100')[1])
            gpt_chat=chat(f"s{skill_name}={dice_value} t={dice_value}")
            # 确定成功阈值
            if difficulty == "极难":
                success_threshold = skill_value // 5
            elif difficulty == "困难":
                success_threshold = skill_value // 2
            else:
                success_threshold = skill_value

            # 确定成功等级
            if dice_value == 1:
                message = f"{user_name}阁下的{skill_name}鉴定结果是{dice_value}/{success_threshold}【大成功】\n{gpt_chat}"
            elif dice_value <= success_threshold:
                if difficulty == "极难":
                    message = f"{user_name}阁下的{skill_name}鉴定结果是{dice_value}/{skill_value // 5}【极难成功】\n{gpt_chat}"
                elif difficulty == "困难":
                    message = f"{user_name}阁下的{skill_name}鉴定结果是{dice_value}/{skill_value // 2}【困难成功】\n{gpt_chat}"
                else:
                    message = f"{user_name}阁下的{skill_name}鉴定结果是{dice_value}/{skill_value}【成功】\n{gpt_chat}"
            else:
                message = f"{user_name}阁下的{skill_name}鉴定结果是{dice_value}/{skill_value}【失败】\n{gpt_chat}"

            await skills_roll.send(message)
        else:
            await skills_roll.send(f"{user_name}阁下，命令格式不正确哦～")


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
                        if comp_key not in filtered_props:
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
        #properties = get_character_properties(conn, user_id, character_id) or {}
        try:
            properties = get_character_skills(conn, user_id, character_id)
            properties=eval(properties)
            #await st.send(properties)
        except Exception as e:
            pass

        # 检查是否有运算符号
        match = re.match(r'([^\d+-/*]+)([+-/*])(\d+)', cmd)
        if not match:
            # 更新数据库中的角色技能数据
            update_character_skills(conn, user_id, character_id, str(existing_skills))
            await st.send(f"{user_name}阁下，技能导入完成啦～")

        prop_name = match.group(1).strip()  # 去除空格
        operator = match.group(2)
        value = int(match.group(3))


        if prop_name in SYNONYMS:
            prop_name = SYNONYMS[prop_name]

        current_value = int(properties[prop_name])

        new_value = current_value
        if operator == '+':
            new_value = current_value + value
        elif operator == '-':
            new_value = current_value - value
        elif operator == '*':
            new_value = current_value * value
        elif operator == '/':
            new_value = current_value // value  # 整除

        # 确保新值不会溢出
        new_value = max(min(new_value, 2 ** 31 - 1), -(2 ** 31))

        properties[prop_name] = new_value
        await st.send(f"{user_name}阁下，属性{prop_name}更新成功～ 当前值为：{properties[prop_name]}")
        # 更新属性
        update_character_skills(conn, user_id, character_id, str(properties))
        return




pc = on_command("pc")
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

    if cmd == 'new':
        character_name = rest_args.strip()
        if not character_name:
            await pc.send(f"{user_name}阁下，请提供角色名哦～")
            return

        insert_player(conn, user_id, user_name, character_name)
        await pc.send(f"{user_name}阁下，角色卡 {character_name} 创建成功～")

    elif cmd == 'tag':
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
            structure += f"[{item[0]}]{item[1]}    {bind_status}\n"
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
