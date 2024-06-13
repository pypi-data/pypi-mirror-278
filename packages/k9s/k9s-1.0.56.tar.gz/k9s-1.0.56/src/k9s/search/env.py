import cjops
import re
from loguru import logger
import json


def get_all_controller(kubectl) -> list:
    """
    获取所有控制器
    """
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
    return all_controllers

def get_json(kubectl, ns, tp, name):
    """获取json文件
    """
    # 定义一个空的json对象
    project_json = ''
    json_command = f"{kubectl} get {tp} {name} -n {ns} -o json |jq .spec"
    stats, data = cjops.command.exec_command(json_command)
    if stats:
        project_json = json.loads(data)
    return project_json

def get_env(ns, tp, name, project_json, keyword, kind, **kwargs):
    """获取环境变量
    """
    only_value = True if kwargs.get('only_value') else False
    compile_key = re.compile(keyword.lower().strip(), re.I)
    result = []
    try:
        env_list = project_json.get('template').get('spec').get('containers')[0].get('env')
        if env_list:
            if keyword:
                if kind == 'blur':
                    if only_value:
                        result = {dic.get('name'): dic.get('value') for dic in env_list
                              if compile_key.search(str(dic.get('value'))) }
                    else:
                        result = {dic.get('name'): dic.get('value') for dic in env_list
                              if compile_key.search(str(dic.get('value'))) or compile_key.search(str(dic.get('name'))) }
                else:
                    if only_value:
                        result = {dic.get('name'): dic.get('value') for dic in env_list
                              if str(keyword).lower() == str(dic.get('value')).lower()}
                    else:
                        result = {dic.get('name'): dic.get('value') for dic in env_list
                              if str(keyword).lower() == str(dic.get('value')).lower() or str(keyword).lower() == str(dic.get('name')).lower()}
            else:
                result = {dic.get('name'): dic.get('value') for dic in env_list}
        else:
            logger.warning(f'命名空间{ns}下的{tp} {name}没有环境变量')
    except Exception as e:
        logger.error(f'控制器的json文件解析失败,报错信息,{e}')
    return result

def subfilter_env(controller, kubectl, keyword, kind, **kwargs):
    all_env_list = []
    ns, tp, name = controller[0], controller[1], controller[2]
    logger.info(f"开始过滤{ns} {tp} {name}的env")
    project_json = get_json(kubectl, ns, tp, name)
    if project_json:
        result = get_env(ns, tp, name, project_json, keyword, kind, **kwargs)
        if result:
            for k, v in result.items():
                tmp_tuple = {
                    "ns": ns,
                    "tp": tp,
                    "name": name,
                    "key": k,
                    "value": v
                    }
                all_env_list.append(tmp_tuple)
    return all_env_list

def filter_env(kubectl, keyword, kind, workers, **kwargs):
    """
    开始过滤env
    """
    if not keyword:
        logger.warning('搜索的关键词keyword为空,将过滤所有的环境变量,请注意!!!')
    all_controllers = get_all_controller(kubectl)
    if not all_controllers:
        raise Exception("没有获取到控制器,请检查!!!!")

    res = cjops.thread.run_thread_pool(subfilter_env, all_controllers, kubectl=kubectl, keyword=keyword, kind=kind, workers=workers, **kwargs)
    return res