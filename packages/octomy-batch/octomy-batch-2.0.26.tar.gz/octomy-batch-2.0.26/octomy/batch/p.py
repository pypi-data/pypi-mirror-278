#!/usr/bin/env python

import importlib.util
import pathlib
import logging
import pprint


logger = logging.getLogger(__name__)

def run():
	logger.info(f"__name__:{__name__}")
	package_name = __name__.split('.')[0]
	logger.info(f"package_name:{package_name}")
	spec = importlib.util.find_spec(package_name)
	logger.info(f"spec:{pprint.pformat(spec)}")
	if spec and spec.origin:
		root_path = pathlib.Path(spec.origin).parent
		logger.info(f"root_path:{root_path}")

