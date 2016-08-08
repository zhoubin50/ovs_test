#!/usr/bin/env python
# coding:utf-8

from oslo_config import cfg


def conf():
    config = cfg.CONF
    config(default_config_files=['main.conf', 'pairs.conf'])
    default_opts = [
        cfg.ListOpt('mtu_list'),
        cfg.StrOpt('scenes'),
        cfg.StrOpt('filename'),
        cfg.ListOpt('test_pair_num'),
        cfg.ListOpt('pair_list'),
        cfg.ListOpt('node_list'),
        cfg.ListOpt('cmd_list'),
        cfg.IntOpt('test_times'),
        cfg.BoolOpt('use_namespace'),
        cfg.StrOpt('namespace'),
        cfg.StrOpt('iperf_time'),
        ]
    config.register_opts(default_opts)
    node_opts = [
        cfg.StrOpt('manageip'),
        cfg.StrOpt('user'),
        cfg.StrOpt('password'),
        cfg.IntOpt('port'),
        cfg.BoolOpt('change_mtu'),
        cfg.ListOpt('change_mtu_device')
    ]
    for i in config.node_list:
        node_group = cfg.OptGroup(
            name=i,
            title=i
        )
        config.register_group(node_group)
        config.register_opts(node_opts, node_group)

    default_opts = [
        cfg.ListOpt('vm_mtu_list'),
    ]
    config.register_opts(default_opts)
    pair_opts = [
        cfg.StrOpt('server_manage_ip'),
        cfg.StrOpt('server_data_ip'),
        cfg.StrOpt('server_ssh_user'),
        cfg.StrOpt('server_ssh_password'),
        cfg.IntOpt('server_ssh_port'),
        cfg.BoolOpt('server_change_mtu'),
        cfg.ListOpt('server_change_mtu_device'),
        cfg.StrOpt('server_cmd_list'),
        cfg.StrOpt('client_manage_ip'),
        cfg.StrOpt('client_data_ip'),
        cfg.StrOpt('client_ssh_user'),
        cfg.StrOpt('client_ssh_password'),
        cfg.IntOpt('client_ssh_port'),
        cfg.BoolOpt('client_change_mtu'),
        cfg.ListOpt('client_change_mtu_device'),
        cfg.StrOpt('client_cmd_list'),
    ]
    for i in config.pair_list:
        pair_group = cfg.OptGroup(
            name=i,
            title=i
        )
        config.register_group(pair_group)
        config.register_opts(pair_opts, pair_group)
    cmd_opt = [
        cfg.StrOpt('TCP_10G'),
        cfg.StrOpt('UDP_10G'),
        cfg.StrOpt('UDP_10G_1472'),
        cfg.StrOpt('UDP_10G_64'),
        cfg.StrOpt('UDP_10G_256'),
        cfg.StrOpt('UDP_10G_512'),
        cfg.StrOpt('UDP_1G_1472'),
        cfg.StrOpt('UDP_1G_64'),
        cfg.StrOpt('UDP_1G_256'),
        cfg.StrOpt('UDP_1G_512'),
    ]
    server_cmd_group = cfg.OptGroup(name='server_cmd', title='server_cmd')
    config.register_group(server_cmd_group)
    config.register_opts(cmd_opt, server_cmd_group)
    client_cmd_group = cfg.OptGroup(name='client_cmd', title='client_cmd')
    config.register_group(client_cmd_group)
    config.register_opts(cmd_opt, client_cmd_group)
    return config

CONF = conf()
