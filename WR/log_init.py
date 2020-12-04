# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 13:26:44 2020
@author: Working Rational
@source: https://www.codegrepper.com/code-examples/delphi/python+log+handler+multiple+files
"""

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s - [%(levelname)s] - %(lineno)d - %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)


