import cjops
from loguru import logger
from .env import get_all_controller
from .ingress import get_all_ingress
import re

def get_json(get_json_command):
    """获取资源的字符串格式
    """
    # 定义一个空的json对象
    project_str = ''
    stats, data = cjops.command.exec_command(get_json_command)
    if stats:
        project_str = str(data)
    return project_str

def sub_filter_yaml_func(resources, kubectl, kind, keyword, **kwargs):
    all_res = {}
    compile_key = re.compile(keyword.lower().strip(), re.I)
    if kind == 'controller':
        ns, tp, name = resources[0], resources[1], resources[2]
        logger.info(f"开始过滤{ns} {tp} {name}的yaml")
        project_str = get_json(f"{kubectl} get {tp} {name} -n {ns} -o json")
        if compile_key.search(project_str.lower()):
            all_res = {
                "ns": ns,
                "tp": tp,
                "name": name
            }

    if kind == 'image':
        ns, tp, name = resources[0], resources[1], resources[2]
        logger.info(f"开始过滤{ns} {tp} {name}的image")
        project_str = get_json(f"{kubectl} get {tp} {name} -n {ns} -o json |jq .spec.template.spec.containers[0].image")
        if compile_key.search(project_str.lower()):
            replics = get_json(f"{kubectl} get {tp} {name} -n {ns} -o json |jq .spec.replicas")
            all_res = {
                "ns": ns,
                "tp": tp,
                "name": name,
                "image": project_str.strip("\n").strip('"'),
                "replics": int(replics)
            }
    if kind == 'ingress':
        ns, ingress_name = resources
        logger.info(f"开始过滤{ns} {ingress_name}的yaml")
        ingress_str = get_json(f"{kubectl} get ingress {ingress_name} -n {ns} -o json")
        if compile_key.search(ingress_str.lower()):
            all_res = {
                "ns": ns,
                "name": ingress_name
            }
    return all_res

def filter_yaml_func(kubectl, kind, keyword, workers, **kwargs):
    """
    过滤资源的yaml文件
    """
    all_resources = []
    if kind == 'controller' or kind == 'image':
        all_resources = get_all_controller(kubectl)
    if kind == 'ingress':
        all_resources = get_all_ingress(kubectl)

    res = cjops.thread.run_thread_pool(sub_filter_yaml_func, all_resources, workers=workers, kubectl=kubectl, kind=kind, keyword=keyword, **kwargs)
    return res
