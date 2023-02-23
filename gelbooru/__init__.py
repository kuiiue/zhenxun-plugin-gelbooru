from .gelbooru import Gelbooru
from utils.message_builder import custom_forward_msg
from utils.message_builder import image
from utils.utils import is_number
from services.log import logger
from nonebot.adapters.onebot.v11 import Bot, ActionFailed, NetworkError, MessageEvent, Message
from nonebot.params import CommandArg
from nonebot import on_command

__zx_plugin_name__='gelbooru'

# &api_key=xxx&user_id=yyy
api_key=
user_id=

gel=on_command("gelbooru", priority=5, block=True)

async def get_random_gelbooru(text):
    tags=[]
    limit=10
    for tag in text.split():
        tags.append(tag)
    if is_number(tags[0]):
        limit=int(tags.pop(0))
        if limit>100:
            limit=100
    gelbooru=Gelbooru(api_key, user_id)
    try:
        results=await gelbooru.random_posts(tags=tags, limit=limit)
    except:
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
        logger.info(f"gelbooru: search failure, text: {text}")
        await gel.finish("搜索出错！", at_sender=True)
    msg_list=[]
    for url in urls:
        msg_list.append(image(url))
    try:
        await bot.send_group_forward_msg(
            group_id=event.group_id, 
            messages=custom_forward_msg(msg_list, bot.self_id, '真寻')
        )
        logger.info(f"gelbooru: success, text: {text}")
    except ActionFailed:
        logger.info(f"gelbooru: ActionFailed, text: {text}")
        await gel.finish("发送失败！账号可能被风控！", at_sender=True)
    except NetworkError:
        logger.info(f"gelbooru: NetworkError, text: {text}")
        await gel.finish("发送失败！网络连接失败！", at_sender=True)
