# -*- coding: utf-8 -*-
# Author: kai.zhang01
# Date: 2018/7/17 
# Desc:

# -*- coding: utf-8 -*-
import os
import logging
from kazoo.client import KazooClient
from kazoo.exceptions import *


log = logging.getLogger(__name__)


class ConfigCenter(object):

    def __init__(self, app, env='beta'):
        self.root = 'config_center' # 配置中心根目录
        self.app = app # 应用名
        self.env = env # 环境  默认beta  【test、beta、product】
        self.client = None
        self._connection()

    def _connection(self, hosts='127.0.0.1'):
        """
        zk connection
        :param hosts:
        :return:
        """
        if self.client is None:
            self.client = KazooClient(hosts)
            self.client.start()

    def _close(self):
        if self.client:
            self.client.close()

    def node_path(self, *args):
        """
        拼接zk目录地址
        :param args:
        :return:
        """
        return os.path.join(self.root, self.app, self.env, '/'.join(args))

    def get(self, key, default_value=None):
        nodes = {}
        if key:
            if isinstance(key, dict):
                for k,v in key.items():
                    nodes[k] = self._get(self.node_path(k)) if self._get(self.node_path(k)) else v
                return nodes
            elif key.endswith('*'):
                p = key[0:-1]
                parent_node = self.node_path('')
                leafs = self.client.get_children(parent_node)
                print(leafs)
                for name in leafs:
                    nodes['.'.join([p, name])] = self._get(self.node_path(parent_node, name))
                return nodes
            else:
                node = self.node_path(key.replace('.', '/'))
                return self._get(node) if self._get(node) else default_value
        else:
            return default_value

    def all(self):
        """
        获取应用下所有配置项
        :return:
        """
        # 应用/环境/组
        root = self.node_path('')
        leafs = self.client.get_children(root)
        nodes = {}
        for name in leafs:
            nodes[name] = self._get(self.node_path(name))
        return nodes


    def _get(self, node):
        """
        获取配置项
        :param app:
        :param key: 支持获取单key和一组配置项
        :param env:
        :return: dict{key: vlaue}
        """
        try:

            value = self.client.get(node)[0].decode('utf-8')
        except NoNodeError as e:
            #log.info(traceback.format_exc())
            return None
        return value

    def set(self, key, value = None):
        """
        设置配置项
        :param key:
        :param value:
        :return:
        """
        if isinstance(key, str):
            self._set(self.node_path(key), value)
        elif isinstance(key, dict):
            for key, v in key.items():
                self._set(self.node_path(key), v)

    def _set(self, path, value, env='beta'):
        """
        设置配置项
        :param path: path
        :param value: value 支持单value和字典
        :param env: 环境目录
        :return:
        """
        nodes = {}
        self.create_node_if_not_exist(path)
        self.client.set(path, value.encode())

    def isOpen(self):
        pass


    def create_node_if_not_exist(self, node, creator='kai.zhang'):
        """
        创建目录
        :param center: zk client
        :param node: path
        :param creator: 节点
        :return:
        """
        if not self.client.exists(node):
            self.client.ensure_path(node)


    @staticmethod
    def getInstance(app, env):
        return ConfigCenter(app, env)

