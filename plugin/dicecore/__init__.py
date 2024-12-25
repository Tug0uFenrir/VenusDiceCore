from nonebot import on_command, get_bot
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, PrivateMessageEvent
from nonebot.params import CommandArg
import re
from plugin.dicecore.dicecore import roll_dice, generate_multiple_characters, bot_info, generate_coc_character, \
    sancheck, generate_fu_character,roll_single_dice
from plugin.dicecore.gpt import *
from .dice_database import *


def is_bot_enabled(group_id,conn):
    '''
    判断bot是否在某个群中被启用
    :param group_id: 群号码
    :param conn: 数据库连接
    :return:
    '''
    group = str(group_id)
    status=get_group_bot_status(conn,group_id)
    return status.lower() == 'on'


set_cmd=on_command("set")
@set_cmd.handle()
async def handle_set(event: MessageEvent,args:Message=CommandArg()):
    '''
    切换规则
    :param event:
    :param args:
    :return:
    '''
    if location := args.extract_plain_text().strip().lower():
        if location in ("coc", "fu", "pokemon", "dnd"):
            group_id = event.group_id if isinstance(event, GroupMessageEvent) else None
            if group_id:
                # 更新数据库中的规则
                conn = connect_db()
                update_group_rule(conn, group_id, location)
                await set_cmd.send(f"已切换规则为 {location}")
            else:
                await set_cmd.send("私聊中无法切换规则哦～")
        else:
            await set_cmd.send("无效的规则，请输入 coc, fu, pokemon 或 dnd")

bot_cmd = on_command("bot")
@bot_cmd.handle()
async def handle_func(event: MessageEvent, args: Message = CommandArg()):
    group_id = event.group_id if isinstance(event, GroupMessageEvent) else None
    if location := args.extract_plain_text():
        if location == "status":
            conn = connect_db()
            status = get_group_bot_status(conn, group_id)
            await bot_cmd.send(f"骰子在该群中的状态为：{status}")
        elif location == "on":
            conn = connect_db()
            update_group_bot_status(conn, group_id, "on")
            await bot_cmd.send("骰子功能已经开启～")
        elif location == "off":
            conn = connect_db()
            update_group_bot_status(conn, group_id, "off")
            #await bot_cmd.send("骰子功能已经关闭～")
    else:
        await bot_cmd.finish(bot_info())

def better_and_punish_roll_skills(value:int,dice_value:int,advantage:str):
    if advantage=="b":
        r2dice=[roll_dice('1d10')[2][0][0], roll_dice('1d10')[2][0][0]]
        switch_number=min(r2dice)
        origin=dice_value
        dice_value=int(str(min(r2dice)) + str(str(dice_value)[-1]))
        if origin<=dice_value:
            dice_value=origin
        return [dice_value,switch_number,origin,"奖励骰"]
    if advantage=="p":
        r2dice = [roll_dice('1d10')[2][0][0], roll_dice('1d10')[2][0][0]]
        switch_number = max(r2dice)
        origin = dice_value
        dice_value = int(str(min(r2dice)) + str(str(dice_value)[-1]))
        if origin>=dice_value:
            dice_value = origin
        return [dice_value,switch_number,origin,"惩罚骰"]

