from nonebot.adapters.onebot.v11 import MessageEvent,Message
from nonebot.plugin.on import on_command
from nonebot.params import CommandArg
from ..dicecore.gpt import baikezongjie
from .browser import *
baikesearch=on_command('search',aliases={'baike','搜索','百科'})
@baikesearch.handle()
async def search(event: MessageEvent,args: Message = CommandArg()):
    if location := args.extract_plain_text():
        text=baidu_baike_search(location)
        await baikesearch.send("搜索内容:\n"+text)
        zongjie=baikezongjie(text,2048)
        await baikesearch.send("AI总结:\n"+zongjie)