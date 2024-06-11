from typing import Union

from .base import DataFileLoader


class EvalDataFileLoader(DataFileLoader):

    def _convert_config_data_to_python(self,
                                       config_data: Union[str, bytes],
                                       **kwargs) -> Union[dict, tuple, list]:
        return eval(config_data)
