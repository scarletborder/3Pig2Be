# -*- coding: utf-8 -*-

import yaml
import sys

with open(sys.path[0] + "/config/config.yaml", "r", encoding="utf-8") as f:
    EnvCfg: dict = yaml.safe_load(f)
