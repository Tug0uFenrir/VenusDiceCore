import ssl
from PIL import Image,ImageEnhance,ImageFilter
import httpx
from io import BytesIO
from nonebot import on_command, get_bot
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, PrivateMessageEvent
from nonebot.params import CommandArg
import pytesseract
import os
from nonebot_plugin_saa import Image, MessageFactory

message_handler = on_command('ocr')

@message_handler.handle()
async def handle_message(event: MessageEvent):
    message = event.get_message()
    for msg in message:
        if msg.type == "image":
            image_url = msg.data['url']
            await message_handler.send(str(image_url))

            # 创建一个SSL上下文，调整TLS版本
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.options |= ssl.OP_NO_SSLv2
            context.options |= ssl.OP_NO_SSLv3
            context.options |= ssl.OP_NO_TLSv1
            context.options |= ssl.OP_NO_TLSv1_1

            # 使用httpx库打开URL
            try:
                async with httpx.AsyncClient(verify=False) as client:
                    response = await client.get(image_url, timeout=10)
                    image = Image.open(BytesIO(response.content))
                    image = image.convert('L')  # 转换为灰度图
                    enhancer = ImageEnhance.Contrast(image)
                    image = enhancer.enhance(2)  # 提高对比度
                    image = image.filter(ImageFilter.MedianFilter())  # 应用中值滤波去噪
                    image = image.point(lambda x: 0 if x < 140 else 255)  # 二值化
                    text = pytesseract.image_to_string(image, lang='chi_sim')
                    print(text)
                    await message_handler.send(text)
            except httpx.RequestError as e:
                await message_handler.send(f"请求失败：{e}")


terminal_handle=on_command('cmd')
@terminal_handle.handle()
async def terminal_message(event: MessageEvent,args: Message = CommandArg()):
    user_id= event.user_id
    if str(user_id) not in ["815290790","3334279102"]:
        await terminal_handle.send("你不是主人！不允许使用终端模式！")
    else:
        if location := args.extract_plain_text():
            with os.popen(location) as process:
                output = process.read()
                print(output)
                await terminal_handle.send(output)

dalle_e3=on_command('绘画')
@dalle_e3.handle()
async def dalle_e3_handle(event: MessageEvent, args: Message = CommandArg()):
    await dalle_e3.send("因为需要获取云端数据，所以绘画可能需要几分钟才能完成，请安心等待~")
    if location := args.extract_plain_text():
        import requests

        # 定义请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': 'https://ai.rcouyi.com',
            'Referer': 'https://ai.rcouyi.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Dnt': '1',
            'Sec-Gpc': '1',
            'Priority': 'u=0',
            'Te': 'trailers',
            'Content-Type': 'application/json'
        }

        # Bearer token
        authorization_token = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNZW1iZXJJZCI6MjU0MTc3MTE4Mzg0NDUzLCJBY2NvdW50VHlwZSI6MSwiTmlja05hbWUiOiLpq5jogIHluoTnmoTlnJ_ni5ciLCJBY2NvdW50IjoiYWxhbmc0NTdAMTYzLmNvbSIsIkxvZ2luTW9kZSI6MSwiaWF0IjoxNzM0OTU3NzAwLCJuYmYiOjE3MzQ5NTc3MDAsImV4cCI6MTc0MDIxMzcwMCwiaXNzIjoicmNvdXlpQUkiLCJhdWQiOiJyY291eWlBSSJ9.ZKWST8PmW7arSCApa04moDZCWrdg4HKUTCGH8TJmMEc'

        # 设置 Authorization 头
        headers['Authorization'] = authorization_token

        # 模拟 OPTIONS 请求
        def options_request(url):
            response = requests.options(url, headers=headers)
            print(f"OPTIONS Response: {response.status_code}")
            return response

        # 模拟 POST 请求（生成图像）
        def post_drawing_task(url, data):
            response = requests.post(url, headers=headers, json=data)
            print(f"POST /chatapi/drawing/task Response: {response.status_code}")
            print(response.json())
            return response

        # 模拟 POST 请求（获取任务列表）
        def post_drawing_list(url, data):
            response = requests.post(url, headers=headers, json=data)
            print(f"POST /chatapi/drawing/list Response: {response.status_code}")
            print(response.json())
            return response

        # URL 基础路径
        base_url = "https://api-10086.rcouyi.com/chatapi/drawing"

        # 第一部分：OPTIONS 请求 - /task
        print("Sending OPTIONS request for /chatapi/drawing/task")
        await dalle_e3.send("Part1 OPTIONS request for /chatapi/drawing/task")
        options_request(f"{base_url}/task")

        # 第二部分：POST 请求 - /task（生成图像请求）
        drawing_task_data = {
            "model": "dall-e-3",
            "size": 100,
            "n": 1,
            "quality": "standard",
            "prompt": f"{location}"
        }
        print("\nSending POST request for /chatapi/drawing/task (Generate Image)")
        await dalle_e3.send("Part2 POST request for /chatapi/drawing/task (Generate Image)")
        origin_post=post_drawing_task(f"{base_url}/task", drawing_task_data)
        image_Urls=origin_post.json()['result']['imageUrls'][0]
        print(image_Urls)
        msg_builder=MessageFactory([
            Image(image_Urls)
        ])
        await dalle_e3.send("Final Message")
        try:
            await msg_builder.send()
        except Exception as e:
            await dalle_e3.send("抱歉！出现错误了！还请阁下再等一会～")
            #await dalle_e3.send(image_Urls)


