import ssl
from PIL import Image,ImageEnhance,ImageFilter
import httpx
from io import BytesIO
from nonebot.plugin import on_command
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.params import CommandArg
import pytesseract

message_handler = on_command('ocr')

@message_handler.handle()
async def handle_message(event: MessageEvent, Message=CommandArg()):
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
