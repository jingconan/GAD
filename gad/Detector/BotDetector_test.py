from __future__ import print_function, division, absolute_import
import pandas
import tempfile
import unittest

from pandas.util.testing import assert_frame_equal

from . import BotDetector
from . import StoDetector
from . import Data
from . import DataHandler

class TestSoBotDet(unittest.TestCase):
    def setUp(self):
        raw_data = pandas.DataFrame({
            'StartTime': ['2011/08/16 10:01:46.000000',
                          '2011/08/16 10:01:47.000000',
                          '2011/08/16 10:01:48.000000',
                          '2011/08/16 10:01:49.000000',
                          '2011/08/16 10:01:50.000000'],
            'Sport': ['100', '1000', '100', '200', 200],
            'SrcAddr': ['1.1.1.1', '2.1.1.1', '3.1.1.1', '1.1.1.1', '1.1.1.1'],
            'DstAddr': ['2.1.1.1', '3.1.1.1', '2.1.1.1', '2.1.1.1', '2.1.1.1'],
        })
        self.temp_path = tempfile.mktemp(suffix='.csv')
        raw_data.to_csv(self.temp_path, sep=',')

    def test_case_one(self):
        import numpy
        desc = {
            'version' : 1,
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
            'normal_rg': None,
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
        }

       #
        data = Data.CSVFile(self.temp_path, desc)
        data_handler = DataHandler.ModelFreeQuantizeDataHandler(data, desc)

        anomaly_detector = StoDetector.ModelFreeAnoDetector(desc)
        base_result = anomaly_detector.detect(data_handler)
        self.assertEqual([0.91629073187415511,
                          1.6094379124341003,
                          0.91629073187415511,
                          0.91629073187415511],
                         base_result['entropy'])

        desc['anomaly_detector'] = anomaly_detector
        bot_detector = BotDetector.SoBotDet(desc)
        result = bot_detector.detect(None,
                                     anomaly_detect=False)
        self.assertEqual(16.0, result['interact_measure_diff'])
        self.assertEqual(['1.1.1.1', '3.1.1.1'],
                         result['detected_bot_ips'])

if __name__ == '__main__':
    unittest.main()
