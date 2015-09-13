from __future__ import print_function, division, absolute_import
import pandas
import tempfile
import unittest

from pandas.util.testing import assert_frame_equal

from . import Correlation
from .Data import CSVFile

class TestTrafficCorrelationAnalyzer(unittest.TestCase):
    def setUp(self):
        raw_data = pandas.DataFrame({
            'src': ['1.1.1.1', '2.1.1.1', '3.1.1.1', '1.1.1.1', '1.1.1.1'],
            'dst': ['2.1.1.1', '3.1.1.1', '2.1.1.1', '2.1.1.1', '2.1.1.1'],
        })
        self.temp_path = tempfile.mktemp(suffix='csv')
        raw_data.to_csv(self.temp_path, sep=',')

    def test_case_zero_pivot_node(self):
        windows = pandas.DataFrame({
            'start_time': [0, 1],
            'end_time': [1, 3],
        })
        data = CSVFile(self.temp_path, {'win_type': 'flow'})
        analyzer = Correlation.TrafficCorrelationAnalyzer(data,
                                                          src_col='src',
                                                          dst_col='dst',
                                                          windows=windows)
        features = analyzer.create_features(3)
        self.assertIs(None, features)

    def test_case_one_pivot_node_trival_correlation(self):
        windows = pandas.DataFrame({
            'start_time': [0, 1],
            'end_time': [1, 3],
        })
        data = CSVFile(self.temp_path, {'win_type': 'flow'})
        analyzer = Correlation.TrafficCorrelationAnalyzer(data,
                                                          src_col='src',
                                                          dst_col='dst',
                                                          windows=windows)
        features = analyzer.create_features(2)
        expected = pandas.DataFrame([[3.0, 0.0], [0.0, 6.0]])
        assert_frame_equal(expected, features)
        graph = analyzer.generate_correlation_graph(features, 0.1)
        expected = pandas.DataFrame([[True, True], [True, True]])
        assert_frame_equal(expected, graph)

    def test_case_one_pivot_node_non_trival_correlation(self):
        windows = pandas.DataFrame({
            'start_time': [0, 1, 3],
            'end_time': [1, 3, 5],
        })
        data = CSVFile(self.temp_path, {'win_type': 'flow'})
        analyzer = Correlation.TrafficCorrelationAnalyzer(data,
                                                          src_col='src',
                                                          dst_col='dst',
                                                          windows=windows)
        features = analyzer.create_features(3)
        assert_frame_equal(pandas.DataFrame([[5.0, 0.0], [0, 10.0], [10, 0]]),
                           features)

        assert_frame_equal(pandas.DataFrame([[True, True], [True, True]]),
                           analyzer.generate_correlation_graph(features, 0.1))

        assert_frame_equal(pandas.DataFrame([[True, False], [False, True]]),
                           analyzer.generate_correlation_graph(features, 0.9))

    def test_case_two_pivot_nodes(self):
        windows = pandas.DataFrame({
            'start_time': [0, 1],
            'end_time': [1, 3],
        })
        data = CSVFile(self.temp_path, {'win_type': 'flow'})
        analyzer = Correlation.TrafficCorrelationAnalyzer(data,
                                                          src_col='src',
                                                          dst_col='dst',
                                                          windows=windows)
        features = analyzer.create_features(1)
        expected = pandas.DataFrame([[3.0], [0.0]])
        assert_frame_equal(expected, features)


if __name__ == '__main__':
    unittest.main()
