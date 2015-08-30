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

    #  def init_parser(self, parser):
    #      super(Eval, self).init_parser(parser)

        #  parser.add_argument('--res_folder', default=None,
        #                      help='result folder')

        #  parser.add_argument('--plot', default=False, action='store_true',
        #                      help='plot the result or not')

    def _get_botnet_flow_num_all_win(self):
        record_data = self.detector.record_data
        data_handler = self.detector.data_file
        win_size = self.desc['win_size']
        botnet_flow_num = []
        for time in record_data['winT']:
            win_data = data_handler.data.get_rows('Label',
                                                  rg=[time, time + win_size],
                                                  rg_type='time')
            num = sum([1 if 'Botnet' in row else 0
                       for row in win_data])
            botnet_flow_num.append(num)

        self.detector.record_data['botnet_flow_num'] = botnet_flow_num
        return botnet_flow_num

    def get_ground_truth(self):
        botnet_flow_num = self._get_botnet_flow_num_all_win()
        return np.array([num > 0 for num in botnet_flow_num], dtype=bool)

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

        plt.plot(res[:, 0], res[:, 1])
        plt.show()
        import ipdb;ipdb.set_trace()


    def run(self):
        self.desc = copy.deepcopy(self.args.config['DETECTOR_DESC'])
        update_not_none(self.desc, self.args.__dict__)

        self.detect()
        self.eval(np.linspace(0, 10, 50))