def coc_skills_check(value,skill:str,count_switch,count_number,difficulty:"",advantage:str):
    '''
    :param value: 技能数值
    :param skill: 技能名称
    :param difficulty: 难度
    :param advantage: 奖励惩罚
    :return:
    '''
    jn_success_threshold = value // 5
    kn_success_threshold = value // 2
    value_list = []
    bp_list = []
    result = []
    if count_switch == "#":
        i=0
        while i<int(count_number):
            dice_value = roll_dice('1d100')[2][0][0]
            if difficulty == "困难":
                value = kn_success_threshold
            if difficulty == "极难":
                value = jn_success_threshold
            if advantage == "b":
                bp_list = better_and_punish_roll_skills(value, dice_value, advantage)
                dice_value = bp_list[0]
                result.append(bp_list)
            if advantage == "p":
                bp_list = better_and_punish_roll_skills(value, dice_value, advantage)
                dice_value = bp_list[0]
                result.append(bp_list)
            if dice_value <= value:
                if 1 <= dice_value <= 5:
                    value_list.append(dice_value)
                    value_list.append(value)
                    value_list.append("大成功！")
                elif dice_value <= jn_success_threshold:
                    value_list.append(dice_value)
                    value_list.append(value)
                    value_list.append("极难成功")
                elif dice_value <= kn_success_threshold:
                    value_list.append(dice_value)
                    value_list.append(value)
                    value_list.append("困难成功")
                else:
                    value_list.append(dice_value)
                    value_list.append(value)
                    value_list.append("成功")
            elif dice_value > value:
                if 96 <= dice_value <= 100:
                    value_list.append(dice_value)
                    value_list.append(value)
                    value_list.append("大失败！")
                else:
                    value_list.append(dice_value)
                    value_list.append(value)
                    value_list.append("失败")
            i+=1
    else:
        dice_value = roll_dice('1d100')[2][0][0]
        if difficulty == "困难":
            value = kn_success_threshold
        if difficulty == "极难":
            value = jn_success_threshold

        if advantage == "b":
            bp_list = better_and_punish_roll_skills(value, dice_value, advantage)
            dice_value = bp_list[0]
            result.append(bp_list)
        elif advantage == "p":
            bp_list = better_and_punish_roll_skills(value, dice_value, advantage)
            dice_value = bp_list[0]
            result.append(bp_list)
        if dice_value <= value:
            if 1 <= dice_value <= 5:
                value_list.append(dice_value)
                value_list.append(value)
                value_list.append("大成功！")
            elif dice_value <= jn_success_threshold:
                value_list.append(dice_value)
                value_list.append(value)
                value_list.append("极难成功")
            elif dice_value <= kn_success_threshold:
                value_list.append(dice_value)
                value_list.append(value)
                value_list.append("困难成功")
            else:
                value_list.append(dice_value)
                value_list.append(value)
                value_list.append("成功")
        elif dice_value > value:
            if 96 <= dice_value <= 100:
                value_list.append(dice_value)
                value_list.append(value)
                value_list.append("大失败！")
            else:
                value_list.append(dice_value)
                value_list.append(value)
                value_list.append("失败")
    if count_switch == "#":
        return [value_list,bp_list]
    else:
        result.append(value_list)
        return result



