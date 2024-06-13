import json
from typing import Union

from .base import DataFileLoader


class JsonDataFileLoader(DataFileLoader):

    def _convert_config_data_to_python(self,
                                       config_data: Union[str, bytes],
                                       **kwargs) -> Union[dict, tuple, list]:
        return json.loads(config_data)
