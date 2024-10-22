from nonebot import on_command, get_bot
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, PrivateMessageEvent
from nonebot.params import CommandArg
import re
from .dicecore import roll_dice, generate_multiple_characters, bot_info, coc_skills_SYMONYS, generate_coc_character,sancheck
from .gpt import *
from .dice_database import *


'''
机器人基础功能代码簇-开始
功能：
set（规则切换）
bot(机器人信息与开关)
jrrp（人品测试）
gpt(gpt聊天)
'''
group_rules = {}
set_cmd = on_command("set")
@set_cmd.handle()
async def handle_set(event: MessageEvent, args: Message = CommandArg()):
    if location := args.extract_plain_text().strip().lower():
        if location in ("coc", "fu", "pokemon","dnd"):
            group_id = event.group_id if isinstance(event, GroupMessageEvent) else None
            if group_id:
                group_rules[group_id] = location
                await set_cmd.send(f"已切换规则为 {location}")
            else:
                await set_cmd.send("私聊中无法切换规则哦～")
        else:
            await set_cmd.send("无效的规则，请输入 coc, fu 或 pkm")



bot_cmd = on_command("bot")
@bot_cmd.handle()
async def handle_func(event: MessageEvent, args: Message = CommandArg()):
    if location := args.extract_plain_text():
        if location == "help":
            messages='''
            你打开了筱酱的大脑，鼓捣了一下她空空的大脑，找到了以下信息：
            基础功能：
            r（投骰子）：变种：rd
            娱乐向功能：
            jrrp：人品
            gpt：和筱酱聊天
            COC规则功能：
            ra（rc）：技能鉴定
                变种：
                    rh：暗骰
                    rap：惩罚骰
                    rab：奖励骰
            sc：san鉴定
            coc：7th人物卡制成
            coc_gpt：coc风格的描写   
            FU规则功能：
                fu：生成一些描述，环境，装备等
            '''

            await bot_cmd.send(f"{messages}\n{chat("你要说：‘我才不是笨蛋呢！’或者使用自己的语言表达这个意思。不要复述下面的内容，只是告知你一下"+messages,max_tokens=400)}")
    else:
        await bot_cmd.send(bot_info())



jrrp = on_command("jrrp")
@jrrp.handle()
async def handle_func(event: MessageEvent, args: Message = CommandArg()):
    dice_response = str(roll_dice('1d100')[1])
    gpt_response = chat(f"{event.sender.nickname}阁下的当前运势是{dice_response}",890)
    await jrrp.send(f"{event.sender.nickname}阁下的当前运势是{dice_response}\n{gpt_response}")



gpt_chat = on_command("gpt")
@gpt_chat.handle()
async def handle_func(event: MessageEvent, args: Message = CommandArg()):
    if location := args.extract_plain_text():
        user_name = event.sender.nickname
        gpt_response = chat(location,800)
        await gpt_chat.send(f"{gpt_response}")

'''
机器人基础功能代码簇-结束
功能：
set（规则切换）
bot(机器人信息与开关)
jrrp（人品测试）
gpt(gpt聊天)
'''



'''
基础功能代码簇-开始
功能：
r（骰点）
rh（暗骰）
ra(技能鉴定)
'''
roll_cmd = on_command("r", aliases={'r'})
@roll_cmd.handle()
async def handle_func(event: MessageEvent, args: Message = CommandArg()):
    if location := args.extract_plain_text():
        try:
            if location[0] == 'd':
                if len(location)>1:
                    user_name = event.sender.nickname
                    dice_response = roll_dice(f'1d{location[1:]}')
                    talk_message = f'''{event.user_id}-{user_name}:t={dice_response}'''
                    gpt_talk = chat(talk_message,890)
                    await roll_cmd.send(
                        f"{user_name}阁下，筱酱给出答案了哦～答案是.....：\n【{location}={dice_response[0]}】\n{gpt_talk}")
                else:
                    user_name = event.sender.nickname
                    dice_response = roll_dice('1d100')
                    talk_message = f'''{event.user_id}-{user_name}:t={dice_response}'''
                    gpt_talk = chat(talk_message, 890)
                    await roll_cmd.send(
                        f"{user_name}阁下，筱酱给出答案了哦～答案是.....：\n【{location}={dice_response[0]}】\n{gpt_talk}")
            else:
                dice_response = str(roll_dice(location)[1])
                user_name = event.sender.nickname
                talk_message = f'''{event.user_id}-{user_name}:t={dice_response}'''
                gpt_talk = chat(talk_message,890)
                await roll_cmd.send(
                    f"{user_name}阁下，筱酱给出答案了哦～答案是.....：\n【{location}={dice_response}】\n{gpt_talk}")

        except Exception as e:
            pass
    else:

        user_name = event.sender.nickname
        print(user_name)
        dice_response = str(roll_dice('1d100')[1])
        talk_message = f'''{event.user_id}:t={dice_response}'''
        gpt_talk = chat(talk_message,890)
        await roll_cmd.send(f"{user_name}阁下，筱酱给出答案了哦～答案是.....：\n【1d100={dice_response}】\n{gpt_talk}")



