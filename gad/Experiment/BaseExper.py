from __future__ import print_function, division, absolute_import
import argparse
import logging
import os
from ..util import abstract_method, load_config, Load

# ROOT = os.environ.get('SADIT_ROOT')


def parse_logging_arg(arg):
    return dict(v.split(':') for v in arg.split(','))

class BaseExper(object):
    # ROOT = ROOT
    LOGGER_NAME = 'experiment'

    def __init__(self, argv, parser=None):
        # import ipdb;ipdb.set_trace()
        if parser is None:
            parser = argparse.ArgumentParser(add_help=False)
            # parser = argparse.ArgumentParser()
        self.parser = parser
        self.init_parser(parser)
        self.args, self.res_args = parser.parse_known_args(argv)

        self.logger = logging.getLogger(self.LOGGER_NAME)

        # set logger status
        logger_setting = parse_logging_arg(self.args.logging)
        for logger_name, logger_lvl in logger_setting.iteritems():
            lvl = logging.getLevelName(logger_lvl)
            logging.getLogger(logger_name).setLevel(lvl)

        if self.args.help:
            self.print_help()
            import sys; sys.exit(0)

        if self.args.config is None:
            print('You must specifiy --config option, run with -h option to see help')
            import sys; sys.exit(0)

    def print_help(self):
        self.parser.print_help()

    def init_parser(self, parser):
        parser.add_argument('-h', '--help', default=False, action='store_true',
                help="""print help message""")
        parser.add_argument('-c', '--config', default=None,
                type=lambda x: load_config(x),
                help="""config""")
        parser.add_argument('--logging',
                            default="root:INFO,experiment:INFO,detector:INFO",
                            help=('logging level. See '
                                  'https://docs.python.org/2/library/'
                                  'logging.html#levels'))



    def run(self):
        abstract_method()
