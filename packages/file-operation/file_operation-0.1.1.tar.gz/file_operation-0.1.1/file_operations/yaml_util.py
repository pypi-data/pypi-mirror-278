# 获取项目路径
import os.path

import yaml


class YamlUtil:
    # 读取config.yml文件
    def read_config_file(self, one_node, two_node, comfig_yaml="config/config.yml"):
        with open(comfig_yaml, 'r', encoding='utf-8') as f:
            value = yaml.load(stream=f, Loader=yaml.FullLoader)
            return value[one_node][two_node]

    # 读yml
    def read_yaml(self, yaml_file):
        with open(yaml_file, encoding='utf-8') as f:
            value = yaml.load(stream=f, Loader=yaml.FullLoader)
        return value

    # yaml.yml文件
    def write_yaml(self, data, yaml_file):
        with open(yaml_file, encoding='utf-8', mode='a') as f:
            yaml.dump(data=data, stream=f, allow_unicode=True)

    # 读取extract.yml文件
    def read_yaml_file(self, node_name=None, yaml_file="extract.yml"):
        with open(yaml_file, encoding='utf-8') as f:
            value = yaml.load(stream=f, Loader=yaml.FullLoader)
            if node_name == None:
                return value

            elif node_name:
                return value[node_name]

    # 清空yaml_file文件
    def clear_yaml(self, yaml_file):
        with open(yaml_file, encoding='utf-8', mode='w') as f:
            f.truncate()

    def remove_yaml(self, yaml_file):
        os.remove(yaml_file)
