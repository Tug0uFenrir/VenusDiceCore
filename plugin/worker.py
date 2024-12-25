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


