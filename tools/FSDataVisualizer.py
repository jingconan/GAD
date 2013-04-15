#!/usr/bin/env python
from __future__ import print_function, division
import sys; sys.path.append('../')

from Detector.DataParser import RawParseData
from pylab import *

class Visualizer(object):
    def __init__(self, f_name):
        self.f_name = f_name
        data, self.keys = RawParseData(f_name)
        self.zip_data = zip(*data)

    def get(self, name):
        idx = self.keys.index(name)
        return self.zip_data[idx]

    def vis(self):
        flow_size = [int(v) for v in self.get('flow_size')]
        plot(flow_size)
        show()
        pass

    pass

if __name__ == "__main__":
    import sys
    import argparse
    parser = argparse.ArgumentParser(description='visualizer of FS data')
    parser.add_argument('file', help='name for the fs data file')
    args, res_args = parser.parse_known_args()
    v = Visualizer(args.file)
    v.vis()
