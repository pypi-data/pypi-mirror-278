import os, yaml, logging


# 读取yaml
def read_yaml(key: str, filename: str):
    """
    读取yaml配置文件
    :param key:     string      要读取的值的名称
    :param filename: string     配置文件的名字
    :return         *           要读取的值
    """
    try:
        with open(os.getcwd() + '/config/' + filename + '.yaml', encoding="utf-8") as f:
            value = yaml.load(stream=f, Loader=yaml.FullLoader)
            return value[key]
    except:
        logging.error(f"{filename}.yaml文件中没有{key}配置，请检查配置文件！！！")
        raise SystemExit(0)


# 修改yaml
def update_yaml(key, new_value, filename):
    """
    修改yaml
    :param key:     string      要读取的值的名称
    :param new_value: string     修改成的值
    :param filename: string     配置文件的名字
    """
    try:
        with open(os.getcwd() + '/config/' + filename + '.yaml', 'r') as file:
            yaml_data = yaml.safe_load(file)

        if yaml_data is not None:
            yaml_data[key] = new_value

            with open(os.getcwd() + '/config/' + filename + '.yaml', 'w') as file:
                yaml.safe_dump(yaml_data, file, default_flow_style=False)

            logging.info(f"YAML文件 '{filename}' 已成功更新")
        else:
            print(f"YAML文件 '{filename}' 是空的")
    except FileNotFoundError:
        print(f"'{filename}' 找啊不到该文件")
    except Exception as e:
        print(f"出现错误: {e}")


# 追加写入yaml
def write_yaml(data: str, filename: str):
    """
    写入yaml配置
    :param data:        json格式
    :param filename:    配置文件的名字
    """
    with open(os.getcwd() + '/config/' + filename, encoding="utf-8", mode="a") as f:
        yaml.dump(data=data, stream=f, allow_unicode=True)


# 写入yaml
def write_yaml_value(data: str, filename: str):
    """
    写入yaml配置
    :param data:        json格式
    :param filename:    配置文件的名字
    """
    with open(os.getcwd() + '/config/' + filename, encoding="utf-8", mode="w") as f:
        yaml.safe_dump(data=data, stream=f, allow_unicode=True)


# 清空yaml
def clear_yaml(filename: str):
    """
    清空yaml
    :param filename:    配置文件的名字
    """
    with open(os.getcwd() + '/config/' + filename, encoding="utf-8", mode="w") as f:
        f.truncate()


# 读取全部yaml配置
def read_all_yaml(filename: str):
    """
    读取全部yaml配置
    :param filename:    配置文件的名字
    :return:            全部配置
    """
    with open(os.getcwd() + '/config/' + filename, encoding="utf-8") as f:
        value: object = yaml.load(stream=f, Loader=yaml.FullLoader)
        return value
