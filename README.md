# zhenxun-plugin-gelbooru
gelbooru plugin for zhenxun-bot  
真寻机器人的gelbooru插件
## 使用库
以[pygelbooru](https://github.com/rainyDayDevs/pygelbooru/)中的[gelbooru.py](https://github.com/rainyDayDevs/pygelbooru/blob/master/pygelbooru/gelbooru.py)为基础，稍加修改
## 使用前安装依赖
在真寻机器人主目录运行`poetry add xmltodict furl`，然后将`gelbooru`文件夹复制到`plugins`文件夹中
## 使用方法
- 将搜索到的图片以合并转发消息的形式发送到群聊中
- **只有基本功能！只能在群聊中使用！没有撤回！没有限制！**
- 需要`api_key`和`user_id`，请到gelbooru[获取](https://gelbooru.com/index.php?page=account&s=options)后填入`__init__.py`相应位置
- 格式：`gelbooru [num] <tags>`  
`[num]`：指定图片数量，可为空，不指定时默认为10  
`<tags>`：gelbooru的tag标准，标签内空格用`_`代替，标签外空格为标签分隔，参考gelbooru的[howto:search](https://gelbooru.com/index.php?page=wiki&s=list&search=howto:search)
- 示例  
`gelbooru white_hair` 返回10张白色头发的图片  
`gelbooru 20 white_pantyhose` 返回20张白色连裤袜的图片
## 注意
- **只有基本功能！只能在群聊中使用！没有撤回！没有限制！**  
只实现了最基础的搜索图片并合并转发功能，没有与真寻插件标准统一，不具备次数限制、频率限制、自动撤回等功能，只能在群聊中使用，请注意。
- **在群聊中涩涩有炸群的可能，请注意！**
