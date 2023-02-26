from .gelbooru import Gelbooru
from utils.message_builder import custom_forward_msg, image
from utils.http_utils import AsyncHttpx
from utils.utils import is_number
from services.log import logger
from nonebot.adapters.onebot.v11 import Bot, ActionFailed, NetworkError, MessageEvent, GroupMessageEvent, Message
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
    urls={}
    for result in results:
        urls[result.id]=str(result)
    return urls

@gel.handle()
async def _(bot: Bot, event: MessageEvent, arg: Message=CommandArg()):
    text=arg.extract_plain_text().strip()
    urls=await get_random_gelbooru(text)
    if not urls:
        logger.info(f"search failure, text: {text}")
        await gel.finish("搜索出错！", at_sender=True)
    msg_list=[]
    for gel_id in urls:
        url=urls[gel_id]
        logger.info(f"id: {gel_id}, url: {url}")
        tail=f"{gel_id}.jpg"
        path=gel_path/tail
        if path.exists():
            logger.info(f"{tail}已存在")
            msg_list.append(f"gelbooru_id: {gel_id}"+image(path))
        else:
            if await AsyncHttpx.download_file(url, path):
                resize_thumb(path)
                msg_list.append(f"gelbooru_id: {gel_id}"+image(path))
            else:
                msg_list.append(f"gelbooru_id: {gel_id} 图片下载失败！")
                logger.info(f"id: {gel_id} download failure, text: {text}")
    if isinstance(event, GroupMessageEvent):
        try:
            await bot.send_group_forward_msg(
                group_id=event.group_id, 
                messages=custom_forward_msg(msg_list, bot.self_id)
            )
            logger.info(f"success, user: {event.user_id}, group: {group_id}, text: {text}")
        except ActionFailed:
            await gel.send("发送失败！账号可能被风控！", at_sender=True)
            logger.info(f"ActionFailed, user: {event.user_id}, group: {group_id}, text: {text}")
        except NetworkError:
            await gel.send("发送失败！网络连接失败！", at_sender=True)
            logger.info(f"NetworkError, user: {event.user_id}, group: {group_id}, text: {text}")
    else:
        for msg in msg_list:
            try:
                await gel.send(msg)
                logger.info(f"success, user: {event.user_id}, text: {text}")
            except ActionFailed:
                await gel.send("发送失败！账号可能被风控！")
                logger.info(f"ActionFailed, user: {event.user_id}, text: {text}")
            except NetworkError:
                await gel.send("发送失败！网络连接失败！")
                logger.info(f"NetworkError, user: {event.user_id}, text: {text}")
            await asyncio.sleep(1)
