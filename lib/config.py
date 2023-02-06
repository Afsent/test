import json
import os.path

config_file = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "conf.json"
)


class Config:
    main = None
    service = None

    @classmethod
    def setup(cls, name, config_file=config_file):
        with open(config_file) as f:
            config = json.load(f)
            cls.main = config.get("main")
            cls.service = config.get(name)
