### README

本项目是一个骰子骰子核心，现在已经完成了coc（克苏鲁的呼唤），fu（最终物语）相关功能

本项目基于LLonebot与nonebot实现，骰子核心作为nonebot插件形式存在。

想实现的功能：

- [x] 掷骰
- [x] coc技能鉴定
- [x] coc人物卡制成（coc7）
- [x] coc人物导入
- [x] fu背景制成
- [x] 人品投点
- [x] gpt对话
- [x] fu人物导入
- [ ] 牌堆
- [ ] dnd相关
- [ ] 宝可梦相关
- [x] 人物卡操作
- [ ] 改名
- [ ] 退群
- [x] OCR文字识别
- [ ] excel等图表操作
- [ ] 语音
- [ ] AI绘图
- [ ] 

如要使用，请更改相关配置文件：

- database_config.ini
- .env
- .env.prod

数据库使用postgresql，结构如下：

``````
数据库名称：coc
表：
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
	players
		qq_id(主键，索引)   玩家的qq号 varchar
		name   qq名称     varchar
``````

```````
文件目录结构：
├── bot.py      启动文件
├── database_config.ini     数据库配置文件
├── plugin     插件目录
│   ├── dicecore
│   │   ├── database_config.ini    数据库配置文件
│   │   ├── dicecore.py            核心
│   │   ├── dice_database.py       数据库操作
│   │   ├── gpt.py                 gpt对话支持u
│   │   ├── __init__.py            插件
│   │   ├── __pycache__
│   │   │   ├── dicecore.cpython-312.pyc
│   │   │   ├── dice_database.cpython-312.pyc
│   │   │   ├── gpt.cpython-312.pyc
│   │   │   └── __init__.cpython-312.pyc
│   │   └── worker.py               效率相关
│   └── __pycache__
│       └── gpt.cpython-312.pyc
├── __pycache__
├── pyproject.toml                  机器人配置文件
├── README.md

```````

