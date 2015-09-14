from __future__ import print_function, division, absolute_import
import collections
import numpy as np
import pandas
import logging

class CorrelationAnalyzer(object):
    """Interface of Correlation Analyzer
    """
    def __init__(self, data):
        self.data = data

    def create_feature(self):
        pass

    def generate_correlation_graph(self):
        pass


class TrafficCorrelationAnalyzer(object):
    def __init__(self, data, src_col, dst_col, windows):
        self.src_col = src_col
        self.dst_col = dst_col
        self.data = data
        self.windows = windows

    @staticmethod
    # interactions has format (src, dst, weight)
    def _identify_pivot_nodes(interactions, threshold):
        node_weight = collections.defaultdict(float)
        for src, dst, weight in interactions:
            node_weight[src] += weight
            node_weight[dst] += weight

        # return all nodes whose weight is > threshold
        return dict((node, weight)
                    for node, weight in node_weight.iteritems()
                    if weight > threshold)

    @staticmethod
    def _calculate_interact_measure(window_data, pivot_nodes):
        node_set = set()
        def process_window(data):
            interact_measure = collections.defaultdict(float)
            for src, dst, weight in data:
                node_set.add(src)
                node_set.add(dst)
                interact_measure[src] += pivot_nodes.get(dst, 0)
                interact_measure[dst] += pivot_nodes.get(src, 0)
            return interact_measure

        measures = [process_window(data) for data in window_data]
        # Remove pivot nodes
        node_set -= set(pivot_nodes.keys())
        observations = []
        for measure in measures:
            obs = [measure.get(node, 0) for node in node_set]
            observations.append(obs)

        # each column represents the feature of a node
        return pandas.DataFrame(observations), node_set

    def create_features(self, threshold):
        interactions = []
        all_interactions = []
        for index, row in self.windows.iterrows():
            window_df = self.data.get_rows(fields=[self.src_col, self.dst_col],
                                           rg=[row['start_time'],
                                               row['end_time']],
                                           rg_type='flow')
            interaction = []
            for src, dst in window_df:
                tmp = [src, dst, 1]
                interaction.append(tmp)
                all_interactions.append(tmp)

            interactions.append(interaction)


        pivot_nodes = self._identify_pivot_nodes(all_interactions, threshold)
        if len(pivot_nodes) == 0:
            logging.warning('There is no pivotal nodes detected!')
            return

        self.features, self.node_set = \
            self._calculate_interact_measure(interactions,
                                             pivot_nodes)
        if len(self.node_set) == 0:
            logging.warning('all nodes are detected as pivot nodes. Are you '
                            'sure?')
        return self.features

    def generate_correlation_graph(self, features, threshold):
        self.correlation_coef = features.corr()
        A = abs(self.correlation_coef) > threshold
        return A
