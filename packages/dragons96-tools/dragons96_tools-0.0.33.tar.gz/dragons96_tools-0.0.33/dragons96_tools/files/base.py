from loguru import logger as log
from abc import ABC
from typing import Union, Type
from pydantic import BaseModel


def _read_normal_file_data(file_path: str, encoding: str = 'utf-8') -> str:
    with open(file_path, encoding=encoding) as f:
        config_data = f.read()
    return config_data


class DataFileLoader(ABC):
    """数据/文件加载器, 可将str, bytes类型数据或文件数据加载为python基本数据类型或pydantic模型"""

    def load(self,
             config_data: Union[str, bytes],
             encoding: str = 'utf-8',
             modelclass: Union[Type[dict], Type[BaseModel]] = dict,
             **kwargs) -> Union[dict, list, BaseModel]:
        """解析数据字符串到python dict或pydantic.BaseModel子类实例中

        Args:
            config_data: 数据字符串
            encoding: 数据编码类型, config_data 为 bytes 类型需传
            modelclass: 解析的每个记录的模型类型
        """
        model_data = self._convert_config_data_to_python(
            config_data, encoding=encoding, **kwargs)
        if isinstance(model_data, (tuple, list)):
            for i in range(len(model_data)):
                model_data[i] = self._convert_item_to_model(
                    model_data[i], modelclass=modelclass)
            return model_data
        return self._convert_item_to_model(model_data, modelclass=modelclass)

    def load_file(self,
                  file_path: str,
                  encoding: str = 'utf-8',
                  modelclass: Union[Type[dict], Type[BaseModel]] = dict,
                  **kwargs) -> Union[dict, list, BaseModel]:
        """解析文件数据字符串到python dict或pydantic.BaseModel子类实例中

        Args:
            file_path: 文件路径
            encoding: 文件编码
            modelclass: 解析的每个记录的模型类型
        """
        config_data = _read_normal_file_data(
            file_path=file_path, encoding=encoding)
        return self.load(config_data, encoding=encoding, modelclass=modelclass, **kwargs)

    def _convert_item_to_model(self, item: Union[dict, tuple, list],
                               modelclass: Union[Type[dict], Type[list], Type[tuple], Type[BaseModel]]):
        """将单个元素从dict, tuple, list 转换为指定的 modelclass

        Args:
            item: 单个元素类型
            modelclass: 解析的每个记录的模型类型
        """
        if isinstance(item, (tuple, list)):
            # 数组无法转直接返回
            if modelclass not in (tuple, list):
                log.warning(
                    '数据为tuple或list类型, 无法转为指定modelclass: %s, 直接返回', modelclass)
            return item
        if item and isinstance(item, dict):
            return modelclass(**item)
        return item

    def _convert_config_data_to_python(self,
                                       config_data: Union[str, bytes],
                                       encoding: str = 'utf-8',
                                       **kwargs) -> Union[dict, tuple, list]:
        """将数据字符串转为python对象

        Args:
            config_data: 数据
        """
        raise NotImplementedError()
