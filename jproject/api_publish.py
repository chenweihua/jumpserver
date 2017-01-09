#!/usr/bin/env python
# coding: utf-8

import os, time, socket
from models import PublishConfig, Env ,Publish
from jumpserver.api import get_object

'''
@version  : v1.0
@license  : Apache Licence 
@contact  : endoffight@gmail.com
@site     : 
@Author   : 'cwh'
@Date     : '16-12-22 下午6:34'
@Filename : 'api_publish.py'
@project  : 'jumpserver'
@blog     : 'www.tdd.net'

'''





def db_update_publish_env(**kwargs):
    """
    update a user info in database
    数据库更新用户信息
    """
    env_id = kwargs.pop('env_id')
    env = Env.objects.filter(id=env_id)
    if env:
        project_get = env[0]
        env.update(**kwargs)

    else:
        return None


def db_del_publish_env(env_code):
    """
    delete a user from database
    从数据库中删除用户
    """
    project = get_object(Env, name=env_code)
    if project:
        project.delete()

