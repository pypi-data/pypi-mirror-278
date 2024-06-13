from cjops import command, thread
from loguru import logger
import json
import re
import os

def get_all_ingress(kubectl) -> list:
    """获取所有的ingress
    """
    all_ns_ingress = []
    ingress_command = f'{kubectl} get ingress -A'
    stats, data = command.exec_command(ingress_command)
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
    return all_ns_ingress

def get_tls_name(domain, tls_list) -> str:
    """获取域名对应的tls名称
    """
    tlsName = ''
    for tls in tls_list:
        if tls.get('hosts'):
            if domain in tls.get('hosts'):
                tlsName = tls.get('secretName')
                break
    return tlsName

def get_domin_filter_path(domain, paths, ns, ingress_name, search_type, specData) -> list:
    domin_list = []
    rules_list = specData.get('rules')
    domain_key = re.compile(domain.lower().strip(), re.I) if domain else None
    paths_key = re.compile(paths.lower().strip(), re.I) if paths else None
    for rule in rules_list:
        try:
            if search_type == 'blur':
                if domain_key:
                    if domain_key.search(rule.get('host').lower().strip()):
                        paths_list = rule.get('http').get('paths')
                        if paths_list:
                            for path_list in paths_list:
                                try:
                                    if paths:
                                        if path_list.get('path'):
                                            if paths_key.search(path_list.get('path').lower().strip()):
                                                tlsName = '' if not specData.get('tls', None) else \
                                                    get_tls_name(rule.get('host'), specData.get('tls'))
                                                domin_dict = {'ns': f'{ns}', 'iname': f'{ingress_name}',
                                                            'domain': rule.get('host'), 'path': path_list.get('path'), 'tls': tlsName}
                                                domin_list.append(domin_dict)
                                    else:
                                        tlsName = '' if not specData.get('tls', None) else \
                                            get_tls_name(rule.get('host'), specData.get('tls'))
                                        domin_dict = {'ns': f'{ns}', 'iname': f'{ingress_name}',
                                                    'domain': rule.get('host'), 'path': path_list.get('path'), 'tls': tlsName}
                                        domin_list.append(domin_dict)
                                except Exception as e:
                                    logger.error(f'获取{ns}命名空间下的{ingress_name}的域名失败,报错提示{e}')
                else:
                    paths_list = rule.get('http').get('paths')
                    if paths_list:
                        for path_list in paths_list:
                            paths_string = path_list.get('path')
                            if paths_string:
                                if paths_key.search(paths_string.lower().strip()):
                                    tlsName = '' if not specData.get('tls', None) else \
                                        get_tls_name(rule.get('host'), specData.get('tls'))
                                    domin_dict = {'ns': f'{ns}', 'iname': f'{ingress_name}',
                                                  'domain': rule.get('host'), 'path': path_list.get('path'), 'tls': tlsName}
                                    domin_list.append(domin_dict)
            else:
                if domain:
                    domain = domain.lower().strip()
                    if domain == rule.get('host').lower().strip():
                        paths_list = rule.get('http').get('paths')
                        if paths_list:
                            for path_list in paths_list:
                                try:
                                    if paths:
                                        paths_string = path_list.get('path')
                                        if paths_string:
                                            if paths.lower().strip() == paths_string.lower().strip():
                                                tlsName = '' if not specData.get('tls', None) else \
                                                    get_tls_name(rule.get('host'), specData.get('tls'))
                                                domin_dict = {'ns': f'{ns}', 'iname': f'{ingress_name}',
                                                            'domain': rule.get('host'), 'path': path_list.get('path'), 'tls': tlsName}
                                                domin_list.append(domin_dict)
                                    else:
                                        tlsName = '' if not specData.get('tls', None) else \
                                            get_tls_name(rule.get('host'), specData.get('tls'))
                                        domin_dict = {'ns': f'{ns}', 'iname': f'{ingress_name}',
                                                    'domain': rule.get('host'), 'path': path_list.get('path'), 'tls': tlsName}
                                        domin_list.append(domin_dict)
                                except Exception as e:
                                    logger.error(f'获取{ns}命名空间下的{ingress_name}的域名失败,报错提示{e}')
                else:
                    paths_list = rule.get('http').get('paths')
                    if paths_list:
                        for path_list in paths_list:
                            paths_string = path_list.get('path')
                            if paths_string:
                                if paths.lower().strip() == path_list.get('path').lower().strip():
                                    tlsName = '' if not specData.get('tls', None) else \
                                        get_tls_name(rule.get('host'), specData.get('tls'))
                                    domin_dict = {'ns': f'{ns}', 'iname': f'{ingress_name}',
                                                  'domain': rule.get('host'), 'path': path_list.get('path'), 'tls': tlsName}
                                    domin_list.append(domin_dict)
        except Exception as e:
            logger.error(f'获取{ns}命名空间下的{ingress_name}的域名失败,报错提示: {e}')
    if domin_list:
        # 对domain_list中的每一项dict添加一个字段rule_count
        for item in domin_list:
            item['rule_count'] = len(rules_list)
    return domin_list

def subfilter_ingress(ingress, kubectl, domain, api, kind, **kwargs):
    """
    子过滤器函数,处理单个ingress
    """
    domain_res = None
    ns, ingress_name = ingress
    if ns and ingress_name:
        logger.info(f'开始获取{ns}命名空间下的{ingress_name}的域名')
        temp_file = f"/tmp/{ns}_{ingress_name}_temp.json"
        json_command = f'{kubectl} get ingress {ingress_name} -n {ns} -o json|jq .spec > {temp_file}'
        stats, data = command.exec_command(json_command)
        if stats:
            with open(temp_file, 'r') as f:
                data = json.load(f)
            # 删除temp_file文件
            os.remove(temp_file)
            rules_list = data.get('rules')
            if rules_list:
                domain_res = get_domin_filter_path(domain, api, ns, ingress_name, kind, data)
    return domain_res

def filter_ingress(kubectl, domain, api, kind, workers, **kwargs):
    """
    开始过滤ingress
    """
    if not domain and not api:
        raise Exception("domain和api不能同时为空")
    all_ingress = get_all_ingress(kubectl)
    if not all_ingress:
        raise Exception("没有获取到ingress,请检查!!!!")

    res = thread.run_thread_pool(subfilter_ingress, all_ingress, kubectl=kubectl, domain=domain, api=api, kind=kind, workers=workers, **kwargs)
    return res

if __name__ == '__main__':
    res = subfilter_ingress(('hzpre-hz-storehouse-center', 'mpc-hz-storehouse-center-web'), kubectl='kubectl --kubeconfig=/usr/local/share/k8s/local/config.dev',
                      domain='mpc',
                      api=None,
                      kind='blur')
    print(res)
