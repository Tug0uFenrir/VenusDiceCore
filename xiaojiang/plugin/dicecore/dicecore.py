import random
import re


professions = {
    "秘仪师": ["神通", "天选者", "召唤师"],
    "嵌合师": ["德鲁伊", "变形者", "荒野法师"],
    "暗黑之刃": ["复仇者", "黑暗骑士", "死亡骑士"],
    "元素师": ["战斗法师", "地术士", "巫师"],
    "熵师": ["占星师", "混沌法师", "赌徒"],
    "狂怒斗士": ["狂战士", "斗士", "维京人"],
    "守护者": ["圣骑士", "士兵", "用心棒"],
    "博学士": ["档案管理者", "贤者", "学者"],
    "吟唱者": ["大使", "外交官", "艺人"],
    "游荡者": ["强盗", "忍者", "盗贼"],
    "神射手": ["弓箭手", "枪手", "狙击手"],
    "灵师": ["愈师", "牧师", "女巫"],
    "修补匠": ["炼金术士", "魔科技工程师", "机甲师"],
    "旅人": ["冒险家", "探索者", "宝藏猎人"],
    "武器大师": ["斗士", "浪人", "战士"]
}

professions_recommendations = {
    "秘仪师": "万事通",
    "神通": "万事通",
    "天选者": "万事通",
    "召唤师": "万事通",
    "嵌合师": "万事通",
    "德鲁伊": "万事通",
    "变形者": "万事通",
    "荒野法师": "万事通",
    "暗黑之刃": "特化型",
    "复仇者": "特化型",
    "黑暗骑士": "特化型",
    "死亡骑士": "特化型",
    "元素师": "标准",
    "战斗法师": "标准",
    "地术士": "标准",
    "巫师": "标准",
    "熵师": "特化型",
    "占星师": "特化型",
    "混沌法师": "特化型",
    "赌徒": "特化型",
    "狂怒斗士": "特化型",
    "狂战士": "特化型",
    "斗士": "特化型",
    "维京人": "特化型",
    "守护者": "标准",
    "圣骑士": "标准",
    "士兵": "标准",
    "用心棒": "标准",
    "博学士": "万事通",
    "档案管理者": "万事通",
    "贤者": "万事通",
    "学者": "万事通",
    "吟唱者": "万事通",
    "大使": "万事通",
    "外交官": "万事通",
    "艺人": "万事通",
    "游荡者": "标准",
    "强盗": "标准",
    "忍者": "标准",
    "盗贼": "标准",
    "神射手": "标准",
    "弓箭手": "标准",
    "枪手": "标准",
    "狙击手": "标准",
    "灵师": "千方百计",
    "愈师": "千方百计",
    "牧师": "千方百计",
    "女巫": "千方百计",
    "修补匠": "标准",
    "炼金术士": "标准",
    "魔科技工程师": "标准",
    "机甲师": "标准",
    "旅人": "万事通",
    "冒险家": "万事通",
    "探索者": "万事通",
    "宝藏猎人": "万事通",
    "武器大师": "特化型",
    "浪人": "特化型",
    "战士": "特化型"
}


details_rules = {
    "远古的血脉": ["秘仪师", "博学士", "元素师"],
    "逃亡中": ["游荡者", "神射手", "熵师"],
    "古老的信仰": ["博学士", "灵师", "占星师"],
    "寻求正义": ["守护者", "暗黑之刃", "圣骑士"],
    "失宠": ["狂怒斗士", "旅人", "游荡者"],
    "深红之翼": ["旅人", "游荡者", "武器大师"],
    "来自高等学府": ["博学士", "秘仪师", "元素师"],
    "来自月球": ["熵师", "灵师", "元素师"],
    "七海之..": ["旅人", "神射手", "嵌合师"],
    "来自未来": ["修补匠", "元素师", "熵师"],
    "寻求答案": ["博学士", "吟唱者", "秘仪师"],
    "无家可归": ["旅行侠客", "游荡者", "武器大师"],
    "皇家军队": ["守护者", "暗黑之刃", "神射手"],
    "从另一维度而来": ["灵师", "秘仪师", "熵师"],
    "沙漠部落的": ["游荡者", "嵌合师", "狂怒斗士"],
    "风暴骑士团": ["守护者", "狂怒斗士", "武器大师"],
    "拥有一颗金子般的心": ["灵师", "守护者", "吟唱者"],
    "来自古老的森林": ["嵌合师", "旅人", "守护者"],
    "来自过去": ["博学士", "灵师", "元素师"],
    "圣火的....": ["灵师", "秘仪师", "熵师"]
}


