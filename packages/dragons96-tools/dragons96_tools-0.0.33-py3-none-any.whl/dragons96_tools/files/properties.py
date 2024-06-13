from typing import Union

from .base import DataFileLoader


def _load_properties_data(config_data: str):
    def dfs_properties_key(p, keys, value):
        if len(keys) == 1:
            p[keys[0]] = value
            return
        if keys[0] not in p:
            p[keys[0]] = {}
        dfs_properties_key(p[keys[0]], keys[1:], value)

    properties = {}
    for line in config_data.split('\n'):
        if not line.strip() or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        key, value = key.strip(), value.strip()
        keys = key.split(".")
        if len(keys) >= 2:
            dfs_properties_key(properties, keys, value)
        else:
            properties[key] = value

    return properties


class PropertiesDataFileLoader(DataFileLoader):

    def _convert_config_data_to_python(self,
                                       config_data: Union[str, bytes],
                                       encoding: str = 'utf-8',
                                       **kwargs) -> Union[dict, tuple, list]:
        if isinstance(config_data, bytes):
            config_data = config_data.decode(encoding=encoding)
        return _load_properties_data(config_data)
