"""put import module sentence that may fail here
"""
from __future__ import print_function, division

import logging
logging.basicConfig()
logger = logging.getLogger('util')

try:
    import numpy as np
except ImportError:
    np = None
    logger.warning('no numpy, some funcationality may be affected')

try:
    import guiqwt.pyplot as plt
    logger.info('Use [guiqwt] as plot backend')
except ImportError:
    try:
        import matplotlib.pyplot as plt
        # import guiqwt.pyplot as plt
        logger.info('Use [matplotlib] as plot backend')
    except Exception:
        plt = None
        logger.warning('No [guiqwt] and [matplotlib], cannot visualize the result')

try:
    from collections import Counter
except ImportError:
    Counter = None
    logger.warning('No [collection.Counter], some funcationality may be affected')

try:
    import _mysql as mysql
    from MySQLdb.constants import FIELD_TYPE
except ImportError:
    mysql = None
    # FIELD_TYPE = object
    # FIELD_TYPE = object

    from Namespace import Namespace
    FIELD_TYPE = Namespace({
            'INT24': None,
            'LONG': None,
            'LONGLONG': None
        })

    logger.warning('Cannot import sql related function, reading for sql server is not supported')


try:
    import tables
except ImportError:
    tables = False

#########################################
## Adaption for Python3
#########################################

try:
    import Queue as queue # replace with 'import queue' if using Python 3
except ImportError:
    import queue

try:
    from itertools import izip
except ImportError:
    izip = zip

