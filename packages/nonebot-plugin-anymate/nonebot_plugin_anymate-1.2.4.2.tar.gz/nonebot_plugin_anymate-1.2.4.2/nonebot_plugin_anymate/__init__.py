from .functions import *

from .tools import db_is_exist
from .config import Config
from .sql_operate import creat_sql, creat_table

from nonebot.plugin import PluginMetadata, get_plugin_config

__plugin_meta__ = PluginMetadata(
    name="AnyMate小助手",
    description="实现对anymate网站的简单帮助",
    usage="使用 /any帮助 来查看指令",
    config=Config,
    supported_adapters=["~onebot.v11"],
    type="application",
    homepage="https://github.com/QuickLAW/nonebot-plugin-anymate"
)

any_config = get_plugin_config(Config)

async def init():
    if db_is_exist(any_config.db_dir):
        pass
    else:
        # 创建数据库和UUID表
        await creat_sql(any_config.db_dir)
        await creat_table(any_config.db_dir, any_config.info_table_name, any_config._info_table_sql)

init()