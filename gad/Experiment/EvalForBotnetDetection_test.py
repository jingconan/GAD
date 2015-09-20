from __future__ import print_function, division, absolute_import
import pandas
import tempfile
import unittest
import numpy

from pandas.util.testing import assert_frame_equal
from gad.Detector.Data import CSVFile

from . import EvalForBotnetDetection

class TestBotnetDetectionEval(unittest.TestCase):
    def setUp(self):
        raw_data = pandas.DataFrame({
            'StartTime': [
                          # for normal flows.
                          '2011/08/16 10:01:44.000000',
                          '2011/08/16 10:01:45.000000',
                          '2011/08/16 10:01:46.000000',
                          '2011/08/16 10:01:47.000000',
                          '2011/08/16 10:01:48.000000',
                          '2011/08/16 10:01:49.000000',
                          '2011/08/16 10:01:50.000000',
                          '2011/08/16 10:01:51.000000',
                          # for botnet flows.
                          '2011/08/16 10:01:52.000000',
                          '2011/08/16 10:01:53.000000',
                          '2011/08/16 10:01:54.000000',
                          '2011/08/16 10:01:55.000000',
                          # end time
                          '2011/08/16 10:01:56.000000',
                         ],
            'Sport': [
                      '80', '80', '80', '22',
                      '80', '80', '80', '22',
                      '10000', '10000', '10000', '10000',
                      '0',
                     ],
            # '2.1.1.1' is the botmaster. '1.1.1.1' and '3.1.1.1' are two bots.
            # '2.1.1.2' and '3.2.1.2' are two normal nodes.
            'SrcAddr': [
                        '2.1.1.2', '3.2.1.2', '2.1.1.2', '3.2.1.2',
                        '2.1.1.2', '3.2.1.2', '2.1.1.2', '3.2.1.2',
                        '1.1.1.1', '2.1.1.1', '3.1.1.1', '1.1.1.1',
                        'dummy',
                       ],
            'DstAddr': [
                        '3.2.1.2', '2.1.1.2', '3.2.1.2', '2.1.1.2',
                        '3.2.1.2', '2.1.1.2', '3.2.1.2', '2.1.1.2',
                        '2.1.1.1', '3.1.1.1', '2.1.1.1', '2.1.1.1',
                        'dummy',
                       ],
            'Label': [
                      'Normal', 'Normal', 'Normal', 'Normal',
                      'Normal', 'Normal', 'Normal', 'Normal',
                      'Botnet', 'Botnet', 'Botnet', 'Botnet',
                      'dummy',
                     ],
        })
        self.temp_path = tempfile.mktemp(suffix='.csv')
        raw_data.to_csv(self.temp_path, sep=',')


        detector_desc = {
            'version' : 1,
            'data': self.temp_path,
            'interval': 1,
            'win_size': 1,
            'win_type': 'time',
            'false_alarm_rate': 0.001,
            'time_index_feature_name': 'StartTime',
            'fea_option': [
                {
                    'feature_name': 'Sport',
                    'feature_type': 'port',
                    'quantized_number': 500,
                },
            ],
            'normal_rg': [0, 8],
            'method': 'mf',
            'pic_show': True,
            'pic_name': './res.eps',
            'export_flows': None,
            'data_type': 'csv',
            'csv': None,
            'alpha': 0.01,
            'ip_col_names': ['SrcAddr', 'DstAddr'],
            'botnet_detection_config': {
                'pivot_node_threshold': 3,
                'correlation_graph_threshold': 0.1,
                'w1': 1,
                'w2': 2,
                'lambda': 10,
                'sdpb_filepath': tempfile.mktemp(suffix='.sdpb'),
                'solution_filepath': tempfile.mktemp(suffix='.sol'),
                'csdp_binary': 'csdp',
            },
            'threshold': 0.1,
            'roc_thresholds': numpy.linspace(0, 1, 10).tolist(),
            'label_col_name': 'Label',
        }

        config = {
            'DETECTOR_DESC': detector_desc
        }

        self.config_file = tempfile.mktemp(suffix='.json')
        import json
        json.dump(config, open(self.config_file, 'w'))


    def test_botnet_detection_eval(self):
        argv = ['-c', self.config_file]
        evaluator = EvalForBotnetDetection.BotnetDetectionEval(argv)
        result = evaluator.run()

        ground_truth = evaluator.get_ground_truth()
        expected_all_ips = ['2.1.1.2', '2.1.1.1', '1.1.1.1', '3.1.1.1',
                            '3.2.1.2']
        self.assertEqual(set(expected_all_ips + ['dummy']),
                         ground_truth['all_ips'])

        expected_bot_ips = ['2.1.1.1', '3.1.1.1', '1.1.1.1']
        self.assertEqual(set(expected_bot_ips),
                         ground_truth['ground_truth_bot_ips'])

        result0 = result['metric'].detect_result[0]
        all_ips_in_abnormal_windows = result0['all_ips_in_abnormal_windows']
        self.assertEqual(set(['2.1.1.1', '1.1.1.1', '3.1.1.1']),
                         set(all_ips_in_abnormal_windows))

        detected_bot_ips = result0['detected_bot_ips']
        self.assertEqual(set(['2.1.1.1', '1.1.1.1', '3.1.1.1']),
                         set(detected_bot_ips))

        expected_coef = pandas.DataFrame([[1.0,-1.0], [-1.0, 1.0]])
        assert_frame_equal(expected_coef, result0['correlation_coef'])