traits_rules = {
    "迷人": ["吟唱者", "艺术家"],
    "宣誓": ["守护者", "圣骑士"],
    "被选中": ["秘仪师", "天选者"],
    "前帝国": ["博学士", "历史学家"],
    "多灾多难": ["冒险家", "探索者"],
    "勇敢": ["守护者", "类勇士"],
    "热爱动物": ["德鲁伊", "变形者"],
    "健忘": ["游荡者", "冒险家"],
    "潇洒": ["艺人", "吟唱者"],
    "帝国": ["博学士", "政治家"],
    "无拘无束": ["冒险家", "游荡者"],
    "忠诚": ["守护者", "圣骑士"],
    "年迈": ["博学士", "学者"],
    "骑士精神": ["守护者", "圣骑士"],
    "微笑": ["吟唱者", "艺术家"],
    "简单直接": ["武器大师", "斗士"],
    "初级": ["冒险家", "学徒"],
    "有影响力": ["博学士", "政治家"],
    "脾气暴躁": ["狂怒斗士", "战士"],
    "坚强": ["狂怒斗士", "斗士"],
    "虔诚": ["灵师", "牧师"],
    "最后": ["冒险家", "探索者"],
    "遥远": ["旅人", "探险者"],
    "骄傲": ["神射手", "战士"],
    "被通缉": ["游荡者", "盗贼"],
    "可怕": ["暗黑之刃", "黑暗骑士"],
    "善良": ["灵师", "牧师"],
    "受尊敬": ["博学士", "贤者"],
    "污秽": ["游荡者", "盗贼"],
    "年轻": ["冒险家", "探索者"],
    "古怪": ["巫师", "愈师"],
    "出身名门": ["博学士"],
    "贵族":["灵师","博学士","修补匠"],
    "天真": ["吟唱者", "年轻的艺人"],
    "娇生惯养": ["游荡者", "艺术家"],
    "天赋异禀": ["吟唱者", "艺术家"],
    "皇家": ["守护者"],
    "鲁莽": ["狂怒斗士", "冒险家"],
    "隐秘": ["游荡者", "忍者"],
    "著名": ["博学士", "神射手"],
    "非人": ["暗黑之刃", "死亡骑士"],
    "骑士":["守护者","神射手","死亡骑士"],
    "赏金猎人":["旅人","探险者","赌徒"],
    "保镖": ["守护者", "用心棒"],
    "强盗": ["游荡者", "盗贼"],
    "工厂工人": ["冒险家", "学生","修补匠"],
    "学生": ["学徒", "冒险家","修补匠"],
    "画家": ["艺术家", "吟唱者"],
    "魔科技工程师": ["修补匠", "炼金术士","修补匠"],
    "弓箭手": ["神射手", "枪手"],
    "神秘学家": ["博学士", "占星师"],
    "圣武士": ["守护者", "圣骑士"],
    "僧侣": ["灵师", "牧师"],
    "枪手": ["神射手", "战士"],
    "黑骑士": ["暗黑之刃", "死亡骑士"],
    "飞艇驾驶员": ["旅人", "冒险家","修补匠"],
    "间谍": ["游荡者", "忍者"],
    "机械师": ["修补匠", "魔科技工程师"],
    "圣殿骑士": ["守护者", "圣骑士"],
    "舞者": ["艺人", "吟唱者"],
    "炮手": ["战士", "斗士"],
    "商人": ["政治家", "博学士"],
    "动画木偶": ["奇异生物", "创造者"],
    "清道夫": ["冒险家", "巡逻者"],
    "叛军特工": ["游荡者", "忍者"],
    "战斗法师": ["元素师", "巫师"],
    "决斗者": ["斗士", "狂战士"],
    "怪物猎人": ["冒险家", "战士"],
    "医生": ["灵师", "治疗师"],
    "变形者": ["德鲁伊", "秘法工程师"],
    "海盗": ["冒险家", "勇士"],
    "赌徒": ["英雄", "浪人"],
    "浪人": ["剑士", "斗士"],
    "雇佣兵": ["战士", "冒险家"],
    "厨师": ["探索者", "普通人"],
    "指挥官": ["守护者", "冒险者"],
    "狙击手": ["神射手", "旅人"],
    "运动员": ["狂怒斗士", "探险者"],
    "治疗师": ["灵师", "牧师"],
    "恶魔猎人": ["暗黑之刃", "战士"],
    "恶煞": ["战士", "暗黑之刃"],

}


