from typing import List

from my_dataclass.api_wrapper_config import ApiWrapperConfig
from util.base_wrapper import BaseWrapper


class BaseApiWrapper(BaseWrapper):
    configs: List[ApiWrapperConfig]

    def __init__(self, dc):

        self.configs = [ApiWrapperConfig.from_dict(idx, config) for idx, config in enumerate(self.configsDict)]
        super().__init__(dc)

    def get(self, hint, data):
        if hint in self.allConfig:
            config = self.getConfigByName(hint)
            config.setJson(data)
            try:
                return getattr(self, f"get{self.dc.ownCapitalize(config.name)}")(config, data)
            except:
                return self.baseGet(config, data)
        else:
            print(f"Error Hint: {hint} not fund")
        return None

    def baseGet(self, config, data):
        config.addData(config.class_.from_dict(data))
        return config.datas