class MockTimeBasedBotnetDetectionEval(
    EvalForBotnetDetection.TimeBasedBotnetDetectionEval):

    def __init__(self, eval_results, *args, **kwargs):
        self.eval_results = eval_results
        super(MockTimeBasedBotnetDetectionEval, self).__init__(*args, **kwargs)

    def detect(self):
        pass

    def eval(self):
        return self.eval_results[tuple(self.desc['detect_rg'])]


class TestTimeBasedBotnetDetectionEval(unittest.TestCase):
    # Please see https://goo.gl/TdNzG7 for the spreadsheet that checks the
    # math for the unittest.
    def test_time_based_botnet_detection_eval(self):
        detector_desc = {
            'version' : 1,
            'roc_thresholds': [0.2, 0.4],
            'timeframe_size': 1,
            'timeframe_rg': [0, 2],
            'timeframe_decay_ratio': 0.01,
        }

        config = {
            'DETECTOR_DESC': detector_desc
        }

        self.config_file = tempfile.mktemp(suffix='.json')
        import json
        json.dump(config, open(self.config_file, 'w'))

        argv = ['-c', self.config_file]
        eval_results = {
            (0, 1): {
                'metric':pandas.DataFrame({
                    'threshold': [0.2, 0.4],
                    'tp': [1, 2],
                    'fn': [3, 2],
                    'fp': [2, 3],
                    'tn': [4, 3],
                    'tpr': [float('nan'), float('nan')],
                    'fpr': [float('nan'), float('nan')],
                }),
                'ground_truth_bot_ips': ['1', '2', '3'],
            },
            (1, 2): {
                'metric':pandas.DataFrame({
                    'threshold': [0.2, 0.4],
                    'tp': [2, 4],
                    'fn': [4, 2],
                    'fp': [1, 3],
                    'tn': [2, 5],
                    'tpr': [float('nan'), float('nan')],
                    'fpr': [float('nan'), float('nan')],
                }),
                'ground_truth_bot_ips': ['1', '2', '3', '4'],
            },
        }

        evaluator = MockTimeBasedBotnetDetectionEval(eval_results, argv)
        result = evaluator.run()
        expected_result = pandas.DataFrame({
            'threshold': [0.2, 0.4],
            'FPR': [0.3333333333, 0.4375],
            'TPR': [0.2940140854, 0.5880281707],
        })
        assert_frame_equal(expected_result, result)


if __name__ == '__main__':
    unittest.main()
