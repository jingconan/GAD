#!/usr/bin/env python
""" Evaluate the performance of detector
get the statistical quantify for the hypotheis test
like False Alarm Rate.
"""
from __future__ import print_function, division, absolute_import
import copy, os
import collections
from ..Detector import MEM_FS
from ..Detector import BotDetector
from ..util import update_not_none, plt, np, DataRecorder
from ..util import zdump, zload, Load, get_detect_metric
import itertools
import pandas

from .Detect import Detect

class BotnetDetectionEval(Detect):
    """plot ROC curve for the hypothesis test"""

    def init_parser(self, parser):
        super(BotnetDetectionEval, self).init_parser(parser)
        parser.add_argument('--roc_thresholds', default=None, type=Load,
                help=("any valid python expression. Thresholds used for get "
                      "roc curve"))

        parser.add_argument('--label_col_name', default=None, type=str,
                            help="name of the label column")

        parser.add_argument('--ip_col_names', default=None,
                            type=lambda x: x.split(','),
                            help="name of the ip columns")

    @staticmethod
    def parse_label(label):
        return 'Botnet' in label

    def get_ground_truth(self):
        label_col_name = self.desc['label_col_name']
        ip_col_names = self.desc['ip_col_names']
        detect_rg = self.desc.get('detect_rg')
        rg_type = self.desc['win_type']
        assert len(ip_col_names) <= 2, "at most two IP columns are allowed."
        fetch_columns = [label_col_name] + ip_col_names
        data_records = self.detector.data_file.data.get_rows(fetch_columns,
                                                             rg=detect_rg,
                                                             rg_type=rg_type)
        ground_truth_bot_ips = set()
        all_ips = set()
        for row in data_records:
            if self.parse_label(row[0]): # is botflow
                ground_truth_bot_ips.add(row[1])
                ground_truth_bot_ips.add(row[2])
            all_ips.add(row[1])
            all_ips.add(row[2])

        return {
            'ground_truth_bot_ips': ground_truth_bot_ips,
            'all_ips': all_ips,
        }

    @staticmethod
    def get_detected_ips(label_info, detection):
        ips = set()
        for i, d in enumerate(detection):
            if not d:
                continue
            ips |= set(label_info['win_ips'][i])
        return ips


    def eval(self):
        thresholds = self.desc['roc_thresholds']
        ground_truth = self.get_ground_truth()

        divs = self.detector.record_data['entropy']
        divs = np.array(divs, dtype=float) / np.max(divs)

        bot_detector_desc = copy.deepcopy(self.desc)
        bot_detector_desc.update({
            'threshold': 0,
            'anomaly_detector': self.detector,
        })
        bot_detector = BotDetector.SoBotDet(bot_detector_desc)

        data_recorder = DataRecorder()
        res = np.zeros((len(thresholds), 2))
        for i, threshold in enumerate(thresholds):
            bot_detector.desc['threshold'] = threshold
            self.logger.info('Start to detect with threshold %s ' % (threshold))
            result = bot_detector.detect(None, anomaly_detect=False)
            tp, fn, tn, fp, sensitivity, specificity = \
                get_detect_metric(ground_truth['ground_truth_bot_ips'],
                                  result['detected_bot_ips'],
                                  ground_truth['all_ips'])
            tpr = tp * 1.0 / (tp + fn) if (tp + fn) > 0 else float('nan')
            fpr = fp * 1.0 / (fp + tn) if (fp + tn) > 0 else float('nan')
            data_recorder.add(threshold=threshold, tp=tp, tn=tn, fp=fp, fn=fn,
                              tpr=tpr, fpr=fpr,
                              detect_result=result)

        data_frame = data_recorder.to_pandas_dataframe()
        data_frame.set_index(['threshold'], drop=False)
        return {
            'metric': data_frame,
            'ground_truth_bot_ips': ground_truth['ground_truth_bot_ips'],
        }

    def run(self):
        self.desc = copy.deepcopy(self.args.config['DETECTOR_DESC'])
        update_not_none(self.desc, self.args.__dict__)

        self.detect()
        return self.eval()


class TimeBasedBotnetDetectionEval(BotnetDetectionEval):
    """Calculate corrected metrics (tTP, tFN, tFP, tTN) for botnet detection.

    Please refer to the following paper for the details:
    Garcia, Sebastian, et al. 'An empirical comparison of botnet detection
    methods.' Computers & Security 45 (2014): 100-123.
    """
    def init_parser(self, parser):
        super(TimeBasedBotnetDetectionEval, self).init_parser(parser)

        parser.add_argument('--timeframe_size', default=None, type=float,
                help=("--timeframe_size [float] the size of each time frame."
                      "Metrics (tTP, tFN, tFP, tTN) will be calculated for "
                      "each time frame."))

        def parse_tuple(s):
            return tuple(float(val) for val in
                         self.desc['timeframe_rg'].split[','])

        parser.add_argument('--timeframe_rg', default=None, type=parse_tuple,
                help=("comma-separated strings, the first one is start time, "
                      "the second one is end time. Data in the range will be "
                      "divided to timeframes for evaluation."))

        parser.add_argument('--timeframe_decay_ratio', default=None, type=float,
                help="parameter in the exp correction function.")

    def get_roc_curve(self, stats):
        thresholds = self.desc['roc_thresholds']
        data_recorder = DataRecorder()
        for threshold in thresholds:
            threshold_stats = stats[stats.threshold==threshold]
            sum_stats = threshold_stats.sum()
            FPR = sum_stats.tFP / (sum_stats.tFP + sum_stats.tTN)
            TPR = sum_stats.tTP / (sum_stats.tTP + sum_stats.tFN)
            data_recorder.add(threshold=threshold,
                              FPR=FPR,
                              TPR=TPR)

        return data_recorder.to_pandas_dataframe()

    def run(self):
        timeframe_rg = self.desc['timeframe_rg']
        thresholds = self.desc['roc_thresholds']
        assert len(timeframe_rg) == 2, "unknown format of timeframe_rg"
        timeframe_size = self.desc['timeframe_size']
        timeframe_decay_ratio = self.desc['timeframe_decay_ratio']

        cur_time = timeframe_rg[0]
        data_recorder = DataRecorder()
        timeframe_idx = 0
        while cur_time < timeframe_rg[1]:
            self.desc['detect_rg'] = [cur_time, cur_time + timeframe_size]
            self.detect()
            eval_result = self.eval()
            metric = eval_result['metric']
            bot_ips = eval_result['ground_truth_bot_ips']
            bot_ip_num =float(len(bot_ips))
            correct_value = np.exp(-1 * timeframe_decay_ratio * timeframe_idx) + 1
            tTP = metric.tp * correct_value / bot_ip_num # UPDATE HERE
            tFN = metric.fn * correct_value / bot_ip_num
            tFP = metric.fp * 1.0 / bot_ip_num
            tTN = metric.tn * 1.0 / bot_ip_num
            for idx, threshold in enumerate(thresholds):
                data_recorder.add(threshold=threshold,
                                  timeframe_idx=timeframe_idx,
                                  tTP=tTP[idx],
                                  tFN=tFN[idx],
                                  tFP=tFP[idx],
                                  tTN=tTN[idx])

            cur_time += timeframe_size
            timeframe_idx += 1

        roc = self.get_roc_curve(data_recorder.to_pandas_dataframe())
        print('roc metric is: ')
        print(roc)
        return roc

    def plot(self, data_recorder):
        pass
