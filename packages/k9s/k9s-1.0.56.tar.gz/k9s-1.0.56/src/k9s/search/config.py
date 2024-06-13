import re
import cjops
from loguru import logger

def get_all_config(kubectl) -> list:
    """获取所有的config
    """
    all_config = []
    ingress_command = f'{kubectl} get configmap,secret -A'
    stats, data = cjops.command.exec_command(ingress_command)
    if stats:
        for item in data.split('\n'):
            if item.startswith('NAMESPACE') or not item:
                continue
            try:
                # 使用re模块对item进行拆分
                ns, tp, config_name = re.split('[/| ]+', item)[0:3]
                all_config.append((ns, tp, config_name))
            except Exception as e:
                logger.error(f'拆分config结果失败,报错提示{e}')
    return all_config

def sub_filter_config(config, kubectl, keyword):
    """
    子线程处理函数
    """
    result = []
    if keyword:
        compile_key = re.compile(keyword.lower().strip(), re.I)
        ns, tp, config_name = config
        if ns and config_name:
            logger.info(f'开始获取{ns}命名空间下的{config_name}配置')
            json_command = f'{kubectl} get {tp} {config_name} -n {ns} -o yaml'
            stats, data = cjops.command.exec_command(json_command)
            if stats:
                if compile_key.search(data.lower()):
                # if keyword.lower().strip() in data.lower():
                    logger.info(f'获取{ns}命名空间下的{config_name}配置成功')
                    result.append({'ns': f'{ns}', 'tp': f'{tp}', 'config_name': f'{config_name}'})
            else:
                logger.error(f'获取{ns}命名空间下的{config_name}配置失败')
    return result

def filter_config(kubectl, keyword, workers, **kwargs):
    """
    搜索配置文件
    """
    if not keyword:
        raise Exception("搜索关键词不能为空")
    all_configs = get_all_config(kubectl)
    if not all_configs:
        raise Exception("未找到配置文件")

    res = cjops.thread.run_thread_pool(sub_filter_config, all_configs, workers=workers, keyword=keyword, kubectl=kubectl)
    return res

