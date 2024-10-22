import random
import re

'''
def roll_dice(command):
    """
    这里是处理骰子roll点的函数，默认为1D100
    """
    # 骰子运算部分
    dice_part = re.match(r'(\d*)[dD](\d+)', command)
    if not dice_part:
        return None, "Invalid dice command"

    count = int(dice_part.group(1)) if dice_part.group(1) else 1
    sides = int(dice_part.group(2))

    dice_results = [random.randint(1, sides) for _ in range(count)]
    dice_str = "[" + "]+[".join(map(str, dice_results)) + "]"
    total = sum(dice_results)

    formula = dice_str

    operator_part = re.findall(r'[\+\-\*/]?\d+', command[dice_part.end():])
    for op in operator_part:
        symbol = op[0] if not op[0].isdigit() else '+'
        number = int(op if symbol == '+' else op[1:])
        if symbol == '+':
            total += number
            formula += f"+{number}"
        elif symbol == '-':
            total -= number
            formula += f"-{number}"
        elif symbol == '*':
            total *= number
            formula += f"*{number}"
        elif symbol == '/':
            total //= number
            formula += f"/{number}"

    formula += f"={total}"
    return formula,total

'''



def roll_dice(command, advantage=0):
    """
    处理骰子roll点的函数，默认为1d100
    """

    # 骰子运算部分
    dice_part = re.match(r'(\d*)[dD](\d+)', command)
    if not dice_part:
        return None, "Invalid dice command"

    count = int(dice_part.group(1)) if dice_part.group(1) else 1
    sides = int(dice_part.group(2))

    dice_results = [random.randint(1, sides) for _ in range(count)]
    dice_str = "[" + "]+[".join(map(str, dice_results)) + "]"

    if count == 1 and sides == 100 and advantage != 0:
        tens = [random.randint(0, 9) * 10 for _ in range(abs(advantage))]
        best_ten = min(tens) if advantage > 0 else max(tens)
        ones = random.randint(0, 9)
        total = best_ten + ones
        dice_str = f'{best_ten}[奖励投:{",".join(map(str, tens))}]' if advantage > 0 else f'{best_ten}[惩罚投:{",".join(map(str, tens))}]'

    else:
        total = sum(dice_results)
        formula = dice_str

        operator_part = re.findall(r'[\+\-\*/]?\d+', command[dice_part.end():])
        for op in operator_part:
            symbol = op[0] if not op[0].isdigit() else '+'
            number = int(op if symbol == '+' else op[1:])

            if symbol == '+':
                total += number
                formula += f"+{number}"
            elif symbol == '-':
                total -= number
                formula += f"-{number}"
            elif symbol == '*':
                total *= number
                formula += f"*{number}"
            elif symbol == '/':
                total //= number
                formula += f"/{number}"

        formula += f"={total}"
        return formula, total

    return f'{dice_str}+[{ones}]={total}', total


def generate_coc_character():
    character = {
        'STR': roll_dice("3d6*5")[1],
        'DEX': roll_dice("3d6*5")[1],
        'POW': roll_dice("3d6*5")[1],
        'CON': roll_dice("3d6*5")[1],
        'APP': roll_dice("3d6*5")[1],
        'EDU': roll_dice("2d6+6*5")[1],
        'SIZ': roll_dice("2d6+6*5")[1],
        'INT': roll_dice("2d6+6*5")[1],
        'LUCK': roll_dice("3d6*5")[1],
    }
    character['total_point'] = sum(character.values())
    character['noluck_point_total'] = character['total_point'] - character['LUCK']

    character['HP'] = (character['CON'] + character['SIZ']) // 10
    character['MP'] = character['POW'] // 5
    character['SAN'] = character['POW']

    total_str_siz:int= int(character['STR']) + int(character['SIZ'])
    if total_str_siz <= 64:
        character['DB'] = '-2'
        character['Build'] = '-2'
    elif 65 <= total_str_siz <= 84:
        character['DB'] = '-1'
        character['Build'] = '-1'
    elif 85 <= total_str_siz <= 124:
        character['DB'] = '0'
        character['Build'] = '0'
    elif 125 <= total_str_siz <= 164:
        character['DB'] = '+1d4'
        character['Build'] = '1'
    elif 165 <= total_str_siz <= 204:
        character['DB'] = '+1d6'
        character['Build'] = '2'
    elif 205 <= total_str_siz <= 284:
        character['DB'] = '+2d6'
        character['Build'] = '3'
    elif 285 <= total_str_siz <= 364:
        character['DB'] = '+3d6'
        character['Build'] = '4'
    elif 365 <= total_str_siz <= 444:
        character['DB'] = '+4d6'
        character['Build'] = '5'
    else:
        character['DB'] = '+5d6'
        character['Build'] = '6'

    return character


