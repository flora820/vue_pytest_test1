import logging
import logging.handlers
import os
import time
from common.text_util import base_dir


class LogUtil(object):
    def __init__(self):
        self.logger = logging.getLogger("")
