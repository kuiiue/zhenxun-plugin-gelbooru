from .gelbooru import Gelbooru
from utils.message_builder import custom_forward_msg
from utils.message_builder import image
from utils.utils import is_number
from services.log import logger
from nonebot.adapters.onebot.v11 import Bot, ActionFailed, NetworkError, MessageEvent, Message
from nonebot.params import CommandArg
from nonebot import on_command
import asyncio

__zx_plugin_name__='gelbooru'

# &api_key=xxx&user_id=yyy
api_key=
user_id=

gel=on_command("gelbooru", priority=5, block=True)

async def get_random_gelbooru(text):
    tags=[]
    limit=10
    try:
        for tag in text.split():
            tags.append(tag)
        if is_number(tags[0]):
            limit=int(tags.pop(0))
            if limit>20:
                limit=20
    except:
        tags=None
        limit=10
    gelbooru=Gelbooru(api_key, user_id)
    try:
        results=await gelbooru.random_posts(tags=tags, limit=limit)
    except:
        return None
    if not results:
        return None
    urls=[]
    for result in results:
        urls.append(str(result))
    return urls

@gel.handle()
async def _(bot: Bot, event: MessageEvent, arg: Message=CommandArg()):
    text=arg.extract_plain_text().strip()
    urls=await get_random_gelbooru(text)
    if not urls:
        logger.info(f"search failure, text: {text}")
        await gel.finish("搜索出错！", at_sender=True)
    l=len(urls)
    for i in range(l):
        url=urls[i]
        logger.info(f"({i+1}/{l})url: {url}")
        try:
            await gel.send(f"({i+1}/{l})"+image(url))
            logger.info(f"({i+1}/{l})success, text: {text}")
        except ActionFailed:
            logger.info(f"({i+1}/{l})ActionFailed, text: {text}")
            await gel.send(f"({i+1}/{l})发送失败！账号可能被风控！")
        except NetworkError:
            logger.info(f"({i+1}/{l})NetworkError, text: {text}")
            await gel.send(f"({i+1}/{l})发送失败！网络连接失败！")
        await asyncio.sleep(1)
