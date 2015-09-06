#!/usr/bin/env python
""" Evaluate the performance of detector
get the statistical quantify for the hypotheis test
like False Alarm Rate.
"""
from __future__ import print_function, division, absolute_import
import copy, os
from ..Detector import MEM_FS
from ..util import update_not_none, plt, np
from ..util import zdump, zload
import itertools

from .Detect import Detect

class Eval(Detect):
    """plot ROC curve for the hypothesis test"""
    def get_ground_truth(self):
        record_data = self.detector.record_data
        data_handler = self.detector.data_file
        win_size = self.desc['win_size']
        win_num = len(record_data['winT'])
        botnet_flow_num = np.zeros((win_num,), dtype=float)
        flow_num = np.zeros((win_num,), dtype=float)
        for i, time in enumerate(record_data['winT']):
            win_data = data_handler.data.get_rows('Label',
                                                  rg=[time, time + win_size],
                                                  rg_type='time')
            botnet_flow_num[i] = sum([1 if 'Botnet' in row else 0 for row in
                                        win_data])
            flow_num[i] = len(win_data)

        #  self.detector.record_data['botnet_flow_num'] = botnet_flow_num
        botnet_flow_ratio = botnet_flow_num / flow_num
        return botnet_flow_ratio > 0.01

    def eval(self, thresholds):
        ground_truth = self.get_ground_truth()
        divs = self.detector.record_data['entropy']
        divs = np.array(divs, dtype=float)

        res = np.zeros((len(thresholds), 2))
        for i, threshold in enumerate(thresholds):
            det_res = divs > threshold
            tp = np.sum(ground_truth & det_res)
            tn = np.sum(np.logical_not(ground_truth) & np.logical_not(det_res))
            fp = np.sum(np.logical_not(ground_truth) & det_res)
            fn = np.sum(ground_truth & np.logical_not(det_res))
            precision = tp * 1.0 / (tp + fp)
            recall = tp * 1.0 / (tp + fn)
            tpr = tp * 1.0 / (tp + fn)
            fpr = fp * 1.0 / (fp + tn)
            res[i, 0] = fpr
            res[i, 1] = tpr

        plt.subplot(211)
        plt.plot(res[:, 0], res[:, 1])
        ground_truth = self.get_ground_truth()
        plt.subplot(212)
        plt.plot(ground_truth)
        plt.show()

        import ipdb;ipdb.set_trace()


    def run(self):
        self.desc = copy.deepcopy(self.args.config['DETECTOR_DESC'])
        update_not_none(self.desc, self.args.__dict__)

        self.detect()
        self.eval(np.linspace(0, 10, 50))
