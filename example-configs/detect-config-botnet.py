from datetime import datetime
import numpy
import json

ROOT = ''
# VERSION is used to indicate the config version. In version 1, fea_option is
# no longer a dict but a array of dict.
VERSION = 1

#2011/08/16 10:01:46.972101
def fast_date_parser(date):
    assert(len(date) == 26)
    return datetime(year=int(date[0:4]),
                    month=int(date[5:7]),
                    day=int(date[8:10]),
                    hour=int(date[11:13]),
                    minute=int(date[14:16]),
                    second=int(date[17:19]),
                    microsecond=int(date[20:26]))

#################################
##   Parameters For Detector  ###
#################################

DETECTOR_DESC = {
    'version' : VERSION,
    'interval': 2,
    'win_size': 2,
    'win_type': 'time', # 'time'|'flow'
    'fr_win_size': 100, # window size for estimation of flow rate
    'false_alarm_rate': 0.001,
    'time_index_feature_name': 'StartTime',
    # date_parse can either be a format string or a function. If it is a
    # string, a parser function will be contructed using
    # pandas.datetime.strptime.
    #  'date_parser': '%Y/%m/%d %H:%M:%S.%f',
    'date_parser': fast_date_parser,
    'fea_option': [
        {
            'feature_name': 'TotBytes',
            'feature_type': 'numerical',
            'quantized_number': 3,
            'range': [0, 608224604],
        },
        #  {
        #      'feature_name': 'SrcBytes',
        #      'feature_type': 'numerical',
        #      'quantized_number': 50,
        #      'range': [0, 251771542],
        #  },
        #  {
        #      'feature_name': 'Dur',
        #      'feature_type': 'numerical',
        #      'quantized_number': 50,
        #      'range': [0, 3600],
        #  },
        {
            'feature_name': 'Proto',
            'feature_type': 'categorical',
            'symbol_index': {
                'tcp': 1,
                'udp': 2,
                #  'ipx/spx': 3,
                #  'arp': 4,
                #  'icmp': 5,
                #  'pim': 6,
                #  'rtcp': 7,
                #  'rtp': 8,
                #  'igmp': 9,
                #  'ipv6-icmp': 10,
                #  'esp': 11,
                #  'ipv6': 12,
                'DEFAULT': 0
            },
        },
        {
            'feature_name': 'Sport',
            'feature_type': 'port',
            'quantized_number': 300,
        },
        {
            'feature_name': 'Dport',
            'feature_type': 'port',
            'quantized_number': 10,
        },
        #  {
        #      'feature_name': 'SrcAddr',
        #      'feature_type': 'ipv4_address',
        #      'ip_cluster_num': 5,
        #      'distance_quantize_num': 3,
        #      'DEFAULT': -1,
        #      'ip_columns': ['SrcAddr'],
        #      'save_symbol_index_path': './SrcAddrSymbolIndex.json'
        #  },
        {
            'feature_name': 'SrcAddr',
            'feature_type': 'ipv4_address',
            'symbol_index': json.load(open('./SrcAddrSymbolIndex.json', 'r')),
        },
        #  {
        #      'feature_name': 'SrcAddr',
        #      'feature_type': 'categorical',
        #      'symbol_index': {
        #          '147.32.84.165': 1,
        #          'DEFAULT': 0,
        #      },
        #  },

    ],
    'normal_rg': [0, 1500],
    'method': 'mf',
    'pic_show': True,
    'pic_name': './res.eps',
    'export_flows': None,
    'data_type': 'csv',
    'roc_thresholds': numpy.linspace(0.4, 1, 10),
    #  'roc_thresholds': numpy.linspace(0.6, 0.7, 10),
    #  'roc_thresholds': [0.3],
    'csv': None,
    'timeframe_size': 300,
    'timeframe_rg': [1500, 6348],
    #  'timeframe_rg': [2100, 2400],
    #  'timeframe_rg': [1500, 1800],
    'timeframe_decay_ratio': 0.01,
    'label_col_name': 'Label',
    'ip_col_names': ['SrcAddr', 'DstAddr'],
    'botnet_detection_config': {
        'pivot_node_threshold': 3,
        'correlation_graph_threshold': 0.99,
        'w1': 0.1,
        'w2': 0.1,
        'lambda': 100,
        'max_graph_to_solve': 1500,
    },
}
