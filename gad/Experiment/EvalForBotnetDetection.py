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

    def get_botnet_info(self):
        label_col_name = self.desc['label_col_name']
        ip_col_names = self.desc['ip_col_names']
        rg_type = self.desc['win_type']
        win_size = self.desc['win_size']
        assert len(ip_col_names) <= 2, "at most two IP columns are allowed."

        # TODO(hbhzwj) use winT sotred in record_data is very ugly. Implement
        # a method to register some logging function to detector.
        record_data = self.detector.record_data
        data_handler = self.detector.data_file
        data_recorder = DataRecorder()
        win_bot_ips = []
        win_ips = []
        for i, time in enumerate(record_data['winT']):
            win_data = data_handler.data.get_rows(label_col_name,
                                                  rg=[time, time + win_size],
                                                  rg_type=rg_type)
            is_botnet_flow = [self.parse_label(label) for label in win_data]
            botnet_flow_num = sum(is_botnet_flow)
            botnet_flow_ratio = botnet_flow_num * 1.0 / len(is_botnet_flow)

            # Get IPS from flows with Botnet label and get the union set.
            flow_ips = data_handler.data.get_rows(ip_col_names,
                                             rg=[time, time + win_size],
                                             rg_type=rg_type)

            win_bot_ip = set()
            win_ip = set()
            for idx, ips in enumerate(flow_ips):
                if is_botnet_flow[idx]:
                    win_bot_ip |= set(ips)
                win_ip |= set(ips)

            win_bot_ips.append(win_bot_ip)
            win_ips.append(win_ip)

            data_recorder.add(botnet_flow_num=botnet_flow_num,
                              flow_num=len(win_data),
                              botnet_flow_ratio=botnet_flow_ratio)
        return {
            'botnet_info': data_recorder.to_pandas_dataframe(),
            'win_bot_ips': win_bot_ips,
            'win_ips': win_ips,
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
        label_info = self.get_botnet_info()
        ground_truth_bot_ips = set.union(*label_info['win_bot_ips'])
        all_ips = set.union(*label_info['win_ips'])

        divs = self.detector.record_data['entropy']
        divs = np.array(divs, dtype=float) / np.max(divs)

        bot_detector = BotDetector.SoBotDet()

        data_recorder = DataRecorder()
        res = np.zeros((len(thresholds), 2))
        for i, threshold in enumerate(thresholds):
            det_res = divs > threshold
            detected_ips = bot_detector.detect(no_anomaly_detect=True)
            tp, fn, tn, fp, sensitivity, specificity = \
                get_detect_metric(ground_truth_bot_ips, detected_ips, all_ips)
            tpr = tp * 1.0 / (tp + fn) if (tp + fn) > 0 else float('nan')
            fpr = fp * 1.0 / (fp + tn) if (fp + tn) > 0 else float('nan')
            data_recorder.add(threshold=threshold, tp=tp, tn=tn, fp=fp, fn=fn,
                              tpr=tpr, fpr=fpr)

        data_frame = data_recorder.to_pandas_dataframe()
        data_frame.set_index(['threshold'], drop=False)
        return {
            'metric': data_frame,
            'botnet_info': label_info['botnet_info'],
            'bot_ips': ground_truth_bot_ips,
        }

    def run(self):
        self.desc = copy.deepcopy(self.args.config['DETECTOR_DESC'])
        update_not_none(self.desc, self.args.__dict__)

        self.detect()
        self.eval()


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

        parser.add_argument('--alpha', default=None, type=float,
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

        import ipdb;ipdb.set_trace()
        return data_recorder.to_pandas_dataframe()

    def run(self):
        timeframe_rg = self.desc['timeframe_rg']
        thresholds = self.desc['roc_thresholds']
        assert len(timeframe_rg) == 2, "unknown format of timeframe_rg"
        timeframe_size = self.desc['timeframe_size']
        alpha = self.desc['alpha']

        cur_time = timeframe_rg[0]
        data_recorder = DataRecorder()
        timeframe_idx = 0
        while cur_time < timeframe_rg[1]:
            self.desc['detect_rg'] = [cur_time, cur_time + timeframe_size]
            self.detect()
            eval_result = self.eval()
            metric = eval_result['metric']
            bot_ips = eval_result['bot_ips']
            bot_ip_num =float(len(bot_ips))
            correct_value = np.exp(alpha * timeframe_idx) + 1
            tTP = metric.tp * correct_value / bot_ip_num # UPDATE HERE
            tFN = metric.fn * correct_value / bot_ip_num
            tFP = metric.fp / bot_ip_num
            tTN = metric.tn / bot_ip_num
            for idx, threshold in enumerate(thresholds):
                data_recorder.add(threshold=threshold,
                                  timeframe_idx=timeframe_idx,
                                  tTP=tTP[idx],
                                  tFN=tFN[idx],
                                  tFP=tFP[idx],
                                  tTN=tTN[idx])

            cur_time += timeframe_size
            timeframe_idx += 1

        self.get_roc_curve(data_recorder.to_pandas_dataframe())
        import ipdb;ipdb.set_trace()

    def plot(self, data_recorder):
        pass
