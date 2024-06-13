import cjops
from loguru import logger
import re

def get_all_controller(kubectl) -> tuple:
    """
    获取所有控制器
    """
    header = ('命名空间', '控制器类型', '控制器名称')
    all_controllers = []
    controller_command = f'{kubectl} get deploy,sts -A'
    stats, data = cjops.command.exec_command(controller_command)
    if stats:
        try:
            for item in data.split('\n'):
                if 'NAMESPACE' not in item and item:
                    tmp = re.split('[.|/| ]+', item)
                    all_controllers.append((tmp[0], tmp[1], tmp[3]))
        except Exception as e:
            logger.error(f'执行命令{controller_command}获取控制器失败,报错信息,{e}')
    return all_controllers, header

def get_all_ingress(kubectl) -> tuple:
    """
    获取所有的ingress
    """
    header = ('命名空间','ingress名称')
    all_ns_ingress = []
    ingress_command = f'{kubectl} get ingress -A'
    stats, data = cjops.command.exec_command(ingress_command)
    if stats:
        try:
            all_ns_ingress = [
                tuple(item.split()[0:2])
                for item in data.split('\n')
                if not item.startswith('NAMESPACE') and item
            ]
        except Exception as e:
            logger.error(f'拆分ingress结果失败,报错提示{e}')
    else:
        logger.error(f'执行{ingress_command}失败 ')
    return all_ns_ingress, header

def get_all_config(kubectl) -> tuple:
    """
    获取所有configmap和secret
    """
    header = ('命名空间', 'configmap/secret', 'configmap/secret名称')
    all_configmaps = []
    controller_command = f'{kubectl} get configmap,secret -A'
    stats, data = cjops.command.exec_command(controller_command)
    if stats:
        try:
            for item in data.split('\n'):
                if 'NAMESPACE' not in item and item:
                    tmp = re.split('[/| ]+', item)
                    all_configmaps.append((tmp[0], tmp[1], tmp[2]))
        except Exception as e:
            logger.error(f'执行命令{controller_command}获取configmap失败,报错信息,{e}')
    return all_configmaps, header

def ziyuan_get_func(kubectl, kind, **kwargs):
    if kind == 'controller':
        return get_all_controller(kubectl)

    if kind == 'ingress':
        return get_all_ingress(kubectl)

    if kind == 'config':
        return get_all_config(kubectl)
