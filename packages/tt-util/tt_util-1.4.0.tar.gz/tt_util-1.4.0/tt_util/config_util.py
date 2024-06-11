import os
import yaml
import logging
import sys


class Setting(object):
    def __init__(self):
        self.root_dir = os.getcwd()
        self.default_config_file = self.root_dir + '/config/' + 'setting.default.yaml'
        self.default_config_path = os.path.join(self.root_dir, self.default_config_file)
        self.config_file = self.root_dir + '/config/' + 'setting.yaml'
        self.config_path = os.path.join(self.root_dir, self.config_file)
        self._load_config(self.default_config_path)
        self._load_config(self.config_path)

    def _load_config(self, config_path):
        """
        config_path: yaml配置文件的地址
        加载配置文件
        """
        # 检查是否存在配置文件
        if not os.path.exists(config_path):
            # 退出整个程序
            logging.error(f'没有配置文件:{config_path}!!!')
            sys.exit()

        with open(config_path, 'r', encoding='utf-8') as file:
            config_data = yaml.safe_load(file)

        for section, value in config_data.items():
            # 检查值是否为字典
            if isinstance(value, dict):
                # 如果值是字典，则处理字典中的键值对
                for key, item_value in value.items():
                    attr_name = "{}_{}".format(section.upper(), key.upper())
                    setattr(self, attr_name, item_value)
            else:
                # 如果值不是字典，则直接将该值作为属性添加到实例中
                attr_name = section.upper()
                setattr(self, attr_name, value)


setting = Setting()
