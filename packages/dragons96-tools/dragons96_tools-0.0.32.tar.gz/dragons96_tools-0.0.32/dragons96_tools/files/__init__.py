from enum import Enum
from typing import Union, Type, Optional

from pydantic import BaseModel

from .base import DataFileLoader
from .csv import CsvDataFileLoader
from .yaml import YamlDataFileLoader
from .json import JsonDataFileLoader
from .ini import IniDataFileLoader
from .eval import EvalDataFileLoader
from .properties import PropertiesDataFileLoader

_csv_data_file_loader = CsvDataFileLoader()
_yaml_data_file_loader = YamlDataFileLoader()
_json_data_file_loader = JsonDataFileLoader()
_ini_data_file_loader = IniDataFileLoader()
_properties_data_file_loader = PropertiesDataFileLoader()
_eval_data_file_loader = EvalDataFileLoader()


class DataType(Enum):
    """ 数据类型 """
    JSON = (('json',), _json_data_file_loader.load,
            _json_data_file_loader.load_file)
    YAML = (('yaml', 'yml'), _yaml_data_file_loader.load,
            _yaml_data_file_loader.load_file)
    INI = (('ini', 'toml', 'cfg'), _ini_data_file_loader.load,
           _ini_data_file_loader.load_file)
    PROPERTIES = (('properties',), _properties_data_file_loader.load,
                  _properties_data_file_loader.load_file)
    CSV = (('csv', ), _csv_data_file_loader.load,
           _csv_data_file_loader.load_file)
    EVAL = (('eval',), _eval_data_file_loader.load,
            _eval_data_file_loader.load_file)


def get_file_data_type(file_path: str) -> Optional[DataType]:
    """获取文件的数据类型枚举, 若识别不了则返回None

    Args:
        file_path: 文件路径
    """
    file_type = file_path.split('.')[-1]
    file_data_type = None
    for data_type in DataType:
        if file_type in data_type.value[0]:
            file_data_type = data_type
            break
    return file_data_type


class AutoDataFileLoader(DataFileLoader):
    """
    自动检测数据/文件类型加载器
    """

    def load(self,
             config_data: Union[str, bytes],
             modelclass: Union[Type[dict], Type[BaseModel]] = dict,
             data_type: DataType = None,
             header=False,
             **kwargs) -> Union[dict, list, BaseModel]:
        """加载配置数据到python或pydantic模型
        Args:
            config_data: 数据字符串
            modelclass: 模型类型
            data_type: 数据类型, None 表示自动解析 (若知道数据类型推荐传入指定数据类型, 防止自动推断类型错误)
            header: 第一行是否为表头, 仅支持CSV传参
        """
        if data_type:
            return data_type.value[1](config_data,
                                      modelclass=modelclass,
                                      header=header,
                                      use_header_as_key=header)

        for data_type in DataType:
            try:
                return data_type.value[1](config_data,
                                          modelclass=modelclass,
                                          header=header,
                                          use_header_as_key=header)
            except Exception:
                pass
        raise ValueError('无法解析的数据: ' + config_data)

    def load_file(self,
                  file_path: str,
                  encoding: str = 'utf-8',
                  modelclass: Union[Type[dict], Type[BaseModel]] = dict,
                  **kwargs) -> Union[dict, list, BaseModel]:
        """加载文件数据到python对象或pydantic模型

        Args:
            file_path: 文件路径
            encoding: 文件编码类型
            modelclass: 模型类型
        """
        data_type = get_file_data_type(file_path)
        if data_type:
            return data_type.value[2](file_path,
                                      encoding=encoding,
                                      modelclass=modelclass,
                                      **kwargs)

        for data_type in DataType:
            try:
                return data_type.value[2](file_path,
                                          encoding=encoding,
                                          modelclass=modelclass,
                                          **kwargs)
            except Exception:
                pass
        raise ValueError('无法解析的文件: ' + file_path)
