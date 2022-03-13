import configparser
import pathlib
import os


class ConfigLoader:
    # Only one instance of config is generated on each robot thread,
    # since the config is a constant, there's no need to reload it.
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self, config_folder: str, *inis: str) -> None:
        # Grab and store config when init
        self._config = self._load_config(config_folder, *inis)

    # For python test framework usage
    @property
    def config(self) -> configparser.ConfigParser:
        return self._config

    # For Robot framework usage
    def Get_Config_Value(self, section: str, key: str) -> str:
        try:
            value = self._config[section][key]
        except KeyError:
            raise KeyError(
                f'Find no key under config["{section}"]["{key}"], please check config file.'
            )
        return value

    @staticmethod
    def _load_config(config_folder: str, *inis: str) -> configparser.ConfigParser:
        if not inis:
            raise Exception("No given ini file indicator in ConfigLoader")
        for each_ini in inis:
            if not os.path.isfile(f"{config_folder}/{each_ini}.ini"):
                raise Exception("Cannot find this filepath")
        path_list = []
        for each_ini in inis:
            path_list.append(pathlib.Path(f"{config_folder}/{each_ini}.ini"))
        config = configparser.ConfigParser()
        config.read(path_list, encoding="utf-8")
        return config