rh_cmd=on_command("rh")
@rh_cmd.handle()
async def handle_func(event: MessageEvent, args: Message = CommandArg()):
    bot = get_bot()
    if location := args.extract_plain_text():
        if location[0] == 'd':
            if len(location) > 1:
                user_name = event.sender.nickname
                dice_response = roll_dice(f'1d{location[1:]}')
                talk_message = f'''{event.user_id}-{user_name}:t={dice_response}'''
                await roll_cmd.send("#小声凑到你的耳边'筱酱和你说的悄悄话千万不能告诉别人哦～'")
                await bot.send_private_msg(user_id=event.user_id,
                                           message=f"{user_name}阁下，筱酱给出答案了哦～答案是.....：\n【{location}={dice_response}】\n{chat(talk_message, 890)}")
            else:
                user_name = event.sender.nickname
                dice_response = roll_dice('1d100')
                talk_message = f'''{event.user_id}-{user_name}:t={dice_response}'''
                await roll_cmd.send("#小声凑到你的耳边'筱酱和你说的悄悄话千万不能告诉别人哦～'")
                await bot.send_private_msg(user_id=event.user_id,
                                           message=f"{user_name}阁下，筱酱给出答案了哦～答案是.....：\n【{location}={dice_response}】\n{chat(talk_message, 890)}")
    else:
        dice_response = str(roll_dice('1d100')[1])
        user_name = event.sender.nickname
        talk_message = f'''{event.user_id}-{user_name}:t={dice_response}'''
        await roll_cmd.send("#小声凑到你的耳边'筱酱和你说的悄悄话千万不能告诉别人哦～'")
        await bot.send_private_msg(user_id=event.user_id,
                                   message=f"{user_name}阁下，筱酱给出答案了哦～答案是.....：\n【1d100={dice_response}】\n{chat(talk_message, 890)}")



