#!/usr/bin/env python
from octomy.utils.setup import megasetup
import logging
import os
import pprint
from setuptools import setup

logger = logging.getLogger(__name__)


source_data = {
	  "base_name": "common"
	, "group_base_name": "octomy"
	, "cwd": os.path.dirname(os.path.abspath(__file__))
	, "debug": True
}

package = megasetup(source_data = source_data)

setup(**package)
