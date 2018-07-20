# config_center
基于zookeeper实现的配置中心。区分环境、统一管理配置项、提供客户端标准服务

使用方法

from config_center.client import *

获取客户端：
client = ConfigClient(
        app_name='app1', # 应用名  
        env='beta' # 环境).getInstance()
        
获取app下所有配置项，返回字典
dict = client.all()

获取某个配置项

client.get('redis_ip', 'default_value')

设置配置项

client.set(key, value)