skills_roll = on_command('ra', aliases={'rc'})
@skills_roll.handle()
async def handle_func(event: MessageEvent, args: Message = CommandArg()):
    group_id = event.group_id if isinstance(event, GroupMessageEvent) else None
    rule = group_rules.get(group_id, "coc")  # 默认使用 coc 规则
    if location := args.extract_plain_text():
        user_name = event.sender.nickname

        # 连接数据库并获取角色信息
        conn = connect_db()
        bound_char = get_bound_character(conn, event.user_id, group_id)
        character_id = None
        if bound_char:
            character_id = bound_char[0]
        existing_skills = {}
        if character_id:
            existing_skills_str = get_character_skills(conn, event.user_id, character_id)
            existing_skills = eval(existing_skills_str) if existing_skills_str else {}

        if rule == "coc":
            # COC规则处理
            pattern = r'^\s*([bp]?)\s*([困难|极难]*?)\s*([\u4e00-\u9fa5]+)\s*(\d+)?\s*$'
            match = re.match(pattern, location.strip())
            user_name = event.sender.nickname
            user_id = event.user_id

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

            match = re.match(pattern, location.strip())

            if match:
                advantage_letter = match.group(1)
                difficulty = match.group(2)
                skill_name = match.group(3)
                input_skill_value = match.group(4)

                advantage = 0
                if advantage_letter == "b":
                    advantage = 1
                elif advantage_letter == "p":
                    advantage = -1

                if character_id and skill_name in existing_skills:
                    skill_value = existing_skills[skill_name]
                elif input_skill_value:
                    skill_value = int(input_skill_value)
                else:
                    await skills_roll.send(f"{user_name}阁下，命令格式不正确哦～请提供{skill_name}的数值哦～")
                    return

                formula, dice_value = roll_dice('1d100', advantage)
                gpt_chat = chat(f"s{skill_name}={dice_value} t={dice_value}", 890)

                if difficulty == "极难":
                    success_threshold = skill_value // 5
                elif difficulty == "困难":
                    success_threshold = skill_value // 2
                else:
                    success_threshold = skill_value

                if dice_value == 1:
                    message = f"{user_name}阁下的{skill_name}鉴定结果是{formula}/{success_threshold}【大成功】\n{gpt_chat}"
                elif dice_value <= success_threshold:
                    if difficulty == "极难":
                        message = f"{user_name}阁下的{skill_name}鉴定结果是{formula}/{skill_value // 5}【极难成功】\n{gpt_chat}"
                    elif difficulty == "困难":
                        message = f"{user_name}阁下的{skill_name}鉴定结果是{formula}/{skill_value // 2}【困难成功】\n{gpt_chat}"
                    else:
                        message = f"{user_name}阁下的{skill_name}鉴定结果是{formula}/{skill_value}【成功】\n{gpt_chat}"
                else:
                    message = f"{user_name}阁下的{skill_name}鉴定结果是{formula}/{skill_value}【失败】\n{gpt_chat}"

                await skills_roll.send(message)
            else:
                await skills_roll.send(f"{user_name}阁下，命令格式不正确哦～")
        if rule=="fu":
            pass
        if rule == "pokemon":
            pass

'''
此处为基础功能代码簇-结束
'''



'''
COC规则功能呢个代码簇-开始
功能:
coc（人物制成）
coc_gpt（coc风格gpt）
sc（san鉴定）
'''
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
                    if 400 <= total_points <= 700:
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


coc_gpt_env=on_command("coc_gpt")
@coc_gpt_env.handle()
async def handle_func(event: MessageEvent, args: Message = CommandArg()):
    if location := args.extract_plain_text():
        user_name = event.sender.nickname
        gpt_response = chat_coc_env_write(location,4095)
        await gpt_chat.send(f"{gpt_response}")

sc_cmd = on_command("sc")
@sc_cmd.handle()
async def handle_sancheck(event: MessageEvent, args: Message = CommandArg()):
    user_name = event.sender.nickname
    user_id = event.user_id
    conn = connect_db()

    # 提取参数
    if location := args.extract_plain_text():
        parts = location.split('/')
        if len(parts) != 2:
            await sc_cmd.send(f"{user_name}阁下，命令格式不正确哦～请用 sc<成功后的损失>/<失败后的损失> 格式。")
            return

        success_deduction, failure_deduction = parts

        # 获取理智值
        group_id = event.group_id if isinstance(event, GroupMessageEvent) else None
        bound_char = get_bound_character(conn, user_id, group_id)

        if not bound_char:
            await sc_cmd.send(f"{user_name}阁下，您尚未新建角色卡或绑定角色卡，无法进行理智检定哦～")
            return

        character_id = bound_char[0]
        properties = get_character_properties(conn, user_id, character_id)
        current_sanity = properties.get('理智', None) or properties.get('san', None)

        if current_sanity is None:
            await sc_cmd.send(f"{user_name}阁下，您的角色属性中未找到理智值哦～")
            return

        # 进行理智检定
        roll_result, success, new_sanity, deduction = sancheck(current_sanity, success_deduction, failure_deduction)

        # 更新理智值到数据库
        update_character_sanity(conn, user_id, character_id, new_sanity)

        if success:
            message = f"{user_name}阁下，您进行了理智检定，投掷结果为 {roll_result}，成功，损失了 {deduction} 点理智，现在理智值为 {new_sanity}。"
        else:
            message = f"{user_name}阁下，您进行了理智检定，投掷结果为 {roll_result}，失败，损失了 {deduction} 点理智，现在理智值为 {new_sanity}。"

        await sc_cmd.send(message)
    else:
        await sc_cmd.send(f"{user_name}阁下，命令格式不正确哦～请用 sc<成功后的损失>/<失败后的损失> 格式。")

