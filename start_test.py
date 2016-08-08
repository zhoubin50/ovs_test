#!/usr/bin/env python
# coding:utf-8

import subprocess
from conf import CONF


if __name__ == '__main__':
    # 启动脚本，如果配置文件中设置使用命名空间则从命名空间启动，否则直接启动
    if CONF.use_namespace:
        namespace = CONF.namespace
        cmd1 = 'ip netns exec {} python ./test2.py'.format(namespace)
    else:
        cmd1 = 'python ./test2.py'
    child1 = subprocess.Popen(cmd1, shell=True)
    child1.wait()
