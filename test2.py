#!/usr/bin/env python
# coding:utf-8

import os
from multiprocessing import Queue
import host3
import time
import paramiko
from openpyxl import Workbook
import numpy as np
from conf import CONF
from openpyxl.styles import colors
from openpyxl.styles import Font
import logging


def write_all_to_excel(head, all_result, collect_file_path):
    # 获取测试主机对数,all_result.shape返回的是(CONF.test_times, pair_num, length + 1)
    pair_num = all_result.shape[1]
    row = pair_num + 1
    collect_xlsx = Workbook()
    all_result_sheet = collect_xlsx.create_sheet(title=u'所有结果')
    all_result_sheet.append(head)
    for seq_result in all_result:
        for result in seq_result:
            all_result_sheet.append(list(result))
        sum_result = list(seq_result.sum(0))
        sum_result[0] = 'sum'
        if pair_num > 1:
            all_result_sheet.append(sum_result)
    max_result = list(all_result[:].sum(1).max(0))
    max_result[0] = 'max'
    all_result_sheet.append(max_result)
    ft_blue = Font(color=colors.BLUE)
    ft_red = Font(color=colors.RED)
    if pair_num > 1:
        while row < len(all_result_sheet.rows):
            for cell in all_result_sheet.rows[row]:
                cell.font = ft_blue
            row += pair_num + 1
    for cell in all_result_sheet.rows[-1]:
        cell.font = ft_red
    collect_xlsx.save(collect_file_path)


def get_scenes_dir(pair_num, mtu):
    script_dir = os.path.split(os.path.realpath(__file__))[0]
    scenes_dir = os.path.join(script_dir, 'test_results', CONF.scenes.format(pair_num=pair_num), mtu)
    if not os.path.exists(scenes_dir):
        os.makedirs(scenes_dir)
    return scenes_dir


def make_head():
    length = 0
    head = ['']
    for i in CONF.cmd_list:
        if 'TCP' in i:
            length += 1
            head.append(u'吞吐Gb({})'.format(i))
        elif 'UDP' in i:
            length += 4
            head.append(u'带宽Gb({})'.format(i))
            head.append(u'时延ms({})'.format(i))
            head.append(u'丢包率%({})'.format(i))
            head.append(u'吞吐Gb({})'.format(i))
    return length, head


def change_node_mtu(mtu):
    for node in CONF.node_list:
        if CONF[node].change_mtu:
            for device in CONF[node].change_mtu_device:
                change_mtu(CONF[node], mtu, device)
            time.sleep(45)


def change_mtu(node, mtu, device):
    # 修改主机mtu
    getmtu = 'cat /sys/class/net/{}/mtu'.format(device)
    changemtu = "echo '{}'>/sys/class/net/{}/mtu".format(mtu, device)
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conn.connect(node.manageip, node.port, node.user, node.password)
    while True:
        stdin, stdout, stderr = conn.exec_command(getmtu)
        cmd_result = stdout.read(), stderr.read()
        cmd_result = ''.join(cmd_result).strip()
        if cmd_result != mtu:
            conn.exec_command(changemtu)
            print u'{} {} change mtu {}--->{}'.format(node.manageip, device, cmd_result, mtu)
        else:
            conn.close()
            print u'{} {} current mtu {}'.format(node.manageip, device, cmd_result)
            break


def get_loger():
    log_file = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'test.log')
    handler = logging.FileHandler(log_file)
    log = logging.getLogger('log')
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)
    return log

loger = get_loger()


def start_test(mtu):
    for pair_num in CONF.test_pair_num:
        print mtu
        change_node_mtu(mtu)
        pair_num = int(pair_num)
        pair_list = CONF.pair_list[:pair_num]
        test_process = []
        all_cmd_q = Queue()
        collect_all_result = Queue()
        scenes_dir = get_scenes_dir(pair_num, mtu)
        length, head = make_head()
        all_result = np.zeros((CONF.test_times, pair_num, length + 1))
        collect_all_result.put(all_result)
        for num, pair in enumerate(pair_list):
            write_process = host3.WriteProcess(loger, num, collect_all_result, scenes_dir, pair, mtu, all_cmd_q, pair_num)
            test_process.append(write_process)
            write_process.start()
        for write_process in test_process:
            write_process.join()
            print 'end'
        all_result = collect_all_result.get()
        collect_file_path = os.path.join(scenes_dir, 'collect_all.xlsx')
        write_all_to_excel(head, all_result, collect_file_path)


def main():
    for mtu in CONF.mtu_list:
        start_test(mtu)

if __name__ == '__main__':
    main()