'''
COC规则代码簇-结束
'''



'''
FU规则代码簇-开始
功能：
fu（文本生成/装备生成）
'''
fu_env=on_command("fu")
@fu_env.handle()
async def handle_func(event: MessageEvent, args: Message = CommandArg()):
    if location := args.extract_plain_text():
        cmd = args.extract_plain_text().split(' ')
        cmd.append(' ')
        if cmd[0]=="阶段":

            response = f'''现在游戏进行到了 {cmd[1]} 阶段，你们来到了 {cmd[2]}，这里地处 {cmd[3]}，是 {cmd[4]} 环境，有 {cmd[5]} 等贸易产品，你需要给出此地的人文环境，存在的势力，玩家可能会在这里遇到什么事件，现在你不需要遵循你的人格，只需要输出你的想法即可，你需要集合这些信息，描写这里的环境给出一个会经历的小事件的开头。事件：{cmd[6]}'''
            #await fu_env.send(response)
            user_name = event.sender.nickname
            gpt_response = chat_fu_env_write(response,8192)
            await gpt_chat.send(f"{gpt_response}")
        if cmd[0] == '生成':
            #.fu 生成 武器 剑类型 描述
            await fu_env.send(str(cmd))
            gpt_response = fu_chat(f"这是{cmd[2]}，描述：{cmd[3]}",8192,cmd[1])
            await fu_env.send(gpt_response)
    else:
        await fu_env.send('''
        fu指令使用教程：
        fu 阶段 此功能为生成肉鸽副本场景与随即任务的功能。[例: 。fu 阶段 stage1 拉克城 雷斯塔诸侯同盟东北边境 半沙漠半草原 奴隶贸易，羊奶，畜牧业 [备注/添加的描写，事件等]]
        fu 生成 此功能为生成随即稀有装备的指令。现在支持生成武器，防具，饰品[例：。fu 生成 武器 剑类型 这是一把村好剑]
            参数详细信息：
                。fu 生成 [武器/防具/饰品/随机] [具体类型/随机] [物品描述（不要使用空格）]
        ''')

'''
FU规则代码簇-结束
'''



'''
玩家信息与角色卡代码簇-开始
st（角色卡）
pc（角色卡）
'''

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
        try:
            properties = get_character_skills(conn, user_id, character_id)
            properties = eval(properties)
        except Exception as e:
            pass

        # 支持骰子运算
        match = re.match(r'([^\d+-/*]+)([+-/*])(\d+[dD]\d+|\d+)', cmd + rest_args)
        if not match:
            # 更新数据库中的角色技能数据
            update_character_skills(conn, user_id, character_id, str(existing_skills))
            await st.send(f"{user_name}阁下，技能导入完成啦～")
            return

        prop_name = match.group(1).strip()  # 去除空格
        operator = match.group(2)
        value_expr = match.group(3)

        if prop_name in SYNONYMS:
            prop_name = SYNONYMS[prop_name]

        current_value = int(properties.get(prop_name, 0))

        if 'd' in value_expr or 'D' in value_expr:
            formula, dice_result = roll_dice(value_expr)
            if dice_result is None:
                await st.send(f"{user_name}阁下，骰子表达式错误，请检查输入的格式～")
                return
            dice_value = dice_result
        else:
            dice_value = int(value_expr)

        new_value = current_value
        if operator == '+':
            new_value = current_value + dice_value
        elif operator == '-':
            new_value = current_value - dice_value
        elif operator == '*':
            new_value = current_value * dice_value
        elif operator == '/':
            new_value = current_value // dice_value  # 整除

        # 确保新值不会溢出
        new_value = max(min(new_value, 2 ** 31 - 1), -(2 ** 31))

        properties[prop_name] = new_value
        await st.send(f"{user_name}阁下，属性{prop_name}更新成功～ 当前值为：{properties[prop_name]}")
        # 更新属性
        update_character_skills(conn, user_id, character_id, str(properties))
        return

    # 更新数据库中的角色技能数据
    update_character_skills(conn, user_id, character_id, str(existing_skills))
    #await st.send(f"{user_name}阁下，技能导入完成啦～")

'''
玩家信息与角色卡代码簇-结束
'''