def sancheck(current_sanity, success_deduction, failure_deduction):
    roll_result = roll_dice('1d100')[1]  # 投1D100 骰子
    success = roll_result <= current_sanity  # 检查是否成功
    if success:
        if "d" in success_deduction or "D" in success_deduction:
            deduction = roll_dice(success_deduction)[1]
        else:
            deduction = eval(success_deduction)
    else:
        if "d" in failure_deduction or "D" in failure_deduction:
            deduction = roll_dice(failure_deduction)[1]
        else:
            deduction = eval(failure_deduction)
    new_sanity = max(0, current_sanity - deduction)  # 确保不会出现负数的理智值
    return roll_result, success, new_sanity, deduction



def generate_multiple_characters(count=1):
    all_characters = [generate_coc_character() for _ in range(count)]

    result = ""

    for idx, character in enumerate(all_characters):
        result += f"COC7th人物制成第{idx + 1}个：\n"
        result += f"力量:{character['STR']}敏捷:{character['DEX']}意志:{character['POW']}\n"
        result += f"体质:{character['CON']}外貌:{character['APP']}教育:{character['EDU']}\n"
        result += f"体型:{character['SIZ']}智力:{character['INT']}幸运:{character['LUCK']}\n"
        result += f"HP:{character['HP']}MP:{character['MP']}SAN:{character['SAN']}\n"
        result += f"体格:{character['Build']}DB:{character['DB']}  点数:[{character['noluck_point_total']}/{character['total_point']}]\n"
    return result


def bot_info():
    text='''
    Dice筱酱By高老庄的土狗
    DiceCore:VenusCoreV1.0Bate
    CoreBy:高老庄的土狗
    GPTVersion:GPT-3.5-Turbo
    '''
    return text


def coc_skills_SYMONYS():
    SYNONYMS = {
        '力量': '力量',
        'str': '力量',
        '敏捷': '敏捷',
        'dex': '敏捷',
        '意志': '意志',
        'pow': '意志',
        '体质': '体质',
        'con': '体质',
        '外貌': '外貌',
        'app': '外貌',
        '教育': '教育',
        'edu': '教育',
        '体型': '体型',
        'siz': '体型',
        '智力': '智力',
        '灵感': '智力',
        'int': '智力',
        '理智': 'san',
        'san': 'san',
        'san值':'san',
        '理智值':'san',
        '幸运': '幸运',
        '运气': '幸运',
        '魔法': '魔法',
        'mp': '魔法',
        '体力': '体力',
        'hp': '体力',
        '会计': '会计',
        '人类学': '人类学',
        '估价': '估价',
        '考古学': '考古学',
        '乐理': '乐理',
        '取悦': '取悦',
        '魅惑': '取悦',
        '攀爬': '攀爬',
        '计算机使用': '计算机使用',
        '计算机': '计算机使用',
        '电脑': '计算机使用',
        '信用评级': '信用评级',
        '信用': '信用评级',
        '信誉': '信用评级',
        '克苏鲁神话': '克苏鲁神话',
        '克苏鲁': '克苏鲁神话',
        '乔装': '乔装',
        '闪避': '闪避',
        '汽车驾驶': '汽车驾驶',
        '汽车': '汽车驾驶',
        '驾驶': '汽车驾驶',
        '电气维修': '电气维修',
        '电子学': '电子学',
        '话术': '话术',
        '斗殴': '斗殴',
        '手枪': '手枪',
        '急救': '急救',
        '历史': '历史',
        '恐吓': '恐吓',
        '跳跃': '跳跃',
        '母语': '母语',
        '法律': '法律',
        '图书馆使用': '图书馆使用',
        '图书馆': '图书馆使用',
        '聆听': '聆听',
        '开锁': '开锁',
        '撬锁': '开锁',
        '锁匠': '开锁',
        '机械维修': '机械维修',
        '医学': '医学',
        '博物学': '博物学',
        '自然学': '博物学',
        '领航': '领航',
        '导航': '领航',
        '神秘学': '神秘学',
        '重型操作': '重型操作',
        '重型机械': '重型操作',
        '操作重型机械': '重型操作',
        '说服': '说服',
        '精神分析': '精神分析',
        '心理学': '心理学',
        '骑术': '骑术',
        '妙手': '妙手',
        '侦查': '侦查',
        '潜行': '潜行',
        '生存': '生存',
        '游泳': '游泳',
        '投掷': '投掷',
        '追踪': '追踪',
        '驯兽': '驯兽',
        '潜水': '潜水',
        '爆破': '爆破',
        '读唇': '读唇',
        '催眠': '催眠',
        '炮术': '炮术',
    }

    return SYNONYMS