roll_cmd = on_command("r", aliases={'r'})
@roll_cmd.handle()
async def handle_func(event: MessageEvent, args: Message = CommandArg()):
    '''
    roll点功能
    :param event:
    :param args:
    :return:
    '''
    conn = connect_db()
    group_id = event.group_id if isinstance(event, GroupMessageEvent) else None
    rule = get_group_bot_rule(conn, group_id)
    if str(group_id) and not is_bot_enabled(group_id, conn):
        return
    if location := args.extract_plain_text():
            #await roll_cmd.send(location)
            advantage=""
            if location[0] == 'd':
                if len(location) > 1:
                    user_name = event.sender.nickname
                    dice_response = roll_dice(f'1d{location[1:]}')
                    # await roll_cmd.send(dice_response)
                    talk_message = f'''{event.user_id}-{user_name}:t={dice_response}'''
                    gpt_talk = chat(talk_message, 890)
                    await roll_cmd.send(
                        f"{user_name}阁下，筱酱给出答案了哦～答案是.....：\n【{location}={dice_response[1]}】{dice_response[2]}\n{gpt_talk}")
                else:
                    # await roll_cmd.send(location+"d")
                    user_name = event.sender.nickname
                    dice_response = roll_dice('1d100')
                    talk_message = f'''{event.user_id}-{user_name}:t={dice_response}'''
                    gpt_talk = chat(talk_message, 890)
                    await roll_cmd.send(
                        f"{user_name}阁下，筱酱给出答案了哦～答案是.....：\n【{location}={dice_response[1]}】{dice_response[2]}\n{gpt_talk}")
            elif location[0] == 'a':
                if rule == "coc":
                    bind_character=get_bind_character(conn,event.user_id, group_id)
                    skills_dict=None
                    if bind_character:
                        skills_dict=eval(bind_character[3])
                    # 处理输入语句
                    #pattern = r'^([bp]?)(困难|极难)(.+?)(\d*)$'
                    pattern =  r'^([bp]?)(\d*)([#]?)(困难|极难)(.+?)(\d*)$'

                    match = re.match(pattern, str(location[1:]))


                    if match:
                        advantage = match.group(1)
                        count=match.group(2)
                        count_switch=match.group(3)
                        difficulty = match.group(4)
                        skill_name = match.group(5)
                        input_skill_value = match.group(6)



                        skills_check=[]
                        if input_skill_value != "":
                            skill_value = int(input_skill_value)
                            skills_check = coc_skills_check(skill_value, skill_name, count_switch=count_switch,
                                                            difficulty=difficulty,count_number=count,
                                                            advantage=advantage)
                        elif skill_name in skills_dict:
                            skill_value = skills_dict[skill_name]
                            skills_check = coc_skills_check(skill_value, skill_name, count_switch=count_switch,
                                                            difficulty=difficulty,count_number=count,
                                                            advantage=advantage)
                        else:
                            await roll_cmd.send(f"{event.sender.nickname}阁下，命令格式不正确哦～请提供{skill_name}的数值哦～")

                        if skills_check[0]!="" and count_switch!="#":
                            message = f"{event.sender.nickname}阁下的{difficulty}{skill_name}{skills_check[0][3]}鉴定结果是{skills_check[0][0]}[{skills_check[0][2]}]/{skills_check[1][1]}【{skills_check[1][2]}】\n"
                        else:
                            if count_switch=="#":
                                message=f"{event.sender.nickname}阁下的{count}次{advantage}{skill_name}{skill_name}鉴定结果分别是：\n"
                                grouped_data = [skills_check[0][i:i + 3] for i in range(0, len(skills_check[0]), 3)]
                                for group in grouped_data:
                                    message=message+f"{group[0]}/{group[1]} 【{group[2]}】\n"
                                await roll_cmd.send(message+chat(message, 890))

                    else:
                        pattern = r'^([bp]?)(\d*)([#]?)(.+?)(\d*)$'
                        match = re.match(pattern, str(location[1:].strip()))
                        skill_name = match.group(3)
                        if match:
                            advantage = match.group(1)
                            skill_name=match.group(4)
                            input_skill_value = match.group(5)
                            count_switch=match.group(3)
                            count_number=match.group(2)
                            skills_check = []
                            if input_skill_value != "":
                                skill_value = int(input_skill_value)
                                skills_check = coc_skills_check(skill_value, skill_name, difficulty="",
                                                                advantage=advantage,count_switch=count_switch,count_number=count_number)
                            elif skill_name in skills_dict:
                                skill_value = skills_dict[skill_name]
                                skills_check = coc_skills_check(skill_value, skill_name, difficulty="",
                                                                advantage=advantage,count_switch=count_switch,count_number=count_number)
                            if count_switch=="#":
                                message=f"{event.sender.nickname}阁下的{count_number}次{skill_name}鉴定结果分别是：\n"
                                grouped_data = [skills_check[0][i:i + 3] for i in range(0, len(skills_check[0]), 3)]
                                for group in grouped_data:
                                    message=message+f"{group[0]}/{group[1]} 【{group[2]}】\n"
                                #await roll_cmd.send(str(grouped_data))
                                await roll_cmd.send(message+chat(message, 890))
                            else:

                                message = f"{event.sender.nickname}阁下的{skill_name}鉴定结果是{skills_check[0][0]}/{skills_check[0][1]}【{skills_check[0][2]}】\n"
                                message = message + chat(message, 890)
                                await roll_cmd.send(message)
                        else:
                            await roll_cmd.send(
                                f"{event.sender.nickname}阁下，命令格式不正确哦～请提供{skill_name}的数值哦～")
                if rule == "fu":
                    pass
            else:
                # await roll_cmd.send(location+"3")
                dice_response = roll_dice(location)
                user_name = event.sender.nickname
                talk_message = f'''{event.user_id}-{user_name}:t={dice_response}'''
                gpt_talk = chat(talk_message, 890)
                await roll_cmd.send(
                    f"{user_name}阁下，筱酱给出答案了哦～答案是.....：\n【{location}={dice_response[1]}】单个结果：{dice_response[2]}\n{gpt_talk}")
    else:
        user_name = event.sender.nickname
        print(user_name)
        dice_response = str(roll_dice('1d100')[1])
        talk_message = f'''{event.user_id}:t={dice_response}'''
        gpt_talk = chat(talk_message, 890)
        await roll_cmd.send(f"{user_name}阁下，筱酱给出答案了哦～答案是.....：\n【1d100={dice_response}】\n{gpt_talk}")





chat_history={}
gpt_chat = on_command("gpt")
@gpt_chat.handle()
async def handle_func(event: MessageEvent, args: Message = CommandArg()):
    global chat_history
    print(len(str(chat_history)))
    if len(str(chat_history))>=8000:
        #print(len(chat_history))
        chat_history={}
    #conn = connect_db()  # 确保有合适的数据库连接

    group_id = event.group_id if isinstance(event, GroupMessageEvent) else None
    user_id = event.user_id
    history_key = (group_id, user_id)

    if location := args.extract_plain_text():
        # 检查并处理特殊命令
        if location == "get":
            await gpt_chat.send(f"对话记录：{chat_history}")
            return
        elif location == "clean":
            chat_history = {}
            await gpt_chat.send(f"筱酱已经忘记你了哦～")
            return

        user_name = event.sender.nickname

        if history_key not in chat_history:
            chat_history[history_key] = []

        gpt_response, updated_history = chat_pro(f"{event.sender.nickname}({user_id})说:{location}", 4096,
                                                 chat_history[history_key])
        chat_history[history_key] = updated_history

        await gpt_chat.send(f"{gpt_response}")
