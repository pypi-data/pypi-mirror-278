import cjops
from loguru import logger
from pathlib import Path
from .search.ingress import filter_ingress
from .search.env import filter_env
from .search.config import filter_config as filter_config_func
from .search.yaml_filter import filter_yaml_func
from .get.ziyuan_get import ziyuan_get_func

class k8sEntrance:
    _kubeconfig_base_path = "/usr/local/share"
    def __init__(self, env="local", kube_bool=True):
        """
        kube_bool: 是否需要获取kubectl执行命令所需的kubeconfig文件,默认是
        """
        if env not in ["local", "release", "test", "hz", "usa"]:
            raise Exception("env只能为local、test、hz或者usa")
        self._kubeconfig = self._judge_kubeconfig(env, kube_bool)
        self._kubectl = self._judge_command_kubectl(kube_bool)

    def _judge_kubeconfig(self, env, kube_bool) -> str:
        if kube_bool:
            env = 'local' if env in ('local', 'release', 'test') else env
            kubeconfig = Path(self._kubeconfig_base_path) / f"k8s/{env}/config.dev"
            if not kubeconfig.exists():
                raise Exception(f"{kubeconfig}不存在")
            return str(kubeconfig)

    def _judge_command_kubectl(self, kube_bool)->str:
        status, _ = cjops.command.exec_command("kubectl")
        if not status:
            raise Exception('kubectl命令不存在,请检查')
        if kube_bool:
            return f"kubectl --kubeconfig={self._kubeconfig}"
        else:
            return f"kubectl"

    def ingress_search(self, domain=None, api=None, kind="blur", workers=5, writefilebool=True, filename="/tmp/filter_domain.csv", **kwargs):
        """
        搜索ingress配置
        domain: 域名
        api: 接口
        kind: 搜索模式,支持正则和精确匹配
        """
        filter_ingress_config = {
            "kubectl": self._kubectl,
            "domain": domain,
            "api": api,
            "kind": kind,
            "workers": workers,
            **kwargs
        }
        ingress_result = filter_ingress(**filter_ingress_config)
        if ingress_result and writefilebool:
            logger.success("获取到ingress信息,写入到csv文件中")
            cjops.csv.write_csv(ingress_result, filename=filename)
        return ingress_result

    def env_search(self, keyword=None, kind="blur", workers=5, writefilebool=True, filename="/tmp/filter_env.csv", **kwargs):
        """
        搜索环境变量,默认key和value均搜索
        keyword: 搜索关键词
        kind: 搜索模式,支持正则和精确匹配
        only_value: 是否只搜索value,默认false
        """
        filter_ingress_config = {
            "kubectl": self._kubectl,
            "keyword": keyword,
            "kind": kind,
            "workers": workers,
            **kwargs
        }
        env_result = filter_env(**filter_ingress_config)
        if env_result and writefilebool:
            logger.success("获取到env信息,写入到csv文件中")
            cjops.csv.write_csv(env_result, filename=filename)
        return env_result

    def config_search(self, keyword=None, workers=5, writefilebool=True, filename="/tmp/filter_config.csv", **kwargs):
        """
        搜索配置文件;支持configmap、secret
        keyword: 搜索关键字
        """
        filter_config = {
            "kubectl": self._kubectl,
            "keyword": keyword,
            "workers": workers,
            **kwargs
        }
        config_result = filter_config_func(**filter_config)
        if config_result and writefilebool:
            logger.success("获取到config信息,写入到csv文件中")
            cjops.csv.write_csv(config_result, filename=filename)
        return config_result

    def yaml_search(self, kind=None, keyword=None, workers=5, writefilebool=True, filename = f'/tmp/filter_ziyuan_yaml.csv', **kwargs):
        """
        搜索yaml文件; 支持controller、ingress、image
        kind: 搜索范围; 支持controller、ingress、image
        keyword: 搜索关键字
        workers: 搜索线程数
        writefilebool: 是否写入文件
        """
        if kind not in  ["controller", "ingress", "image"]:
            raise Exception("kind参数错误,请使用controller或ingress或image")

        if not keyword:
            raise Exception("keyword参数不能为空")

        filter_yaml = {
            "kubectl": self._kubectl,
            "kind": kind,
            "workers": workers,
            "keyword": keyword,
            **kwargs
        }
        yaml_result = filter_yaml_func(**filter_yaml)
        if yaml_result and writefilebool:
            # print('yaml_result搜索结果', yaml_result)
            logger.success(f"获取到{kind}信息,写入到csv文件中")
            cjops.csv.write_csv(yaml_result, filename=filename)
        return yaml_result

    def ziyuan_get(self, kind=None, writefilebool=True, filename = f'/tmp/ziyuan_get.csv', **kwargs):
        """
        获取k8s资源; 支持controller、ingress、config
        kind: 搜索范围; 支持controller、ingress、config
        writefilebool: 是否写入文件
        """
        if kind not in  ["controller", "ingress", "config"]:
            raise Exception("kind参数错误,请使用controller或ingress")

        ziyuan_yaml = {
            "kubectl": self._kubectl,
            "kind": kind,
            **kwargs
        }

        ziyuan_result, header = ziyuan_get_func(**ziyuan_yaml)
        if ziyuan_result and writefilebool:
            # print('yaml_result搜索结果', yaml_result)
            logger.success(f"获取到{kind}信息,写入到csv文件中")
            cjops.csv.write_csv(ziyuan_result, filename=filename, fieldnames=header)
        return ziyuan_result
