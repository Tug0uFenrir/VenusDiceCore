from inspect import Arguments

import nonebot
from nonebot import on_command, on_message
from nonebot.adapters.onebot.v11 import Bot, Event, Message
from nonebot.params import CommandArg
import datetime
from .database import update_status,connect_db
import json
import requests
import os
from .analysis import chat
from .get_chat_record import get_chat_record

conn=connect_db()
export_logs=on_command('导出聊天记录',aliases={"export,daochu,导出"},priority=5)
@export_logs.handle()
async def export_chat_recode(bot:Bot, event:Event,args:Message=CommandArg()):
    now=datetime.datetime.now().strftime('%Y-%m-%d')
    if location := args.extract_plain_text():
        group_id=str(location.split()[0])
        upload_group_id=event.group_id
        count=location.split()[1]
        await export_logs.send(f"已导出群[{group_id}]的{count}条记录到文件！正在上传文件，请稍等.....")
        cwd=os.getcwd()+'/'
        path='hunt_logs/'
        file_path=f"{group_id}_{now}_recode.txt"
        with open(path+file_path,"w",encoding="utf-8") as f:
            conn_api=get_chat_record(group_id,count)
            logs=''''''
            for i in conn_api['data']['messages']:
                sender = i['sender']['nickname']
                msg = i['raw_message']
                time=i['time']
                #print(f"[{time}]-{sender}:{msg}")
                logs+=f"[{time}]-{sender}:{msg}\n"
            f.write(logs)
            f.close()
        await bot.call_api("upload_group_file", group_id=upload_group_id, file=str(cwd+path+file_path), name=file_path)




start_logs=on_command('开启记录',aliases={'start_recode','recode','记录'},priority=5)
@start_logs.handle()
async def start_recode(bot:Bot, event:Event,args:Message=CommandArg()):
    group_id=event.group_id


    update_status(conn,group_id,True)

analysis_gpt=on_command('分析')
@analysis_gpt.handle()
async def analysis(bot:Bot, event:Event,args:Message=CommandArg()):
    if location :=args.extract_plain_text():
        group_id=str(location.split()[0])
        count=location.split()[1]
        msgs=get_chat_record(group_id,count)
        logs = ''''''
        for i in msgs['data']['messages']:
            sender = i['sender']['nickname']
            msg = i['raw_message']
            # print(f"[{time}]-{sender}:{msg}")
            logs += f"[{sender}:{msg}\n"
        replay=chat(logs,4096)
        await analysis_gpt.send(replay)




