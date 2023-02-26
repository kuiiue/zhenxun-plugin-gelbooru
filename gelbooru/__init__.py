from .gelbooru import Gelbooru
from utils.message_builder import custom_forward_msg, image
from utils.http_utils import AsyncHttpx
from utils.utils import is_number
from services.log import logger
from nonebot.adapters.onebot.v11 import Bot, ActionFailed, NetworkError, MessageEvent, Message
from nonebot.params import CommandArg
from nonebot import on_command
import asyncio
from .resize import resize_thumb
from configs.path_config import IMAGE_PATH
import os

gel_path=IMAGE_PATH/'gelbooru'
gel_path.mkdir(parents=True, exist_ok=True)

__zx_plugin_name__='gelbooru'

# &api_key=xxx&user_id=yyy
api_key=
user_id=

exclude_tags=['video', 'sound', 'animated']

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
        results=await gelbooru.search_posts(tags=tags, exclude_tags=exclude_tags, limit=limit)
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
    msg_list=[]
    l=len(urls)
    for i in range(l):
        url=urls[i]
        logger.info(f"({i+1}/{l})url: {url}")
        img_id=len(os.listdir(gel_path))
        path=gel_path/f"{img_id}.jpg"
        if await AsyncHttpx.download_file(url, path):
            resize_thumb(path)
            msg_list.append(f"({i+1}/{l})"+image(path))
        else:
            msg_list.append(f"({i+1}/{l})图片下载失败！")
            logger.info(f"({i+1}/{l})download failure, text: {text}")
    try:
        await bot.send_group_forward_msg(
            group_id=event.group_id, 
            messages=custom_forward_msg(msg_list, bot.self_id)
        )
        logger.info(f"success, text: {text}")
    except ActionFailed:
        await gel.send("发送失败！账号可能被风控！")
        logger.info(f"ActionFailed, text: {text}")
    except NetworkError:
        await gel.send("发送失败！网络连接失败！")
        logger.info(f"NetworkError, text: {text}")
