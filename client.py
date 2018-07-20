# -*- coding: utf-8 -*-
# Author: kai.zhang01
# Date: 2018/7/17 
# Desc:

from config_center.connection import *

import logging

logging = logging.getLogger(__name__)


class ConfigClient():

    def __init__(self, app_name, configs={}, env='beta'):
        """
        获取配置中心客户端
        :param app_name: 应用名称
        :param configs: 配置项列表
        :param env: 环境
        """
        self.app = app_name
        self.configs = configs
        self.env = env

    def getInstance(self):
        return ConfigCenter.getInstance(self.app, self.env)


if __name__ == '__main__':
    app_all_config = ConfigClient(
        app_name='quant',
        env='beta').getInstance().all()
    logging.info('app_all_config:{0}'.format(app_all_config))
    dict = ConfigClient(app_name='quant', env='beta').getInstance().get(
        {'redis_ip': '127.0.0.56', 'redis_port': '1234', 'redis_abc': '1234'})

    print('dict:', dict)

    single_redis_ip = ConfigClient(
        app_name='quant',
        env='beta').getInstance().get(
        'redis_ip',
        '127.0.0.57')

    print('single_redis_ip:', single_redis_ip)
