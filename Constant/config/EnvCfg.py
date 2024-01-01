# -*- coding: utf-8 -*-

import yaml
import os


with open(os.path.dirname(__file__) + "/config.yaml", "r", encoding="utf-8") as f:
    EnvCfg: dict = yaml.safe_load(f)