'''
        "1-2": [
            "骑士", "赏金猎人", "武术家", "寻宝猎人", "外星人", "牧师/修女",
            "教授", "武士", "吟游诗人", "士兵", "发明家", "走私者", "机器人",
            "忍者", "外交官", "盗贼", "国王/王后", "法师", "角斗士", "王子/公主"
        ],
        "3-4": [
            "保镖", "强盗", "工厂工人", "学生", "画家", "魔科技工程师",
            "弓箭手", "神秘学家", "圣武士", "僧侣", "枪手", "黑骑士",
            "飞艇驾驶员", "间谍", "机械师", "圣殿骑士", "舞者", "炮手", "商人"
        ],
        "5-6": [
            "动画木偶", "清道夫", "叛军特工", "战斗法师", "贵族", "决斗者",
            "怪物猎人", "医生", "变形者", "海盗", "赌徒", "浪人",
            "雇佣兵", "厨师", "指挥官","狙击手", "运动员", "治疗师", "恶魔猎人", "恶煞"
        ]
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

        operator_part = re.findall(r'[+\-*/]?\d+', command[dice_part.end():])
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



def fu_character_roll_core():
    # 定义核心表
    core_table = {
        "1-2": [
            "骑士", "赏金猎人", "武术家", "寻宝猎人", "外星人", "牧师/修女",
            "教授", "武士", "吟游诗人", "士兵", "发明家", "走私者", "机器人",
            "忍者", "外交官", "盗贼", "国王/王后", "法师", "角斗士", "王子/公主"
        ],
        "3-4": [
            "保镖", "强盗", "工厂工人", "学生", "画家", "魔科技工程师",
            "弓箭手", "神秘学家", "圣武士", "僧侣", "枪手", "黑骑士",
            "飞艇驾驶员", "间谍", "机械师", "圣殿骑士", "舞者", "炮手", "商人"
        ],
        "5-6": [
            "动画木偶", "清道夫", "叛军特工", "战斗法师", "贵族", "决斗者",
            "怪物猎人", "医生", "变形者", "海盗", "赌徒", "浪人",
            "雇佣兵", "厨师", "指挥官","狙击手", "运动员", "治疗师", "恶魔猎人", "恶煞"
        ]
    }
    roll = int(roll_dice("1d6")[1])

    if 1 <= roll <= 2:
        core_identity = core_table["1-2"][int(roll_dice("1d20")[1])-1]
    elif 3 <= roll <= 4:
        core_identity = core_table["3-4"][int(roll_dice("1d20")[1])-1]
    else:
        core_identity = core_table["5-6"][int(roll_dice("1d20")[1])-1]
    return core_identity


def fu_character_roll_adj():
    adj_table = {
        "1-3": [
            "迷人", "宣誓", "被选中", "前帝国", "多灾多难", "勇敢",
            "热爱动物", "健忘", "潇洒", "帝国", "无拘无束", "忠诚",
            "年迈", "骑士精神", "微笑", "简单直接", "初级", "有影响力",
            "脾气暴躁", "坚强"
        ],
        "4-6": [
            "虔诚", "最后", "遥远", "骄傲", "被通缉", "可怕",
            "善良", "受尊敬", "污秽", "年轻", "古怪", "出身名门",
            "天真", "娇生惯养", "天赋异禀", "皇家", "鲁莽", "隐秘",
            "著名", "非人"
        ]
    }
    roll=int(roll_dice("1d6")[1])
    adj_identity=''
    if 1 <= roll <= 3:
        adj_identity=adj_table["1-3"][int(roll_dice("1d20")[1])-1]
    elif 4 <= roll <= 6:
        adj_identity = adj_table["4-6"][int(roll_dice("1d20")[1]) - 1]
    return adj_identity

def fu_character_roll_detail():
    detail_table = [
        "远古的血脉", "逃亡中", "古老的信仰", "寻求正义", "失宠",
        "深红之翼", "来自高等学府", "来自月球", "七海之..",
        "来自未来", "寻求答案", "无家可归", "皇家军队",
        "从另一维度而来", "沙漠部落的", "风暴骑士团", "拥有一颗金子般的心",
        "来自古老的森林", "来自过去", "圣火的...."
    ]
    roll=int(roll_dice("1d20")[1])
    return detail_table[roll-1]


def generate_fu_character():
    core1 = fu_character_roll_core()
    core2 = fu_character_roll_core()
    adj1 = fu_character_roll_adj()
    adj2 = fu_character_roll_adj()
    detail1 = fu_character_roll_detail()

    # 获取推荐职业
    recommended_professions = generate_professions(detail1, [adj1, adj2])

    # 确保返回的职业唯一，并获取它们的骰子尺寸
    profession_dice_sizes = {}
    for profession in recommended_professions:
        size = professions_recommendations.get(profession, "未推荐")
        profession_dice_sizes[profession] = size

    charter = {
        "identity_core": [core1, core2],
        "identity_adj": [adj1, adj2],
        "identity_detail": [detail1],
        "recommended_professions": recommended_professions,
        "recommended_professions_dice_size": profession_dice_sizes
    }

    return charter

def generate_professions(detail, traits):
    recommended_professions = set(details_rules[detail])
    for trait in traits:
        recommended_professions.update(traits_rules[trait])
    return list(recommended_professions)





