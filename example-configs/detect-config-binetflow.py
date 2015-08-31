from datetime import datetime

ROOT = ''
# VERSION is used to indicate the config version. In version 1, fea_option is
# no longer a dict but a array of dict.
VERSION = 1

#################################
##   Parameters For Detector  ###
#################################

ANO_ANA_DATA_FILE = './Share/AnoAna.txt'
DETECTOR_DESC = {
    'version' : VERSION,
    'interval': 20,
    'win_size': 20,
    'win_type': 'time', # 'time'|'flow'
    'fr_win_size': 100, # window size for estimation of flow rate
    'false_alarm_rate': 0.001,
    'time_index_feature_name': 'StartTime',
    'fea_option': [
        {
            'feature_name': 'TotBytes',
            'feature_type': 'numerical',
            'quantized_number': 4,
            'range': [0, 608224604],
        },
        {
            'feature_name': 'SrcBytes',
            'feature_type': 'numerical',
            'quantized_number': 4,
            'range': [0, 251771542],
        },
        {
            'feature_name': 'Dur',
            'feature_type': 'numerical',
            'quantized_number': 10,
            'range': [0, 3600],
        },
        {
            'feature_name': 'Proto',
            'feature_type': 'categorical',
            'symbol_index': {
                'tcp': 1,
                'udp': 2,
                'ipx/spx': 3,
                'arp': 4,
                'icmp': 5,
                'pim': 6,
                'rtcp': 7,
                'rtp': 8,
                'igmp': 9,
                'ipv6-icmp': 10,
                'esp': 11,
                'ipv6': 12,
                'DEFAULT': 0
            },
        },
        {
            'feature_name': 'SrcAddr',
            'feature_type': 'ipv4_address',
            'quantized_number': 10,
            'range': [0, 4294967296],
            'ipv6_map_to_value': 0,
        },
        {
            'feature_name': 'DstAddr',
            'feature_type': 'ipv4_address',
            'quantized_number': 10,
            'range': [0, 4294967296],
            'ipv6_map_to_value': 0,
        },
    ],
    'ano_ana_data_file': ANO_ANA_DATA_FILE,
    'normal_rg': None,
    'detect_rg': [1000, 2000],
    'detector_type': 'mfmb',
    'max_detect_num': 1000,
    'pic_show': True,
    'pic_name': './res.eps',
    'export_flows': None,
    'csv': None,
}
